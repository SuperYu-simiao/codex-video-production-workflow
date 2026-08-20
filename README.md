# Codex 视频剪辑工作流

这里公开的是可复用的 Skills、安装清单、项目目录模板、特效规范和操作流程，不包含作者自己的视频工程、原片、录屏、转录、成片、旧版项目、私人风格参考或本机插件缓存。

第一次使用从 [`00-先读我.md`](00-先读我.md) 开始。Codex 的机器入口是仓库根目录下的 `.agents/skills/video-production-bootstrap/`。

## 公开内容

- `00-先读我.md`：从下载到开始第一条视频的操作说明。
- `workflow.json`：Codex 读取的目录规划、素材入口、输出目录和阶段规则。
- `effects.json`：Codex 读取的画面状态、特效卡、切屏矩阵和组合规则。
- `特效与切屏规范.md`：开头动效、真人小窗、素材全屏、字幕和过程动效说明。
- `dependencies.json`：系统工具、账号、插件和外部 GitHub Skill 固定版本。
- `项目模板/`：每条新视频的空白项目配置与说明。
- `skills/ai-visual-director/`：视觉分析、动效规划和导演分镜。
- `skills/chatcut/`：需要可编辑工程时的交付流程。
- `skills/transcribe/`：可选的 OpenAI 转录流程。
- `THIRD_PARTY_NOTICES.md`：第三方来源和许可证。

`video-use` 与 [`video-shotcraft`](https://github.com/Vincentwei1021/video-shotcraft) 不复制进仓库，由安装脚本按照 `dependencies.json` 中的固定 commit 下载。后者提供 Shotcraft 镜头配方、动态 Gallery、准确 demo TSX、Remotion 模板和音频资产；本工作流参考其镜头结构、运动语法、节奏和实现代码，并按每个用户的素材重新适配。

## 快速开始

克隆仓库：

```bash
git clone https://github.com/SuperYu-simiao/codex-video-production-workflow.git
cd codex-video-production-workflow
```

在仓库根目录打开 Codex，然后说：

```text
请读取 00-先读我.md、workflow.json 和 dependencies.json，
先检查视频工作流环境。
不要安装、剪辑或渲染，先告诉我缺少什么。
```

只读环境检查：

```bash
python3 .agents/skills/video-production-bootstrap/scripts/check_dependencies.py
```

得到明确授权后安装外部 Skills：

```bash
python3 .agents/skills/video-production-bootstrap/scripts/install_dependencies.py --install
```

## 每条视频新建一个项目

不要把素材放进 `skills/`、仓库根目录或其他人的示例目录。开始一条新视频时运行：

```bash
python3 .agents/skills/video-production-bootstrap/scripts/create_video_project.py \
  --name "产品功能演示"
```

项目会创建在 `本地项目/产品功能演示/`。`本地项目/` 已被 Git 忽略，不会随着工作流上传。

创建后，把文件放入：

```text
01-原始素材/
├── 01-口播视频/
├── 02-录屏/
├── 03-图片与截图/
├── 04-音频/
├── 05-文稿与字幕/
├── 06-授权说明/
└── 07-背景与动效素材/
```

Codex 运行时先读取当前项目的 `project.json`，再只扫描当前项目的 `01-原始素材/`。原始素材始终只读；转录、精剪、包装、预览和成片分别写入 `02` 到 `07` 的目录。

制作包装时，Codex 还会读取 [`effects.json`](effects.json) 和 [`特效与切屏规范.md`](特效与切屏规范.md)：产品名和章节标题进入黑灰科技网格标题舞台；录屏、截图和图片铺满主画面；真人口播缩到右下角；字幕始终放在主画面；任何画面状态变化都使用与语义匹配的转场。

## 设备与账号

| 类别 | 要求 |
|---|---|
| 设备 | 现代 Mac 或 PC；建议 16 GB 内存和 30 GB 可用空间 |
| 系统工具 | Git、Node.js 22+、npm、Python 3.10+、uv、FFmpeg/ffprobe |
| 必需账号 | Codex；GitHub 账号仅在 fork、提交或推送时需要 |
| 可选转录 | ElevenLabs API Key 或 OpenAI API Key；已有转录时可以不调用 API |
| Codex 插件 | Remotion；ChatCut 仅在需要可编辑工程时使用 |

API Key 只放在本机环境变量或未提交的 `.env`，可参考 `.env.example`。完整版本、来源和用途以 `dependencies.json` 为准。

## 发布边界

可以上传：工作流文档、JSON 清单、项目模板、repo Skills、安装与检查脚本、许可证声明。

不要上传：`视频项目/`、`旧版项目/`、`本地项目/`、`动效库/`、`视觉规范与参考/`、原片、录屏、转录、成片、`.env`、凭据、第三方仓库副本、插件缓存、`node_modules` 和渲染缓存。

本机原有内容不会被删除，只会被 Git 忽略。正式提交前仍须逐项检查 staged diff，禁止使用 `git add -A` 或 `git add .`。
