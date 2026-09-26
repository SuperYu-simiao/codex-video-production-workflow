# AI 视频制作工作流

把你对着镜头拍的一段口播视频交给 Codex，自动走完「逐字稿盘点 → 补录清单 → 素材收集 → 统一包装 → 精剪 → 动效 → Remotion 合成 → 成片」的全流程。

这个仓库是可分享、可复用的完整工作流：流程规则、动效库、特效模板、制作经验，以及内置的 `video-use` 和 `video-shotcraft` 技能都打包在里面，克隆下来就能用，不需要额外联网下载。

---

## 第一次使用（装好环境，做一次就行）

### 1. 装好工具和 Codex

| 工具 | Mac 安装命令 | 说明 |
|---|---|---|
| Git | 系统自带 | 用来下载仓库 |
| Node.js 22+ | `brew install node@22` | Remotion 渲染需要 |
| Python 3.10+ | `brew install python` | 流程脚本需要 |
| uv | `brew install uv` | Python 依赖管理 |
| FFmpeg | `brew install ffmpeg` | 视频处理 |

> 没有 `brew` 的话先去 https://brew.sh 装。Windows 用户到各工具官网下载安装包。

再装好 **Codex**（OpenAI 的编码助手，本工作流就靠它驱动），并在 Codex 插件里搜索安装 **Remotion** 插件。

### 2. 克隆仓库并一键安装

```bash
git clone https://github.com/SuperYu-simiao/codex-video-production-workflow.git
cd codex-video-production-workflow
python3 .agents/skills/video-production-bootstrap/scripts/install_workflow.py --all
```

> 安装脚本复用仓库内置的技能，离线可用，不会碰你的素材和凭据。

### 3. 检查环境缺什么（可选）

```bash
python3 .agents/skills/video-production-bootstrap/scripts/check_dependencies.py
```

它会列出还缺哪些工具/插件。可选账号：需要 API 转录时才准备 ElevenLabs 或 OpenAI 的 API Key，已有字幕可跳过。

---

## 开始做一条视频（每次的流程）

### 1. 新建一个项目

```bash
python3 .agents/skills/video-production-bootstrap/scripts/create_video_project.py --name "你的视频名字"
```

项目会创建在 `本地项目/你的视频名字/`（这个目录不会被提交到仓库）。

### 2. 把你的素材放进去

把原始素材放进项目里的 `01-原始素材/` 对应子目录：

```text
本地项目/你的视频名字/01-原始素材/
├── 01-口播视频/   ← 你对着镜头拍的视频放这里
├── 02-录屏/       ← 产品操作、网页演示录屏
├── 03-图片与截图/ ← 产品图、截图、照片
├── 04-音频/       ← 独立录音、音乐、音效
├── 05-文稿与字幕/ ← 口播稿、Word 逐字稿、已有字幕
├── 06-授权说明/   ← 素材来源和授权说明（可选）
└── 07-背景与动效素材/
```

### 3. 打开 Codex 开工

在仓库根目录打开 Codex，对它说：

```text
使用 $video-editing-workflow 完成这条口播视频，项目是「本地项目/你的视频名字」
```

> 更详细的启动提示词见 [`docs/00-先读我.md`](docs/00-先读我.md)，可以直接照抄。

### 4. 跟着 Codex 的流程走

Codex 会按固定流程推进，**每个关键节点都会停下来等你确认**，不会自己一路做完：

1. **读逐字稿、盘点素材**：先读你的 Word 逐字稿，只盘素材不碰你的口播视频
2. **出补录清单**：告诉你还缺什么、怎么补、去哪录
3. **收集素材**：能下载的公开图它自己下；需要动态录屏的，它给你链接和录法，你自己录
4. **统一设计包装**：开头动效、真人小窗、转场、特效一次性设计好，你确认锁定
5. **精剪对齐字幕**
6. **加动效**
7. **Remotion 合成渲染**
8. **先出小样给你看 → 你确认 → 出成片**

你的口播原片全程只读，不会被改动。

---

## 仓库里有什么

- `skills/`：剪辑工作流 + 内置的 `video-use`、`video-shotcraft`
- `memory/`：沉淀的制作经验和剪辑规则（越用越聪明）
- `动效库/`：特效模板和动效注册表
- `workflow.json`、`effects.json`、`特效与切屏规范.md`：流程与特效规则
- `项目模板/`：每条新视频的空白配置
- `tools/remotion-editor/`：包装组件编辑器（可选，实时预览调包装）
- `docs/00-先读我.md`：详细操作手册

## 使用边界

- 仓库分享的是**方法**，不含任何私人素材：口播原片、转录、成片都不在里面
- 你的视频项目放在本地 `本地项目/`，被 Git 忽略，不会上传
- API 密钥只放本机环境变量，绝不进仓库
- 原始素材只读，所有生成物写入各阶段目录

## 第三方来源与许可

外部技能和素材来源见 `THIRD_PARTY_NOTICES.md`。
