# GitHub 开源 AI 视频动效与画面参考（补充）

> 核查日期：2026-08-23。以下仓库是本次新增筛选，不重复已有的 `remotion-scenes`、`Remocn/remocn`、`video-shotcraft`、`Curvable/motion`、`pixel2motion` 和 `clippkit`。
>
> 筛选标准：公开仓库、许可证可确认、存在可读源码或真实示例、能对应当前工作流的标题/字幕/UI/转场/背景/画面状态。仓库中的 demo 画面只作为运动机制参考，不能默认当作本项目素材。

## 一、可以直接改代码的动效库

| 仓库 | 许可证 | 最适合参考的内容 | 现有工作流的落点 |
|---|---|---|---|
| [snapcndev/snapcn](https://github.com/snapcndev/snapcn) | MIT | 21 个 Remotion 组件：`answer-stream`、`search-typing`、`prompt-zoom`、手机/电脑/终端框、`text-reveal`、`text-build`、`text-swap`、`karaoke-captions`、`hero-launch`、`orbit-gallery`、`logo-assemble` 等。源码按 shadcn 思路复制进项目，可直接替换主题和 props。 | **优先级最高。** 对应 `title-stage`、`code-prompt-stage`、`material-fullscreen`、字幕和产品演示。优先研究 `components/snap-cn/` 与 `content/docs/` 的组件实现。 |
| [fand/vfx-js](https://github.com/fand/vfx-js) | MIT | WebGL 后期效果，可挂到图片或视频；内置 `glitch`、`bloom`、`datamosh`、`dither`、`fluid`、`halftone`、`light-streak`、`matrix`、`pixelate`、`scanline`、`rgb-shift`、`vignette`、`voronoi` 等。 | 对应 `glitch-displace`、`scanline-annotate-focus`、`flash-cut` 和黑灰科技舞台的短时叠加层。先抽离 shader/参数，再适配 Remotion 或 HyperFrames；不要在阅读录屏时持续施加。 |
| [motion-canvas/motion-canvas](https://github.com/motion-canvas/motion-canvas) | MIT | TypeScript 生成器动画 + 实时编辑器，专门支持信息图、矢量图解和旁白同步；自带 `Grid`、`CodeBlock`、`Txt`、`Camera`、`Video`、路径和基础转场。 | 对应技术解释、流程图、模型/数据管线、章节桥接。重点看 `packages/2d/src/lib/components/`、`packages/core/src/transitions/` 和 `packages/create/template-2d-ts/`。它是独立于 Remotion 的实现参考，不要未经适配直接混进现有工程。 |
| [remotion-dev/template-three](https://github.com/remotion-dev/template-three) | MIT（仓库；Remotion 依赖另有条款） | 极简 Remotion + React Three Fiber 模板，含 `Phone`、`RoundedBox`、`Scene`、手机/平板视频纹理和 3D 镜头示例。 | 对应手机/设备登场、产品界面空间化、`basic-3d-scene` 和 `neon-frame-orbit-drop`。重点看 `src/Phone.tsx`、`src/Scene.tsx`、`src/RoundedBox.tsx`。 |
| [stefanwittwer/remotion-animated](https://github.com/stefanwittwer/remotion-animated) | MIT | Remotion 的小型动画抽象：`Fade`、`Move`、`Rotate`、`Scale`、`Size`，带 spring/ease/custom easing 和组合式组件。 | 对应真人全屏↔PIP、标题卡入场、卡片落定和可控的缓动曲线。重点看 `packages/remotion-animated/src/animations/` 与 `src/easing/`。维护节奏较慢，适合读实现和复制局部模式。 |

## 二、背景、粒子和后期画面参考

| 仓库 | 许可证 | 可以借鉴的画面机制 | 使用边界 |
|---|---|---|---|
| [astrofox-io/astrofox](https://github.com/astrofox-io/astrofox) | MIT | 本地音频驱动的 motion-graphics 程序；示例插件包含 `audio-orb`、`bass-glow`、`cubes`、`plasma`、`pulse-bars`，源码还有频谱、波形、径向频谱、隧道、网格和 3D 几何层。 | 适合片头音乐桥、节奏蒙太奇和抽象科技背景。重点看 `examples/plugins/`、`src/lib/canvas/`、`src/lib/audio/`、`src/lib/core/render/geometry/`。它是独立桌面/网页工具，先借视觉和参数，不假定能直接导入 Remotion。 |
| [williamngan/pts](https://github.com/williamngan/pts) | Apache-2.0 | Creative-coding 几何库，包含大量可读 demo：Delaunay、噪声点、Bezier、文字框、图片像素、声音频率、节奏和 stagger。 | 适合自建透视网格、点阵、线稿、数据场和轻量音频反应层。重点看 `demo/guide.sound_*`、`demo/guide.tempo_*`、`demo/create.delaunay.js`、`demo/create.noisePts.js`。需要自己补视频帧输出。 |
| [tsparticles/tsparticles](https://github.com/tsparticles/tsparticles) | MIT | 兼容 React/Vue/Svelte 等的粒子系统；内置 `ambient`、`hyperspace`、`links`、`fireworks`、`stars`、`bubbles` 等 preset，也有粒子遮罩和字符粒子教程。 | 适合低对比度粒子背景、星点/连线、章节标题的环境层。优先看 preset 和 demo，不要让粒子层压过人物、字幕或真实 UI；在当前工作流中需先做成可控的离线/透明层。 |
| [theatre-js/theatre](https://github.com/theatre-js/theatre) | Core Apache-2.0；Studio AGPL-3.0 | 面向 Web 的高保真 motion-design editor，支持 3D 对象、HTML/SVG、微交互和生成艺术；适合观察关键帧曲线、空间编排和镜头节奏。 | 作为“怎么调运动曲线”的参考，不列为当前首选运行时。`@theatre/core` 与编辑用 `@theatre/studio` 许可证不同，复制代码或发布工具前必须单独审核。仓库最近公开提交较早，优先读文档和示例。 |

## 三、AI 剪辑与可编辑时间线的实现参考

| 仓库 | 许可证 | 值得看的能力 | 适合怎么用 |
|---|---|---|---|
| [0xsline/OpenChatCut](https://github.com/0xsline/OpenChatCut) | AGPL-3.0 | 本地优先、可编辑多轨时间线、Agent/MCP、Remotion、字幕、模板、WebGL motion graphics、shader 转场、LUT、缩放和音效库；源码里有 `page-curl`、`glitch-cut`、`whip-pan`、`circle-wipe` 等 shader/transition。 | 研究“AI 指令如何落成真实轨道、转场、字幕和可撤销工程”。它不是 MIT，若要拷贝代码进闭源项目，先做 AGPL 合规判断；README 里的音效和截图也要按各自来源处理。 |
| [notivn/AIEV](https://github.com/notivn/AIEV) | MIT | Claude 导演 → HyperFrames（HTML + GSAP 动效）→ Remotion 时间线；包含 kinetic typography、karaoke subtitle、beat-sync zoom、SFX、style kit、调色 preset 和完整转场参考文档。 | 研究与你当前 HyperFrames/Remotion 双后端最接近的自动包装流程。重点看 `.claude/skills/hyperframes/references/transitions/`、`palettes/`、`engines/remotion/src/components/`。生成图片仍可能需要 Gemini 等外部密钥，不能把“MIT”理解成所有运行依赖都免费。 |
| [Orkas-AI/Orkas-VideoStudio](https://github.com/Orkas-AI/Orkas-VideoStudio) | MIT | 用可读、可 diff、可重渲染的 `plan.json` 表达 Compose/Edit/Generate/Auto；Compose/Edit 走 HyperFrames、FFmpeg、Whisper.cpp，带阶段化 skills 和 delivery guard。 | 研究“素材、旁白、字幕、动效、生成片段如何被一个计划串起来”，尤其适合完善当前项目的阶段门和可审计产物。生成能力采用 BYO provider key；只看架构和 plan，不要默认安装或运行。 |

## 四、按当前工作流的推荐顺序

1. **先看 `snapcn`**：直接补齐 AI 输入框、搜索、终端、设备框、标题和逐字字幕，最容易映射到现有 `title-stage` / `code-prompt-stage`。
2. **再看 `vfx-js`**：挑一个短时 `glitch`、`scanline`、`pixelate` 或 `light-streak`，做成可控的 2–6 帧转场层。
3. **需要技术图解时看 `motion-canvas`**：借它的 `Grid`、`CodeBlock`、路径和旁白同步思路，输出仍放在当前项目自己的 Remotion 工程。
4. **需要空间感时看 `template-three`**：从手机/平板 3D 镜头开始，不要先做复杂全场景。
5. **需要背景气氛时看 `Astrofox` + `Pts` / `tsParticles`**：先确定语义和字幕安全区，再选择网格、点阵、频谱或隧道，不把背景做成持续抢焦点的主运动。
6. **研究自动化架构时看 `AIEV`、`OpenChatCut`、`Orkas-VideoStudio`**：只借流程、数据结构和 QA 机制，外部密钥、音效、示例图片和依赖都要单独核验。

## 五、许可证和素材提醒

- `MIT` / `Apache-2.0` 只说明仓库代码的许可，不自动覆盖 README 截图、demo 视频、字体、音效、纹理和第三方依赖。
- `OpenChatCut` 是 `AGPL-3.0`；`Theatre.js` 的 Studio 也是 `AGPL-3.0`。它们很适合研究，但不应未经合规判断直接复制到闭源交付工程。
- `Remotion` 本身有独立许可；`template-three` 的仓库代码虽标 MIT，实际使用仍要按当前 Remotion 条款核验。
- 本次只做公开仓库研究，没有把任何仓库安装到工作流、没有采集公开身份截图、没有读取视频项目素材，也没有启动预览或渲染。

## 核查快照

为保证以后复查不受默认分支变化影响，本次读取的是以下提交（只读浅克隆位于 `/tmp/codex-ai-video-research-20260823/`）：

| 仓库 | 提交 |
|---|---|
| `motion-canvas/motion-canvas` | `7b91435c301d530351dcf5ebb91dd139c002e405` |
| `astrofox-io/astrofox` | `47b76f0f7241103cf9b55c0f51469bcde5b695e5` |
| `theatre-js/theatre` | `6ea82b938ea49609489f6377ded693ccc6ee8f5b` |
| `williamngan/pts` | `0f350d4145efd2d54a57a7cd29d3c9a03a4e6bbb` |
| `fand/vfx-js` | `0e8f10211a1ca5b366fff461077154af008e575c` |
| `tsparticles/tsparticles` | `85d4d01d84bdaea301484427cdd41652c33bcad0` |
| `remotion-dev/template-three` | `4272f1a21258674471a6c711f2b7a464cc484338` |
| `stefanwittwer/remotion-animated` | `263f73b46fe9b72f587017acd555874d4c00191f` |
| `snapcndev/snapcn` | `5c1528d21e9d1fee38540200523875551ab15f9f` |
| `notivn/AIEV` | `1a4c2b0c67f685e3cc62b34cd29755bc2742b768` |
| `0xsline/OpenChatCut` | `320c07fd146c4068fc0ac62004b9e2818122d530` |
| `Orkas-AI/Orkas-VideoStudio` | `7387d99d468e0cce22508854ba8bca04e79657e1` |
