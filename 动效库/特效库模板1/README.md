# 特效库模板1：暗场网格 + 语义证据动效

这是从“第9期 Codex 三个 Skill”实际成片中抽出的可复用动效模板。它保留本期已经验证过的运动语法、层级、节奏和安全区，把人物、网页截图、录屏、标题、步骤和字幕都改成可替换输入。

模板不是一条固定成片，也不包含任何本期真人原片、私人录屏、账户信息或 API key。使用时只把当前项目的素材放进项目自己的 `05-Remotion工程/public/`，按 `config/模板配置.example.json` 绑定槽位。

## 入口

- `特效库模板1.json`：机器可读的模块、卡名、时长、槽位和缓存策略。
- `模板调用说明.md`：以后新视频直接复制的调用提示词与执行顺序。
- `config/模板配置.example.json`：一条新视频的最小配置骨架。
- `src/index.ts`：模板代码入口，统一导出注册表和基础组件。
- `src/Template1Registry.ts`：TypeScript 类型、模块注册表和帧数换算工具。
- `src/Template1MotionPrimitives.tsx`：可复制到 Remotion 项目的网格、面板、标签、人物安全构图和隐私遮挡基础组件。
- `../../视觉规范与参考/特效库模板1.md`：完整的视觉规范、镜头选择和 QA 清单。
- `scripts/validate-template1.mjs`：检查 JSON、必需槽位和 Shotcraft Gallery 卡名。

## 本期抽取的模块

| 模块 | 语义用途 | 主 Shotcraft 卡 | 主要可替换槽位 |
|---|---|---|---|
| `hero-news` | 人物/新闻图全屏开场 | `graze-face-tour` | `heroImage`、`eyebrow` |
| `word-fracture` | 产品名碎片聚合 | `fracture` | `word` |
| `integration-hub` | “完全体/接入能力” | `integration-hub-map` | `centerImage`、`nodes[]` |
| `kill-shot` | 结论重音 | `montage-rhythm-moves` + `slam-entrance-moves` | `headline`、`accent` |
| `skill-wall` | 多个 Skill/产品首页墙 | `page-waterfall-wall` | `cards[]`（真实公开截图） |
| `bridge-flock` | 口播停顿的开场转场 | `card-flock-tumble`、`paper-plane-messenger` | `bridgeLabel`、可选 BGM |
| `definition-sop` | Codex/Skill/SOP 概念解释 | `paper-plane-messenger`、`research-card-stack-scroll` | `conceptImage`、`cards[]` |
| `identity-switch` | “快速切换身份” | `ai-stream-response` | `roles[]`、`summary` |
| `install-steps` | 三步安装/配置 | `beat-step-list-theme-cycle`、`doc-park-left-pill-deal`、`list-stack-press` | `steps[]`、`command` |
| `recording-runway` | 展示一段真实录屏 | `runway-ground-skim`、`line-unfold-panel` | `recording`、`privacyMask`、`fit` |
| `prompt-density` | 重复提示词/输入负担 | `scanline-annotate-focus` | `lines[]` |
| `process-flash` | 标准流程快速演示 | `flash-cut` | `steps[]` |
| `clone-assistant` | 工作方法克隆成助手 | `slam-entrance-moves`、`kanada-perspective-snap` | `headline`、`pills[]` |
| `research-hero` | anysearch 章节 | `spotlight-hero-card` | `pageImage`、`title` |
| `evidence-strip` | 财报/法律/论文举例 | `word-relay-filmstrip` | `documents[]` |
| `vertical-sources` | 垂直信息源连接 | `word-relay-geometry` | `sources[]` |
| `result-bento` | 搜索结果逐格点亮 | `wall-reveal-moves` + `bento-light-up` | `tiles[]` |
| `third-skill-morph` | 第三个 Skill 品牌揭示 | `ui-to-brand-morph` + `icon-flip-bloom` | `icon`、`title` |
| `thinking-rush` | AI 太急、先猜后写 | `typing-code-block` | `safeCode[]` |
| `planning-timeline` | 理解→拆解→计划→验证→执行 | `timeline-travel` | `milestones[]` |
| `floating-tags` | 辅助标签/关键词层 | `flying-words`、`floating-glossy-label-pills`、`dashboard-glow-highlight-pill` | `labels[]` |

## 不重复渲染的边界

模板会避免重复写动效代码和重复调参；但只要人物、口播、截图或字幕发生变化，最终视频仍需要一次合成渲染。可复用的部分分三层：

1. **动效壳**：卡片飞入、网格、扫描线、步骤链、时间线和转场参数固定，直接调用注册表。
2. **内容槽位**：人物视频、真实公开截图、录屏、标题和字幕作为 `inputProps` 替换。
3. **渲染缓存**：没有内容变化的静态转场或背景可保留成透明/独立片段；只改某一镜头时只渲染该镜头，再合成全片。

因此“调用模板”表示不用从头设计和调试特效，不表示完全不生成新的最终视频文件。模板目录不保存本期隐私素材，也不把本期内容硬编码进下一期。

## 基本约束

- 输出默认 `1920x1080`、`25fps`；Shotcraft 卡的 30fps 时长按比例换算，不能直接照搬帧数。
- 人物视频使用焦点居中裁剪；默认 `object-position: 50% 50%`，窄栏根据脸部焦点调整，不直接机械裁剪画面中心。
- 录屏默认 `contain`，只有确认四周无敏感信息时才用 `cover`；隐私遮挡不得覆盖有效操作区域。
- 每个镜头只设一个主动作，落定后至少保留 `0.8s` 阅读停留。
- 字幕始终在主画面安全带，不能压住人物脸、网页正文、控制条或关键卡片。
- API key、账户头像、私人路径、工作区名称和真实客户信息永远不进入模板或成片。
- 公开身份图只使用非登录页，并在项目的公开素材表记录来源 URL、日期和范围。

## 来源与许可证

Shotcraft 卡名和实现路径以当前机器的 `video-shotcraft` Gallery 为准；模板只记录卡名和调用关系，不复制第三方样片。具体卡片的许可证与实现说明仍以安装版本为准，升级 Shotcraft 后需重新校验 `source` 路径和时长。
