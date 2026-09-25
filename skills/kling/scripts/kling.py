#!/usr/bin/env python3
"""可灵 Kling 图生视频 CLI —— 把本地照片变成电影级运镜视频。

用法:
  python3 kling.py auth <API_KEY>                                # 保存 API key（一次性）
  python3 kling.py submit -i cat.jpg -p "提示词" [-d 10] [-r 1080p]   # 提交图生视频任务
  python3 kling.py status <task_id>                              # 查询任务状态
  python3 kling.py wait <task_id> [-o out.mp4]                   # 轮询直到完成并下载
  python3 kling.py gen -i cat.jpg -p "提示词" [-o out.mp4]        # 一条龙：提交+轮询+下载

纯 Python 标准库实现，无第三方依赖。
"""
import argparse
import base64
import json
import os
import sys
import time
import urllib.error
import urllib.request

BASE = "https://api-beijing.klingai.com"
UA = ("Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
      "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0 Safari/537.36")
AUTH = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "auth.json")


def load_key():
    if not os.path.exists(AUTH):
        sys.exit("未配置 API key：先运行  kling.py auth <API_KEY>")
    with open(AUTH, "r", encoding="utf-8") as f:
        d = json.load(f)
    key = d.get("api_key", "").strip()
    if not key:
        sys.exit("auth.json 里没有 api_key")
    return key


def http(method, url, token=None, body=None):
    headers = {"User-Agent": UA}
    data = None
    if body is not None:
        data = json.dumps(body, ensure_ascii=False).encode("utf-8")
        headers["Content-Type"] = "application/json"
    if token:
        headers["Authorization"] = "Bearer " + token
    req = urllib.request.Request(url, data=data, headers=headers, method=method)
    try:
        with urllib.request.urlopen(req, timeout=60) as r:
            return json.loads(r.read().decode("utf-8"))
    except urllib.error.HTTPError as e:
        try:
            return json.loads(e.read().decode("utf-8") or "{}")
        except Exception:
            return {"code": e.code, "message": "HTTP %s" % e.code}
    except Exception as e:
        sys.exit("请求失败: %s" % e)


def img_b64(path):
    if not os.path.exists(path):
        sys.exit("图片不存在: %s" % path)
    with open(path, "rb") as f:
        return base64.b64encode(f.read()).decode("ascii")


def download(url, out):
    # 防盗链 URL 需带 UA + Referer
    headers = {"User-Agent": UA, "Referer": BASE + "/"}
    req = urllib.request.Request(url, headers=headers)
    with urllib.request.urlopen(req, timeout=120) as r, open(out, "wb") as f:
        f.write(r.read())


def cmd_auth(args):
    os.makedirs(os.path.dirname(AUTH), exist_ok=True)
    with open(AUTH, "w", encoding="utf-8") as f:
        json.dump({"api_key": args.key.strip()}, f)
    os.chmod(AUTH, 0o600)
    print("已保存 API key ->", AUTH)


def build_body(image_path, prompt, duration, resolution):
    contents = [
        {"type": "prompt", "text": prompt},
        {"type": "first_frame", "url": img_b64(image_path)},
    ]
    return {
        "contents": contents,
        "settings": {
            "resolution": resolution,
            "duration": duration,
            "audio": "off",
            "multi_shot": False,
        },
        "options": {"watermark_info": {"enabled": False}},
    }


def cmd_submit(args):
    token = load_key()
    body = build_body(args.image, args.prompt, args.duration, args.resolution)
    r = http("POST", BASE + "/image-to-video/kling-3.0", token, body)
    print(json.dumps(r, ensure_ascii=False, indent=2))
    if r.get("code") == 0:
        print("\n任务ID:", r["data"]["id"])
    else:
        sys.exit(1)


def cmd_status(args):
    token = load_key()
    r = http("GET", BASE + "/tasks?task_ids=" + args.task_id, token)
    print(json.dumps(r, ensure_ascii=False, indent=2))


def cmd_wait(args):
    token = load_key()
    tid = args.task_id
    while True:
        r = http("GET", BASE + "/tasks?task_ids=" + tid, token)
        if r.get("code") != 0 or not r.get("data"):
            print(json.dumps(r, ensure_ascii=False, indent=2))
            sys.exit(1)
        t = r["data"][0]
        st = t.get("status")
        print("[%s] 状态: %s" % (time.strftime("%H:%M:%S"), st), flush=True)
        if st == "succeeded":
            out = t.get("outputs", [{}])[0].get("url", "")
            if not out:
                sys.exit("任务成功但未返回视频 url")
            dest = args.out or (tid + ".mp4")
            print("下载中 ->", dest, flush=True)
            download(out, dest)
            print("完成:", dest)
            return
        if st == "failed":
            print("生成失败:", t.get("message"))
            sys.exit(1)
        time.sleep(args.poll)


def cmd_gen(args):
    token = load_key()
    body = build_body(args.image, args.prompt, args.duration, args.resolution)
    r = http("POST", BASE + "/image-to-video/kling-3.0", token, body)
    if r.get("code") != 0:
        print(json.dumps(r, ensure_ascii=False, indent=2))
        sys.exit(1)
    tid = r["data"]["id"]
    print("已提交，任务ID:", tid, flush=True)
    # 复用 wait 逻辑
    import types
    ns = types.SimpleNamespace(task_id=tid, out=args.out, poll=args.poll)
    cmd_wait(ns)


def main():
    p = argparse.ArgumentParser(description="可灵 Kling 图生视频 CLI")
    sub = p.add_subparsers(dest="cmd", required=True)

    a = sub.add_parser("auth", help="保存 API key")
    a.add_argument("key")
    a.set_defaults(fn=cmd_auth)

    s = sub.add_parser("submit", help="提交图生视频任务")
    s.add_argument("-i", "--image", required=True)
    s.add_argument("-p", "--prompt", required=True)
    s.add_argument("-d", "--duration", type=int, default=10, choices=range(3, 16))
    s.add_argument("-r", "--resolution", default="1080p", choices=["720p", "1080p", "4k"])
    s.set_defaults(fn=cmd_submit)

    t = sub.add_parser("status", help="查询任务")
    t.add_argument("task_id")
    t.set_defaults(fn=cmd_status)

    w = sub.add_parser("wait", help="轮询直到完成并下载")
    w.add_argument("task_id")
    w.add_argument("-o", "--out", default=None)
    w.add_argument("--poll", type=int, default=10)
    w.set_defaults(fn=cmd_wait)

    g = sub.add_parser("gen", help="一条龙：提交+轮询+下载")
    g.add_argument("-i", "--image", required=True)
    g.add_argument("-p", "--prompt", required=True)
    g.add_argument("-d", "--duration", type=int, default=10, choices=range(3, 16))
    g.add_argument("-r", "--resolution", default="1080p", choices=["720p", "1080p", "4k"])
    g.add_argument("-o", "--out", default=None)
    g.add_argument("--poll", type=int, default=10)
    g.set_defaults(fn=cmd_gen)

    args = p.parse_args()
    args.fn(args)


if __name__ == "__main__":
    main()
