# AI 视频制作工作流

把你对着镜头拍的一段口播视频交给 Codex，自动走完「逐字稿盘点 → 补录清单 → 素材收集 → 统一包装 → 精剪 → 动效 → Remotion 合成 → 成片」的全流程。

这个仓库是可分享、可复用的完整工作流：流程规则、动效库、特效模板、制作经验，以及内置的 `video-use` 和 `video-shotcraft` 技能都打包在里面，克隆下来就能用，不需要额外联网下载。

## 三步上手

```bash
# 1. 克隆仓库
git clone https://github.com/SuperYu-simiao/codex-video-production-workflow.git
cd codex-video-production-workflow

# 2. 一键安装（复用仓库内置技能，离线可用）
python3 .agents/skills/video-production-bootstrap/scripts/install_workflow.py --all

# 3. 在这个目录打开 Codex，对它说：
#    「使用 $video-editing-workflow 完成这条口播视频」
#    然后告诉它你的视频项目路径
```

> 第一次用建议先跑只读检查，看环境缺什么：
> `python3 .agents/skills/video-production-bootstrap/scripts/check_dependencies.py`

## 开工前准备

| 类别 | 要求 |
|---|---|
| 设备 | 现代 Mac 或 PC，建议 16 GB 内存、30 GB 可用空间 |
| 系统工具 | Git、Node.js 22+、npm、Python 3.10+、uv、FFmpeg |
| Codex 插件 | Remotion（必装） |
| 可选 | ElevenLabs 或 OpenAI 的 API Key，仅在使用 API 转录时才需要；已有字幕可跳过 |

完整版本和来源以 `dependencies.json` 为准。

## 新建一条视频

```bash
python3 .agents/skills/video-production-bootstrap/scripts/create_video_project.py --name "你的视频名字"
```

项目会建在 `本地项目/你的视频名字/`（该目录不进仓库）。把你的口播视频、录屏、图片、音频放进 `01-原始素材/` 的对应子目录，然后在 Codex 里开始即可。

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
