# LONG_TUTORIAL_TRANSITION_BASELINE

状态：候选长期复用基线，固定的是实现结构与节奏逻辑，不是具体颜色、文案或时间码。

## 固定复用

- 章节转场使用 `AuroraTitle`/`AuroraFlip`：浅色 bloom → 约 9 帧 dark flip → 标题落定，再进入真实 UI；一个新小标题只使用一次完整桥。
- 录屏/面板进入使用 22 帧 ease-out 的位移+透明度+轻微缩放；落定后停止相机运动。
- 人物全屏/PIP/隐藏由 `ContinuousSpeakerLayer` 以 18 帧几何插值完成；同源 `OffthreadVideo` 与独立连续音轨不重启。
- 录屏主画面保持真实证据，字幕与 pill 位于主合成层；PIP 与字幕采用对侧安全区。
- `ShotcraftEdgeMotion` 只在外缘运行 rail/scan/flyline/neon/boil 等低侵入层；不得覆盖脸、按钮、表格、地图或文档。

## 可替换变量

章节标题、副标题、录屏/截图、Logo、步骤文案、强调色和实际 PIP 左右位置可替换；隐私遮罩区域按素材重新标注。

## 小范围自适应

可根据内容决定使用标题桥、内部焦点变化或无转场的连续操作；结果 hold 时长按阅读负荷调整。不得把每个 BEAT=75 边缘节拍当作切点。

## 未经确认不得改

Aurora 的浅→暗结构、语义转场触发原则、18/22 帧核心关系、连续人物时间基准、边缘层安全范围。若新内容不适合，必须提供不适配证据并获得用户确认。

证据：`WorkBuddyEpisode3.tsx`、`ShotcraftEdgeMotion.tsx`、第二段审核报告、第三段 V3/V6/V8 QA、第三段导演分镜。
