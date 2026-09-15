# 风格库2 × video-shotcraft 特效映射

对照仓库：[`Vincentwei1021/video-shotcraft`](https://github.com/Vincentwei1021/video-shotcraft)

对照基准：`风格库2.MD` 对参考视频 `/Users/yusimiao/Desktop/录屏2026-08-18 21.23.34.mov` 的 0–139 秒拆解。

用途：为下一期视频分镜选型。这里匹配的是**视觉布局、运动机制和剪辑语法**，不是要求素材、配色和文案完全相同。

> 结论：库里没有一张卡能复刻整支参考片，但有 50 余个可用的布局或运动机制，其中 16 个是优先级最高的直接近似项。黑色透视网格、三枚机械齿轮、法庭/赛车/AI 人物等内容资产仍需单独制作或替换。

## 1. 匹配等级

- `A 直接近似`：布局或运动因果与参考片基本一致，主要替换内容和配色。
- `B 可组合`：单独看只覆盖一个环节，与另一张卡组合后能还原该段语法。
- `C 借机制`：视觉长相不同，但适合表达同一种叙事功能。

名称写法为 `卡片名 / style key`。没有斜杠时，两者同名。在 Gallery 中优先搜索 style key。

## 2. 17 个参考模块逐项映射

| 参考模块与原片时间 | A 级直接近似 | B/C 级备选机制 | 下一期适用场景与改造方法 |
|---|---|---|---|
| `S2-C01` 黑色透视技术舞台，全片 | `basic-3d-scene`、`dashboard-glow-highlight-pill` | `assemble-then-type-flyin`、`depth-layer-moves / multiplane`、`radial-wave` | 作为全片统一母场景：暗底、消失点、中央主物、轻推或轻视差。Shotcraft 没有完全相同的独立网格背景，需要自建底层；借这些卡的空间和镜头语法。 |
| `S2-C02` 3D 手机 + 关键词，00:00–00:05 | `radial-ripple-phone-chips` | `magician-card-flourish`、`spotlight-hero-card`、`outline-word-fill` | 手机产品、工具界面、开场 hook。把浅灰波纹改成黑色透视舞台，两侧 chip 换成用户反馈或功能词；手机必须放真实页面。 |
| `S2-C03` 中心文档 + 周边评论卡，00:02、00:05 | `card-stack`、`research-card-stack-scroll` | `deck-deal-flyin`、`list-stack-press`、`page-waterfall-wall` | 大量评论、资料、案例、提示词或报告。主文档先建立，再让证据卡错峰出现；不要让所有卡同时抢阅读。 |
| `S2-C04` 头像/图标 + 能量场，00:08–00:11 | `radial-wave`、`spotlight-hero-card` | `integration-hub-map`、`magician-card-flourish` | 工具升级、角色拟人、能力激活。中央图标只做一次明确升级，外围波纹/节点表示能力扩散；改为蓝、紫或单一强调色。 |
| `S2-C05` 三档齿轮/模式选择，00:16–00:18 | `chip-grid-single-select-blackout`、`picker-carousel-feature-cycle` | `segmented-thumb-hero`、`floating-glossy-label-pills`、`pill-slot-cycle`、`beat-step-list-theme-cycle` | 套餐、速度档、模型档、工作流模式。保留“三项同时可见、一次只亮一个”的原则；`segmented-thumb-hero` 原生是二选一，使用时需扩为三段。 |
| `S2-C06` 轨道/半球层级，00:23–00:25 | `carousel-3d` | `countdown-arc-scatter`、`integration-hub-map`、`basic-3d-scene`、`floating-glossy-label-pills` | 多档系统、产品生态、能力从中心向外展开。`carousel-3d` 负责环形空间，`integration-hub-map` 负责中心—外围关系；均需重做成低速、低亮度。 |
| `S2-C07` 巨型章节字 + 技术线稿，00:26、00:54、00:99 | `outline-word-fill`、`wall-reveal-moves / wireframe-draw-on` | `blur-slide`、`split-flap-title`、`type-entrance-moves / scramble-decode` | “顶层设计 / 搜索 / 质检”这类章节页。大标题先定，线稿随后描出；一支片最多用两种标题入场，glitch 只留给转折。 |
| `S2-C08` 失败拼贴 + 印章，00:29–00:33 | `slam-entrance-moves / score-slam`、`slam-entrance-moves / impact-burst-kit` | `slam-entrance-moves / kanada-perspective-snap`、`cel-flash-stomp`、`montage-rhythm-moves / drop-blackout-slam`、`paper-craft-moves / masking-tape-slap` | 失败案例、错误方法、淘汰判定。把 KPI 卡换成 `FAILED` 或结论印章；只砸一次，落定后停 0.8–1.5 秒。 |
| `S2-C09` 舞台上的网页/文档，00:13–00:15、00:34–00:40、00:49–00:50 | `dashboard-glow-highlight-pill`、`doc-park-left-pill-deal` | `neon-frame-forerun`、`neon-frame-orbit-drop`、`spotlight-hero-card`、`steep-tilt-glide`、`cursor-flyover` | 展示真实网页、GitHub、提示词、回答和报告。入场可有 3D 仪式，开始阅读后必须停掉无关漂移；文字页面至少保留可读停留。 |
| `S2-C10` 搜索框 + 旧档案，00:46–00:50 | `type-and-filter`、`command-palette-summon` | `glass-pill-dictation-typing`、`research-card-stack-scroll`、`ai-stream-response` | 搜索、筛选、查证、Agent 检索。推荐链路：资料堆建立 → 输入关键词 → 结果收敛 → 证据行补齐。需要真实 UI 时首选 `type-and-filter`。 |
| `S2-C11` 专家/机构会审，00:51–00:56 | `avatar-bracket-carousel`、`research-card-stack-scroll` | `card-stack`、`carousel-3d`、`card-flip-reveal`、`floating-glossy-label-pills` | 多专家、多模型、多机构交叉验证。要表达“同一位置轮换专家”用头像轮播；要表达“资料很多”用论文堆；机构和结论必须真实或明确标为示意。 |
| `S2-C12` 多窗口推理 + 真人 PIP，00:66–00:67、01:41–01:46 | `doc-park-left-pill-deal` | `panel-grid-moves / comic-panel-split`、`quad-split-parallel-scenes`、`terminal-3d`、`basic-3d-scene` | 真人讲解 + 文档证据、主结论 + 辅助过程。`doc-park-left-pill-deal` 最适合“左文档、右结论”；若换真人 PIP，人物固定不动，只让证据页更新。 |
| `S2-C13` AI 生成画面/B-roll 例证，01:08–01:12、01:49–01:54 | `trailer-grammar-moves / card-footage-cadence` | `shot-transitions / shot-transitions-5`、`transition-hidden-cut / light-leak-burn`、`shot-transitions / flash-cut` | 用生成画面或现实 B-roll 举例。库里提供的是“素材与字卡如何交替”和转场，不提供人物/场景素材；示例结束要明确回到真人。 |
| `S2-C14` 逻辑盒/数据工地，01:21–01:26 | `paper-craft-moves / popup-book-rise` | `scanline-assemble-flyin`、`assemble-then-type-flyin`、`bezier-source-converge-merge`、`montage-rhythm-moves / domino-cascade` | 素材出箱、组件组装、数据搬运、多源汇聚。`popup-book-rise` 适合箱盖打开后对象立起；数据流则用贝塞尔路径汇聚，不必真的拍工人搬箱。 |
| `S2-C15` 快档 glitch + 质检蓝图，01:32–01:48 | `glitch-cycle`、`tear-streak-transitions / glitch-displace`、`wall-reveal-moves / wireframe-draw-on`、`scanline-annotate-focus` | `smear-multiples`、`draw-svg-trace`、`speed-ramp-freeze / freeze-annotate`、`type-entrance-moves / scramble-decode` | 快速但粗糙：残影、短 glitch、快切；质量检查：线稿、扫描、圈注、定格。两种模式必须有明显运动反差，不能只换颜色。 |
| `S2-C16` 赛车/引擎类比蒙太奇，01:59–02:10 | `beat-cut-moves / beat-cut-accelerando`、`speed-ramp-freeze / speed-ramp`、`shot-transitions / whip-pan` | `montage-rhythm-moves / wright-triple-cut`、`smear-multiples`、`crash-zoom-punch`、`rhythm-interrupt-moves / jump-cut-punch-in`、`trailer-grammar-moves / smash-cut` | 工具—操作者—档位—结果的高速类比。库里负责切点、变速和动作接力，不提供赛车素材；镜头方向要一致，快切结束后必须给结论长镜。 |
| `S2-C17` 键盘设问 + GitHub 收尾，02:11–02:19 | `speed-ramp-freeze / freeze-annotate`、`cursor-flyover`、`scanline-annotate-focus` | `input-trigger-moves / cursor-performance`、`type-entrance-moves / scramble-decode`、`tear-streak-transitions / glitch-displace` | 进入实操、仓库导览、页面重点指示。先用问题字卡设问，再切真实 GitHub；用光标、定格圈注或扫描框指重点，不要在结尾继续堆概念动画。 |

## 3. 下一期优先使用的 16 个核心效果

这些最贴合风格库2，且彼此分工清楚。

| 优先级 | 精确名称 | 最适合的场景 | 使用限制 |
|---:|---|---|---|
| 1 | `radial-ripple-phone-chips` | 手机、App、工具界面开场；两侧功能/评论标签 | 改成暗场；手机屏幕放真实内容。 |
| 2 | `type-and-filter` | 搜索、筛选、查证、从结果进入详情 | 真实 UI 逻辑优先，不要为了酷改成假界面。 |
| 3 | `command-palette-summon` | AI 命令、快捷搜索、Agent 入口 | 更偏风格化；不适合长文阅读。 |
| 4 | `score-slam` | `FAILED`、错误判定、关键结论砸落 | 一段只砸一次。 |
| 5 | `glitch-displace` | 失败、章节跳转、强问题 | 从原 demo 裁成 2–6 帧，禁止持续故障。 |
| 6 | `flash-cut` | 黑舞台冲入白色网页或录屏 | 曝光峰值覆盖切点即可，不要长时间纯白。 |
| 7 | `popup-book-rise` | 素材出箱、文档/组件立起 | 纸艺外观可换，底边铰链式“立起”机制保留。 |
| 8 | `wireframe-draw-on` | 质检、设计蓝图、从草稿到成品 | 线稿必须与最终页面严格对位。 |
| 9 | `scanline-annotate-focus` | 页面审查、AI 识别、规范拆解 | 标注数量控制在 3–6 个；扫完要停住。 |
| 10 | `doc-park-left-pill-deal` | 文档 + 三条结论；真人 + 证据分屏的骨架 | 只允许一个区域滚动。 |
| 11 | `research-card-stack-scroll` | 读了很多论文、处理很多材料、多机构证据 | 顶卡可读，其余卡只表达数量。 |
| 12 | `avatar-bracket-carousel` | 多专家、多角色、多模型在同一槽位轮换 | 适合“轮换”，不适合同时展示全部人物。 |
| 13 | `carousel-3d` | 三档/多档能力环、生态环、模板轮播 | 降低转速；改成一次展开而非无限炫转。 |
| 14 | `beat-cut-accelerando` | 赛车、工具操作、流程冲刺的加速蒙太奇 | 切完必须接稳定结论镜头。 |
| 15 | `speed-ramp` / `freeze-annotate` | 动作重点慢看；页面或 B-roll 定格讲解 | 教学场景优先 `freeze-annotate`。 |
| 16 | `cursor-flyover` | GitHub、产品页、单页四区域导览 | 不要飞遍整页；只点与旁白有关的位置。 |

## 4. 按使用场景查效果

### 开场 Hook / 主角登场

- 稳重产品主视觉：`radial-ripple-phone-chips`、`spotlight-hero-card`。
- 黑场魔术揭晓：`magician-card-flourish`。
- 重拳砸入：`kanada-perspective-snap`、`score-slam`、`impact-burst-kit`。
- 巨型利益词：`outline-word-fill`。

### 多档模式 / 多角色 / 多能力

- 三档同时可见并点亮：`chip-grid-single-select-blackout`。
- 竖向档位选择：`picker-carousel-feature-cycle`。
- 两档切换，可扩三档：`segmented-thumb-hero`。
- 同一词槽连续换模式：`pill-slot-cycle`、`pill-chip-slot-cycle-handled`。
- 多角色同槽轮换：`avatar-bracket-carousel`。
- 空间环形陈列：`carousel-3d`。

### 搜索 / 检索 / Agent 工作过程

- 真实搜索链路：`type-and-filter`。
- 命令面板式搜索：`command-palette-summon`。
- 输入框安静登场：`glass-pill-dictation-typing`。
- 先结论、后证据、再完成：`ai-stream-response`。
- 大量资料被处理：`research-card-stack-scroll`、`page-waterfall-wall`。

### 文档 / 页面 / 证据

- 文档 + 结论卡：`doc-park-left-pill-deal`。
- 页面隆重进入暗场：`neon-frame-forerun`、`neon-frame-orbit-drop`。
- 单页功能巡览：`cursor-flyover`。
- 页面自己写出来：`document-typewriter-reveal`。
- 多页面形成卡墙：`deck-deal-flyin`、`card-stack`。

### 失败 / 警告 / 强结论

- 判定砸落：`score-slam`。
- 影响周边元素的重击：`impact-burst-kit`。
- 大词像图章落下：`cel-flash-stomp`。
- 高潮前黑场蓄爆：`drop-blackout-slam`。
- 动漫式命中反馈：`impact-feedback / anime-impact`，仅在全片最重的一次使用。

### 质检 / 审查 / 专业判断

- 蓝图成形：`wireframe-draw-on`。
- 扫描并逐项标注：`scanline-annotate-focus`。
- 单个元素描边圈出：`draw-svg-trace`。
- 播放—定格—圈注—恢复：`freeze-annotate`。
- 多专家轮换：`avatar-bracket-carousel`。

### 高速蒙太奇 / 类比段

- 切点逐渐加快：`beat-cut-accelerando`。
- 三个流程特写：`wright-triple-cut`。
- 快—慢—快看重点：`speed-ramp`。
- 横向甩镜换场：`whip-pan`。
- 漫画式速度残像：`smear-multiples`。
- 一拍急推到目标：`crash-zoom-punch`。
- 最后猛切定论：`trailer-grammar-moves / smash-cut`。

### 真实录屏 / GitHub / 实操结尾

- 光标带观众巡览：`cursor-flyover`。
- 定格圈注重点：`freeze-annotate`。
- 扫描并打标签：`scanline-annotate-focus`。
- 光标点击 + 涟漪 + 推近：`cursor-performance`。
- 卡片变窗口进入详情：`shot-transitions / mask-wipe`。

## 5. 推荐的 5 条组合链

### 组合 A：产品/工具开场，5–7 秒

`radial-ripple-phone-chips` → `outline-word-fill` → `basic-3d-scene`

适合“今天介绍一个新工具/新模型”。手机或主页面先成为主角，巨型标题钉住主题，再回到统一暗舞台。

### 组合 B：搜索查证，7–10 秒

`research-card-stack-scroll` → `type-and-filter` → `ai-stream-response`

适合“先查资料，再给结论”。三段分别回答：资料量、具体操作、结果与证据。

### 组合 C：失败到正确方法，6–9 秒

`score-slam` → `glitch-displace` → `flash-cut` → 真实网页

适合反例教学。失败判定落下，极短故障撕裂，再用白闪把黑色概念舞台交给真实操作。

### 组合 D：质量检查，8–12 秒

`wireframe-draw-on` → `scanline-annotate-focus` → `doc-park-left-pill-deal` → `freeze-annotate`

适合“专业模式/质检模式”。从蓝图建立严谨感，扫描问题，给出结论，最后定格指出关键证据。

### 组合 E：高速类比到实操，8–12 秒

`beat-cut-accelerando` + `speed-ramp` + `whip-pan` → `cursor-flyover`

适合赛车、流水线、厨师等现实类比。前段用节奏把情绪拉高，最后降速进入真实页面，让“类比”落回“怎么操作”。

## 6. 统一改造成风格库2的规则

1. 所有效果统一放入低对比黑色透视舞台，不照搬 Gallery 的浅灰、纯白或霓虹底。
2. 每个镜头只保留一种强强调色：危险红、章节橙、AI 蓝、思考紫或专家红。
3. 动画先服务“对象发生了什么”，再服务好看；一镜只讲一个主概念。
4. `glitch-displace`、`glitch-cycle` 和 `scramble-decode` 只在失败、问题或跳章使用；强 glitch 限 2–6 帧。
5. 真实文档进入阅读阶段后，停止背景滚动、卡片轮播和持续推拉。
6. `carousel-3d`、`basic-3d-scene`、`neon-frame-*` 等炫技卡要降速、减光，不做持续霓虹表演。
7. 每次高能冲击后留 0.8–1.5 秒稳定画面；高速蒙太奇后留 1.5–2.5 秒结论镜头。
8. 下一期先按口播分配效果，再替换真实截图、文档和 B-roll；不要先挑一堆好看的效果再硬塞进内容。

## 7. 库中没有直接成品、仍需单独制作的内容

- 完全相同的黑色透视网格母舞台。
- 三枚真实机械齿轮及蓝—紫—红档位能量变化。
- 法庭、法槌、机构专家、乡村案例等概念内容资产。
- AI 蓝脑/旋涡、人物生成画面、赛车和数据工地等 B-roll。
- 真人口播竖屏 PIP 的完整模板；可用 `doc-park-left-pill-deal` 的布局骨架改造。

Shotcraft 在这些段落里主要提供运镜、卡片调度、强调、转场与剪辑节奏，不等于内容素材库。

## 8. 预览位置

- 在线 Gallery：<https://vincentwei1021.github.io/video-shotcraft/library.html>
- 本地候选样片：`参考分析缓存/video-shotcraft_匹配样片/`
- 候选静帧总览：`参考分析缓存/video-shotcraft_匹配样片/候选匹配总览.jpg`

实际制作下一期时，应先从上面的 16 个核心效果中选 4–7 个，再读取所选卡片的完整说明和 demo 实现，按具体口播逐槽编排；不建议一条片同时使用全部效果。
