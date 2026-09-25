---
name: framesbase
description: 查询 Framesbase 私人设计资料库（远程 MCP，OAuth 授权）。按分类/类型列出网站·应用·区块设计卡片、按标题/分类名搜索、取某张卡的 prompt 正文、找同分类同类卡片。当用户要查或复用 Framesbase 里的设计参考/设计 prompt，或想把这些网站/应用/区块设计用在视频包装、画面、网页搭建时使用。
---

# Framesbase 设计资料库接入

Framesbase 是用户的私人设计资料库（`https://app.framesbase.app`），对外暴露一个无状态 HTTP MCP 端点。本技能是它的本地客户端，替 pi 完成 OAuth 授权并调用其工具。

## 先认清它是什么（避免误用）

- 库里的卡片是**网站 / 应用 / 区块（sites / apps / sections）的设计 prompt**，交付物通常是「一段 prompt，用来生成单个自包含 HTML 页面」，少数是仓库或在线应用链接。
- **它不是视频特效库**。视频特效/动效仍走 `effects.json` 与 `动效库/`，本库只在需要「网页/应用界面画面、UI 设计参考、产品演示里的界面」这类素材时用。
- 搜索只命中**标题与分类名**，不搜 prompt 正文，也不是语义搜索：按「深色」「极简」搜，命中的是名字里真有这词的卡片；空结果 = 这些词没出现在标题/分类里，不等于库里没有相关主题。
- `get_prompt`（取正文）需要会员；卡片交付物是仓库/链接时，返回的是那个链接而不是正文。

## 用法

脚本在 `scripts/framesbase.py`（仅用 Python 标准库，无第三方依赖）。凭证存在 `skills/framesbase/auth.json`，已被仓库 `.gitignore` 排除，绝不进 git。

```bash
# 首次接入（浏览器授权一次，之后自动用 refresh_token 续期）
python3 skills/framesbase/scripts/framesbase.py auth

# 查看凭证状态与可用工具
python3 skills/framesbase/scripts/framesbase.py status

# 按分类/类型列卡片
python3 skills/framesbase/scripts/framesbase.py browse SaaS --limit 20
python3 skills/framesbase/scripts/framesbase.py browse SaaS --type sections --offset 20

# 按标题/分类名搜索（至少 2 个字符）
python3 skills/framesbase/scripts/framesbase.py search dashboard --limit 20

# 取某张卡的 prompt 正文（需要会员）
python3 skills/framesbase/scripts/framesbase.py fetch <卡片id>

# 同分类同类卡片
python3 skills/framesbase/scripts/framesbase.py related <卡片id> --limit 12

# 调用任意工具（工具名见 status 或 tools）
python3 skills/framesbase/scripts/framesbase.py call search_prompts '{"query":"hero"}'
```

卡片输出形如：`<id>  <type>  <category>  <title>  [access] <deliverable>`。

## 注意事项

- **限流**：Framesbase 对 MCP 调用有分钟级限流，不要一次批量猛查；按需查询，命中哪张再 `fetch` 哪张。
- **授权失效**：access_token 过期会脚本自动续期；若 refresh_token 也失效，重新跑一次 `auth`（浏览器再点一次同意）。
- 凭证文件 `auth.json` 属于密钥，不要读取内容回显给用户，也不要提交。
