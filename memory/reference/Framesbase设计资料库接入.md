---
name: framesbase-设计资料库接入
description: Framesbase 私人设计资料库 MCP 已接入（本地客户端脚本），是网站/应用/区块设计 prompt 库而非视频特效库；搜索只命中标题/分类名。要查/复用 Framesbase 设计参考时读。
type: reference
---

## 涉及文件
- `skills/framesbase/scripts/framesbase.py`（本地 MCP 客户端：OAuth 授权 + 调用工具）
- `skills/framesbase/SKILL.md`（用法与注意事项）
- `skills/framesbase/auth.json`（OAuth 凭证，已被 `.gitignore` 的 `**/auth.json` 排除，绝不进 git）

## 必保行为
1. **Framesbase 是 Web/UI 设计 prompt 库，不是视频特效库**。卡片是 sites/apps/sections 三类，交付物是「生成单页 HTML 的 prompt」或仓库/链接。视频特效/动效仍走 `effects.json` 与 `动效库/`，不要把它当特效库用。
2. **search_prompts 只搜标题与分类名**，不搜 prompt 正文、非语义搜索；空结果 = 词没出现在标题/分类里，不等于库里没有该主题（官方 instructions 明确要求：空结果就照实说，别声称库里没相关内容）。
3. **get_prompt 需要会员**；交付物为仓库/在线应用时返回链接而非正文。
4. **限流**：MCP 调用有分钟级限流，按需查询、命中再 fetch，不批量猛查。
5. 凭证在 `auth.json`，属于密钥：不读取回显、不提交；access_token 过期脚本自动用 refresh_token 续期，refresh 也失效就重跑 `auth`。

## 回归测试
```bash
python3 skills/framesbase/scripts/framesbase.py status
python3 skills/framesbase/scripts/framesbase.py search dashboard --limit 3
```

来源：2026-09-17 用户要求接入 framesbase MCP（app.framesbase.app/mcp）。排查接入时踩到两个外部系统坑并已写进脚本：① OAuth token 端点被 Cloudflare「浏览器签名」规则拦截，需用浏览器 User-Agent；② token 端点只接受 x-www-form-urlencoded，发 JSON 会报 `client_id is required`。
