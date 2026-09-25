#!/usr/bin/env python3
"""Framesbase MCP 本地客户端（pi 技能配套脚本）。

Framesbase 是一个私人设计资料库。它的 MCP 服务器是无状态 HTTP JSON-RPC 端点：

    https://app.framesbase.app/mcp

鉴权走 OAuth 2.1（浏览器授权 + PKCE，公共客户端，无共享密钥）。本脚本替 pi 完成：

  1. 动态注册客户端（只注册一次，client_id 持久化到 auth.json）
  2. 浏览器授权 + PKCE 拿 access_token / refresh_token（refresh_token 自动续期）
  3. 调用 MCP 工具（tools/list、tools/call，工具名运行时发现，不写死）

凭证保存在 skills/framesbase/auth.json，已被仓库 .gitignore 的 **/auth.json 规则排除，绝不进 git。

用法：
    python3 framesbase.py auth                 # 首次接入：注册 + 浏览器授权
    python3 framesbase.py status               # 查看当前凭证 / 可用工具
    python3 framesbase.py tools                # 列出 MCP 可用工具
    python3 framesbase.py call <工具名> '<json参数>'   # 调用任意工具

    python3 framesbase.py browse [分类] [--type sites|apps|sections] [--limit N] [--offset N]
    python3 framesbase.py search <关键词> [--limit N]     # 只搜标题/分类名
    python3 framesbase.py fetch <卡片id>                  # 取 prompt 正文
    python3 framesbase.py related <卡片id> [--limit N]    # 同分类同类卡片
"""

from __future__ import annotations

import base64
import hashlib
import json
import secrets
import sys
import threading
import time
import urllib.parse
import urllib.request
import urllib.error
import webbrowser
from http.server import BaseHTTPRequestHandler, HTTPServer
from pathlib import Path

ISSUER = "https://app.framesbase.app"
MCP_URL = ISSUER + "/mcp"
REGISTER_URL = ISSUER + "/oauth/register"
AUTHORIZE_URL = ISSUER + "/oauth/authorize"
TOKEN_URL = ISSUER + "/oauth/token"

REDIRECT_PORT = 8787
REDIRECT_URI = f"http://127.0.0.1:{REDIRECT_PORT}/callback"
SCOPES = "entitlement profile"
CLIENT_NAME = "pi-framesbase"
PROTOCOL_VERSION = "2025-06-18"
AUTH_TIMEOUT_SECONDS = 300  # 浏览器授权等待上限

# 凭证文件：skills/framesbase/auth.json（__file__ = scripts/framesbase.py）
AUTH_FILE = Path(__file__).resolve().parent.parent / "auth.json"


# ---------------------------------------------------------------- 小工具

def b64url(raw: bytes) -> str:
    return base64.urlsafe_b64encode(raw).rstrip(b"=").decode("ascii")


def log(msg: str) -> None:
    print(msg, file=sys.stderr, flush=True)


BROWSER_UA = (
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
    "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36"
)


def http_json(method: str, url: str, data=None, headers=None, timeout=30):
    """发 JSON 请求，返回 (status, parsed_or_text)。"""
    body = None
    # 用浏览器 UA，避免被 Cloudflare 的「浏览器签名」规则拦截
    req_headers = {
        "User-Agent": BROWSER_UA,
        "Accept": "application/json, text/plain, */*",
        "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8",
    }
    if headers:
        req_headers.update(headers)
    if data is not None:
        body = json.dumps(data).encode("utf-8")
        req_headers["Content-Type"] = "application/json"
    req = urllib.request.Request(url, data=body, headers=req_headers, method=method)
    try:
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            raw = resp.read().decode("utf-8")
            try:
                return resp.status, json.loads(raw)
            except json.JSONDecodeError:
                return resp.status, raw
    except urllib.error.HTTPError as e:
        raw = e.read().decode("utf-8", errors="replace")
        try:
            return e.code, json.loads(raw)
        except json.JSONDecodeError:
            return e.code, raw


def http_form(url: str, data: dict, headers=None, timeout=30):
    """发 x-www-form-urlencoded 请求（OAuth token 端点用），返回 (status, parsed_or_text)。"""
    body = urllib.parse.urlencode(data).encode("utf-8")
    req_headers = {
        "User-Agent": BROWSER_UA,
        "Accept": "application/json",
        "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8",
        "Content-Type": "application/x-www-form-urlencoded",
    }
    if headers:
        req_headers.update(headers)
    req = urllib.request.Request(url, data=body, headers=req_headers, method="POST")
    try:
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            raw = resp.read().decode("utf-8")
            try:
                return resp.status, json.loads(raw)
            except json.JSONDecodeError:
                return resp.status, raw
    except urllib.error.HTTPError as e:
        raw = e.read().decode("utf-8", errors="replace")
        try:
            return e.code, json.loads(raw)
        except json.JSONDecodeError:
            return e.code, raw


def load_auth() -> dict:
    if AUTH_FILE.exists():
        try:
            return json.loads(AUTH_FILE.read_text("utf-8"))
        except (json.JSONDecodeError, OSError):
            return {}
    return {}


def save_auth(data: dict) -> None:
    AUTH_FILE.parent.mkdir(parents=True, exist_ok=True)
    AUTH_FILE.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", "utf-8")
    AUTH_FILE.chmod(0o600)


# ---------------------------------------------------------------- OAuth

def register_client() -> str:
    """动态注册公共客户端，返回 client_id。"""
    payload = {
        "client_name": CLIENT_NAME,
        "redirect_uris": [REDIRECT_URI],
        "grant_types": ["authorization_code", "refresh_token"],
        "response_types": ["code"],
        "token_endpoint_auth_method": "none",
    }
    status, resp = http_json("POST", REGISTER_URL, payload)
    if status not in (200, 201) or not isinstance(resp, dict) or "client_id" not in resp:
        log(f"客户端注册失败（HTTP {status}）：{resp}")
        sys.exit(1)
    return resp["client_id"]


def make_pkce() -> tuple[str, str]:
    verifier = secrets.token_urlsafe(64)  # 86 字符，符合 43~128
    challenge = b64url(hashlib.sha256(verifier.encode("ascii")).digest())
    return verifier, challenge


def token_is_expired(auth: dict) -> bool:
    expires_at = auth.get("expires_at")
    if not expires_at:
        return True
    return time.time() > float(expires_at) - 60  # 提前 60 秒续期


def refresh_token(auth: dict) -> dict:
    rt = auth.get("refresh_token")
    cid = auth.get("client_id")
    if not rt or not cid:
        log("没有 refresh_token，需要重新授权。")
        sys.exit(1)
    payload = {
        "grant_type": "refresh_token",
        "refresh_token": rt,
        "client_id": cid,
    }
    status, resp = http_form(TOKEN_URL, payload)
    if status not in (200, 201) or not isinstance(resp, dict) or "access_token" not in resp:
        log(f"令牌续期失败（HTTP {status}）：{resp}")
        sys.exit(1)
    return resp


def apply_token_response(auth: dict, resp: dict) -> dict:
    auth["access_token"] = resp["access_token"]
    if "refresh_token" in resp:
        auth["refresh_token"] = resp["refresh_token"]
    if "expires_in" in resp:
        auth["expires_at"] = time.time() + float(resp["expires_in"])
    else:
        auth.pop("expires_at", None)
    return auth


def get_valid_access_token() -> str:
    auth = load_auth()
    if not auth.get("access_token"):
        log("尚未授权，请先运行：python3 framesbase.py auth")
        sys.exit(1)
    if token_is_expired(auth):
        log("access_token 已过期，正在用 refresh_token 续期…")
        auth = apply_token_response(auth, refresh_token(auth))
        save_auth(auth)
    return auth["access_token"]


def auth_flow() -> None:
    auth = load_auth()

    client_id = auth.get("client_id")
    if not client_id:
        log("首次接入：动态注册客户端…")
        client_id = register_client()
        auth["client_id"] = client_id
        auth["redirect_uri"] = REDIRECT_URI
        save_auth(auth)

    verifier, challenge = make_pkce()
    state = secrets.token_urlsafe(16)

    params = {
        "response_type": "code",
        "client_id": client_id,
        "redirect_uri": REDIRECT_URI,
        "scope": SCOPES,
        "code_challenge": challenge,
        "code_challenge_method": "S256",
        "state": state,
    }
    auth_url = AUTHORIZE_URL + "?" + urllib.parse.urlencode(params)

    captured: dict = {}

    class Handler(BaseHTTPRequestHandler):
        def do_GET(self):
            parsed = urllib.parse.urlparse(self.path)
            if parsed.path == "/callback":
                qs = urllib.parse.parse_qs(parsed.query)
                captured["code"] = qs.get("code", [None])[0]
                captured["state"] = qs.get("state", [None])[0]
                captured["error"] = qs.get("error", [None])[0]
                body = (
                    "<html><meta charset='utf-8'><body style='font-family:sans-serif;padding:40px'>"
                    "<h2>授权完成</h2><p>可以关闭本页，回到编辑器继续。</p></body></html>"
                ).encode("utf-8")
                self.send_response(200)
                self.send_header("Content-Type", "text/html; charset=utf-8")
                self.send_header("Content-Length", str(len(body)))
                self.end_headers()
                self.wfile.write(body)
                threading.Thread(target=self.server.shutdown, daemon=True).start()
            else:
                self.send_response(404)
                self.end_headers()

    server = HTTPServer(("127.0.0.1", REDIRECT_PORT), Handler)
    server.timeout = AUTH_TIMEOUT_SECONDS

    log("即将打开浏览器完成 Framesbase 授权。")
    log("授权链接（若浏览器未自动打开，请手动复制打开）：")
    log("")
    log(auth_url)
    log("")
    webbrowser.open(auth_url)

    server.handle_request()  # 处理一次回调后由 handler 主动 shutdown

    if captured.get("error"):
        log(f"授权被拒绝或出错：{captured['error']}")
        sys.exit(1)
    code = captured.get("code")
    if not code:
        log("没有收到授权码（可能超时或浏览器未完成登录）。")
        sys.exit(1)
    if captured.get("state") != state:
        log("state 校验失败，授权流程异常，已中止。")
        sys.exit(1)

    log("正在换取令牌…")
    token_payload = {
        "grant_type": "authorization_code",
        "code": code,
        "redirect_uri": REDIRECT_URI,
        "client_id": client_id,
        "code_verifier": verifier,
    }
    status, resp = http_form(TOKEN_URL, token_payload)
    if status not in (200, 201) or not isinstance(resp, dict) or "access_token" not in resp:
        log(f"令牌换取失败（HTTP {status}）：{resp}")
        sys.exit(1)

    auth = apply_token_response(auth, resp)
    save_auth(auth)
    log("授权成功，凭证已保存到 " + str(AUTH_FILE))


# ---------------------------------------------------------------- MCP 调用

def mcp_request(method: str, params: dict | None, token: str | None) -> dict:
    payload = {
        "jsonrpc": "2.0",
        "id": secrets.token_hex(8),
        "method": method,
        "params": params or {},
    }
    headers = {"Accept": "application/json, text/event-stream"}
    if token:
        headers["Authorization"] = "Bearer " + token
    status, resp = http_json("POST", MCP_URL, payload, headers=headers, timeout=60)
    if status != 200:
        log(f"MCP 请求失败（HTTP {status}）：{resp}")
        sys.exit(1)
    if isinstance(resp, dict) and resp.get("error"):
        log(f"MCP 返回错误：{json.dumps(resp['error'], ensure_ascii=False)}")
        sys.exit(1)
    return resp.get("result", resp)


def initialize(token: str | None) -> dict:
    return mcp_request(
        "initialize",
        {
            "protocolVersion": PROTOCOL_VERSION,
            "capabilities": {},
            "clientInfo": {"name": CLIENT_NAME, "version": "1.0"},
        },
        token,
    )


def list_tools(token: str) -> list:
    initialize(token)
    result = mcp_request("tools/list", {}, token)
    return result.get("tools", [])


def call_tool(token: str, name: str, arguments: dict) -> dict:
    initialize(token)
    return mcp_request("tools/call", {"name": name, "arguments": arguments}, token)


# ---------------------------------------------------------------- 命令

def cmd_auth() -> None:
    auth_flow()


def cmd_status() -> None:
    auth = load_auth()
    if not auth:
        print("尚未授权。请运行：python3 framesbase.py auth")
        return
    cid = auth.get("client_id", "(无)")
    has_access = bool(auth.get("access_token"))
    exp = auth.get("expires_at")
    exp_s = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(exp)) if exp else "未知"
    expired = token_is_expired(auth) if exp else True
    print(f"客户端 client_id : {cid}")
    print(f"access_token     : {'已保存' if has_access else '无'}")
    print(f"过期时间         : {exp_s}")
    print(f"当前状态         : {'已过期（下次调用会自动续期）' if expired else '有效'}")
    if has_access:
        try:
            token = get_valid_access_token()
            tools = list_tools(token)
            print(f"可用工具数       : {len(tools)}")
            for t in tools:
                print(f"  - {t.get('name')}: {t.get('description', '')[:80]}")
        except SystemExit:
            pass


def cmd_tools() -> None:
    token = get_valid_access_token()
    tools = list_tools(token)
    print(json.dumps(tools, ensure_ascii=False, indent=2))


def cmd_call(name: str, args_json: str) -> None:
    token = get_valid_access_token()
    args = {}
    if args_json:
        try:
            args = json.loads(args_json)
        except json.JSONDecodeError:
            log("参数必须是合法 JSON，例如 '{\"query\":\"仪表盘\"}'")
            sys.exit(1)
    result = call_tool(token, name, args)
    print(json.dumps(result, ensure_ascii=False, indent=2))


# ---------------------------------------------------------------- 便捷命令

def _cards_from_result(result: dict) -> list:
    """从 tools/call 结果里抽出卡片列表（兼容 structuredContent 与纯文本两种返回）。"""
    sc = result.get("structuredContent")
    if isinstance(sc, dict) and isinstance(sc.get("cards"), list):
        return sc["cards"]
    content = result.get("content") or []
    for item in content:
        if item.get("type") == "text":
            try:
                data = json.loads(item["text"])
                if isinstance(data, dict) and isinstance(data.get("cards"), list):
                    return data["cards"]
            except json.JSONDecodeError:
                continue
    return []


def _print_cards(cards: list) -> None:
    if not cards:
        print("（空，没有命中的卡片）")
        return
    for c in cards:
        extra = c.get("deliverable") or ""
        access = c.get("access") or ""
        flags = f"[{access}]" if access else ""
        if extra:
            flags += f" <{extra}>"
        print(f"{c.get('id')}  {c.get('type','')}  {c.get('category','')}  {c.get('title','')}  {flags}")


def cmd_browse(argv: list[str]) -> None:
    args: dict = {}
    positional = []
    i = 0
    while i < len(argv):
        a = argv[i]
        if a == "--type" and i + 1 < len(argv):
            args["type"] = argv[i + 1]; i += 2
        elif a == "--limit" and i + 1 < len(argv):
            args["limit"] = int(argv[i + 1]); i += 2
        elif a == "--offset" and i + 1 < len(argv):
            args["offset"] = int(argv[i + 1]); i += 2
        else:
            positional.append(a); i += 1
    if positional:
        args["category"] = positional[0]
    token = get_valid_access_token()
    result = call_tool(token, "list_prompts", args)
    _print_cards(_cards_from_result(result))


def cmd_search(argv: list[str]) -> None:
    query = argv[0] if argv else ""
    args: dict = {"query": query}
    i = 1
    while i < len(argv):
        if argv[i] == "--limit" and i + 1 < len(argv):
            args["limit"] = int(argv[i + 1]); i += 2
        else:
            i += 1
    if len(query) < 2:
        log("search 至少需要 2 个字符。")
        sys.exit(1)
    token = get_valid_access_token()
    result = call_tool(token, "search_prompts", args)
    _print_cards(_cards_from_result(result))


def cmd_fetch(card_id: str) -> None:
    token = get_valid_access_token()
    result = call_tool(token, "get_prompt", {"id": card_id})
    content = result.get("content") or []
    for item in content:
        if item.get("type") == "text":
            text = item["text"]
            try:
                data = json.loads(text)
                if isinstance(data, dict) and "prompt" in data:
                    print(data["prompt"])
                else:
                    print(text)
            except json.JSONDecodeError:
                print(text)
            return
    print(json.dumps(result, ensure_ascii=False, indent=2))


def cmd_related(card_id: str, limit: int | None = None) -> None:
    args: dict = {"id": card_id}
    if limit:
        args["limit"] = limit
    token = get_valid_access_token()
    result = call_tool(token, "get_related_prompts", args)
    _print_cards(_cards_from_result(result))


def main(argv: list[str]) -> None:
    if not argv or argv[0] in ("-h", "--help", "help"):
        print(__doc__)
        return
    cmd = argv[0]
    if cmd == "auth":
        cmd_auth()
    elif cmd == "status":
        cmd_status()
    elif cmd == "tools":
        cmd_tools()
    elif cmd == "call":
        if len(argv) < 2:
            log("用法：python3 framesbase.py call <工具名> ['json参数']")
            sys.exit(1)
        cmd_call(argv[1], argv[2] if len(argv) > 2 else "{}")
    elif cmd == "browse":
        cmd_browse(argv[1:])
    elif cmd == "search":
        cmd_search(argv[1:])
    elif cmd == "fetch":
        if len(argv) < 2:
            log("用法：python3 framesbase.py fetch <卡片id>")
            sys.exit(1)
        cmd_fetch(argv[1])
    elif cmd == "related":
        if len(argv) < 2:
            log("用法：python3 framesbase.py related <卡片id> [--limit N]")
            sys.exit(1)
        limit = None
        if "--limit" in argv[2:]:
            idx = argv.index("--limit")
            if idx + 1 < len(argv):
                limit = int(argv[idx + 1])
        cmd_related(argv[1], limit)
    else:
        log(f"未知命令：{cmd}")
        print(__doc__)
        sys.exit(1)


if __name__ == "__main__":
    main(sys.argv[1:])
