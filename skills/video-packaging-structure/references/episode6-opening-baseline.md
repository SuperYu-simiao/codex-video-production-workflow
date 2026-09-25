# LONG_TUTORIAL_OPENING_BASELINE

状态：候选长期复用基线，来自用户明确满意的第六期开头实现；本文件不修改 Harness。

## 固定复用实现

- `WorkBuddyOpening` 四段顺序：OpeningToolCard 0–178f（7.12s）、WebsiteCompare 178–390f（8.48s）、PropositionLockup 390–631f（9.64s）、BrandBridge 631–744f（4.52s）。25fps、1920×1080。
- 口播在前 631f 使用连续 `voice.m4a`；BrandBridge 使用 `house-vibez`（trimBefore 300）与 `space-intro-futuristic`，639f 起 whoosh，689f 起 impact。
- OpeningToolCard：真实 WorkBuddy landing page 为 terrain；72f 透视游走，标签在约 .26/.48/.72 相位落地；94f 词级交接回连续人物。
- WebsiteCompare：Aurora pale→dark flip 42–51f；真实网站先 settle，再 WorkBuddy/Codex 双身份卡错峰 147/161f；人物为右侧 portrait。
- PropositionLockup：六张案例卡按 8/28/48/68/88/106f 依次飞入，106–122f overview；随后 logo 5.4→1、字母按 2.2f stagger、主张与“好在哪里？”。
- BrandBridge：三张能力卡 Catmull-Rom 空间运动，58f smoke ring，70f logo lockup，最终 113f 收束。

## 可替换变量

本期工具名、Logo、公开 landing page、案例截图、卡片文案、副标题、品牌色变量可替换，但必须来自已授权且可核验素材。

## 小范围自适应

可按新一期句长调整标签文案、卡片数量（保持错峰与信息层级）、公开截图裁切和 PIP 安全位置；核心阶段顺序和运动语义保持。

## 未经用户确认不得改

核心四段顺序、Aurora/透视游走/卡片飞入/BrandBridge 收束结构、主要时间关系、连续口播时间基准、音效组合、核心图层关系。新一期若不适合，需先说明证据和原因。

证据：`src/Root.tsx`、`src/WorkBuddyOpening.tsx`、`src/scenes/OpeningToolCard.tsx`、`WebsiteCompare.tsx`、`PropositionLockup.tsx`、`BrandBridge.tsx`。
