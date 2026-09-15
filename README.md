# Codex 视频剪辑工作流

这里集中保存可复用的 Skills、安装清单、项目目录模板、特效规范和操作流程。个人视频工程、素材、动效库、旧版项目和缓存可以放在同一总文件夹中，但都由 Git 忽略，不会进入公开仓库。

克隆后的目录就是工作流根目录；除非用户另外明确要求，不提交、不推送，也不上传任何项目、素材或成片。

第一次使用从 [`00-先读我.md`](00-先读我.md) 开始。Codex 的机器入口是本地项目根目录下的 `.agents/skills/video-production-bootstrap/`。

## 工作流核心文件

- `00-先读我.md`：从下载到开始第一条视频的操作说明。
- `workflow.json`：Codex 读取的目录规划、素材入口、输出目录和阶段规则。
- `effects.json`：Codex 读取的画面状态、特效卡、切屏矩阵和组合规则。
- `特效与切屏规范.md`：开头动效、真人小窗、素材全屏、字幕和过程动效说明。
- `dependencies.json`：系统工具、账号、插件和外部 GitHub Skill 固定版本。
- `skills/video-editing-workflow/`：完整剪辑统一入口，串起 `video-use → video-shotcraft → Remotion`、字幕、包装、预览和 QA。
- `项目模板/`：每条新视频的空白项目配置与说明。
- `视频制作统一工作流.md`：阶段顺序的唯一入口；先补齐素材，再统一设计包装。
- `skills/video-packaging-structure/`：素材就绪后生成包装方案、公开身份素材表和特效映射的结构 Skill。
- `skills/ai-visual-director/`：视觉分析、动效规划和导演分镜。
- `skills/chatcut/`：需要可编辑工程时的交付流程。
- `skills/transcribe/`：可选的 OpenAI 转录流程。
- `tools/remotion-editor/`：通用的本地包装组件编辑器原型，用 `@remotion/player` 实时预览并保存 `video.config.json`。
- `THIRD_PARTY_NOTICES.md`：第三方来源和许可证。

本机的 `video-use` 位于 `skills/video-use/`；[`video-shotcraft`](https://github.com/Vincentwei1021/video-shotcraft) 由安装脚本按照 `dependencies.json` 中的固定 commit 管理。后者提供 Shotcraft 镜头配方、动态 Gallery、准确 demo TSX、Remotion 模板和音频资产；本工作流参考其镜头结构、运动语法、节奏和实现代码，并按每个用户的素材重新适配。

## 一键安装工作流 Skill

克隆后，在仓库根目录执行下面的命令，会把统一入口链接到 Codex，并安装 `dependencies.json` 中固定版本的 `video-use` 与 `video-shotcraft`：

```bash
git clone https://github.com/SuperYu-simiao/codex-video-production-workflow.git
cd codex-video-production-workflow
python3 .agents/skills/video-production-bootstrap/scripts/install_workflow.py --all
```

如果只需要先接入本仓库的统一 Skill，不安装外部依赖：

```bash
python3 .agents/skills/video-production-bootstrap/scripts/install_workflow.py --install
```

安装脚本不会安装 Homebrew、插件或凭据，不会复制视频素材，也不会覆盖已有的非 Skill 路径。安装后在 Codex 中直接说“使用 `$video-editing-workflow` 完成这条口播视频”，再提供当前项目路径即可。

## 可编辑包装组件编辑器

仓库根目录的 `tools/remotion-editor/` 是独立的本地编辑器，不绑定任何一期视频，也不包含私人素材。它支持切换素材槽位、修改标题、切换人物/素材布局、切换转场、调整特效强度、调整 PIP 大小和场景时间，并通过 `@remotion/player` 实时预览。点击“保存配置”会下载 `video.config.json`；接入具体视频时，把它放入该项目的 `05-Remotion工程/config/`。

启动方式：

```bash
cd tools/remotion-editor
npm install
npm run dev
```

这个编辑器负责包装参数，不替代口播精剪、转录和最终渲染审批。完整边界见 [`tools/remotion-editor/README.md`](tools/remotion-editor/README.md)。

## 快速开始

直接进入本地项目：

```bash
cd codex-video-production-workflow
```

在这个目录打开 Codex，然后说：

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

需要检查字幕结构时：

```bash
python3 .agents/skills/video-production-bootstrap/scripts/validate_subtitles.py \
  --srt '/绝对路径/当前项目/01-原始素材/05-文稿与字幕/字幕.srt'
```

## 每条视频新建一个项目

不要把素材放进 `skills/`、仓库根目录或其他人的示例目录。开始一条新视频时运行：

```bash
python3 .agents/skills/video-production-bootstrap/scripts/create_video_project.py \
  --name "产品功能演示"
```

项目会创建在 `本地项目/产品功能演示/`。`本地项目/` 已被 Git 忽略，只保留在本机。

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

总文件夹统一保存视频项目、旧项目、动效库和本地输出；它们保持原位，不因一条新视频迁移或删除。Codex 运行时先读取用户明确指定的当前项目 `project.json`，再只扫描该项目的 `01-原始素材/`，不枚举其他视频项目、旧项目或整个动效库。原始素材始终只读；转录、精剪、包装、预览和成片分别写入当前项目的 `02` 到 `07` 目录。

先按 [`视频制作统一工作流.md`](视频制作统一工作流.md) 读取当前项目根目录、与 `project.json` 同级的 Word 逐字稿，再盘点其他素材文件并输出补录清单；此阶段禁止读取或分析口播视频。Agent 按已授权范围保存公开图片、Logo、官网和 GitHub 截图；动态页面或真实操作由用户按链接与具体录法录制。素材齐备或用户明确接受缺项后，才读取包装 Skill、[`effects.json`](effects.json)、[`特效与切屏规范.md`](特效与切屏规范.md) 和 [AI剪辑参考会话沉淀](视觉规范与参考/AI剪辑参考会话沉淀.md)，一次性设计并锁定包装。

## 剪辑效率工具

工具位于 `.agents/skills/video-production-bootstrap/scripts/`：

- `create_short_proxy.py`：原片只读，只转码明确的 `--start` 到 `--end` 区间，默认输出到当前项目 `03-精剪输出/代理片段/`；每个代理有 `.proxy.json` 回连清单。
- `batch_extract_frames.py`：从已存在预览用一次 FFmpeg 进程抽取多个 `--time`，输出到 `06-预览与审核/关键帧/` 并生成 JSON 索引；不会启动 Remotion。
- `check_render_processes.py`：只列出命令或工作目录关联当前项目路径的 Remotion、FFmpeg、Chromium、渲染 Node 进程；完全只读，不提供终止功能。

前两个工具默认 dry-run，必须显式添加 `--execute` 才会写当前项目。三者都必须传 `--project`，且生成代理、抽帧、查进程不等于剪辑、预览渲染、最终渲染或结束进程授权。完整命令见 [`00-先读我.md`](00-先读我.md)。

## 排除机制

`.gitignore` 只控制 Git；仓库根和新项目中的 `.vscode/settings.json` 才使用 VS Code 原生 watcher/search 排除；新项目 `05-Remotion工程/remotion.config.ts` 使用 Remotion 官方 Webpack override 设置当前项目的 `watchOptions.ignored`。Node 没有通用 watcher 排除项，因此运行入口限定在当前项目的 `05-Remotion工程/`，共享动效库只按当前项目明确引用进入依赖图，不做整库扫描。

## 设备与账号

| 类别 | 要求 |
|---|---|
| 设备 | 现代 Mac 或 PC；建议 16 GB 内存和 30 GB 可用空间 |
| 系统工具 | Git、Node.js 22+、npm、Python 3.10+、uv、FFmpeg/ffprobe |
| 必需账号 | Codex；GitHub 账号仅在 fork、提交或推送时需要 |
| 可选转录 | ElevenLabs API Key 或 OpenAI API Key；已有转录时可以不调用 API |
| Codex 插件 | Remotion；ChatCut 仅在需要可编辑工程时使用 |

API Key 只放在本机环境变量或未提交的 `.env`，可参考 `.env.example`。完整版本、来源和用途以 `dependencies.json` 为准。

## 本地使用边界

默认不提交、不推送、不上传。`视频项目/`、`旧版项目/`、`本地项目/`、`动效库/`、`视觉规范与参考/`、原片、录屏、转录、成片、`.env`、凭据、第三方项目副本、插件缓存、`node_modules` 和渲染缓存均由 Git 忽略并保留在本机。
