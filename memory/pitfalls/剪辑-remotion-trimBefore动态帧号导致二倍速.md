---
name: 剪辑-remotion-trimBefore动态帧号导致二倍速
description: Remotion Video 的 trimBefore 传「当前帧号」会让视频 2 倍速播放（每帧都重新 seek）。人物 PIP/视频轨道 trimBefore 必须传固定起始帧，让 Video 自己随 Sequence 帧推进。改人物口播/视频对齐前必读。
type: gotcha
---

## 涉及文件
- `视频项目/*/05-Remotion工程/src/scenes/*.tsx`（人物 PIP 的 SpeakerVideo trimBefore）
- `视频项目/*/05-Remotion工程/src/components/SpeakerVideo.tsx`（Video 组件的 trimBefore 透传）

## 必保行为
1. **Remotion `<Video trimBefore={X}>` 语义**：在当前上下文帧 F，播放源视频第 `X + F` 帧。trimBefore 是「跳过源前 X 帧」的固定偏移，不是「当前该播哪一帧」。
2. **禁止传动态帧号**：`trimBefore={useCurrentFrame()}` 会导致帧 F 播源帧 `F + F = 2F`，整段 2 倍速（画面动作快、声音变尖快）。
3. **正确用法**：人物 PIP 放在 `<Sequence from={S}>` 里时，trimBefore 传固定值 S（该 Sequence 的起始源帧），Video 会随 Sequence 局部帧自动 1:1 推进。
4. 违反后果（实际发生过）：2026-09-17 第18期 v3 小样人物 PIP 用了 `trimBefore={frame}`，用户实报「人物语速那么快」，经能量包络对比定位为 2 倍速播放。

## 回归测试
- 渲染后验证音画同步：提取成片口播段能量包络，与源视频同时段逐 0.5s 对比，差异应 <5dB（`ffmpeg -ar 8000 -ac 1` + Python 算 RMS 包络）。

来源：2026-09-17 用户实报语速异常 → 定位 trimBefore 动态帧号 → 改为固定起始帧后能量包络对齐验证通过
