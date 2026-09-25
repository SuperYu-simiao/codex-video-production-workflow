---
name: 剪辑-remotion-封面裁剪焦点对齐露黑边
description: Remotion 人物口播封面裁剪（cover + 焦点对齐）时，left/top 不 clamp 到有效裁剪范围会露出黑边（尤其正方形 PIP：高度刚好 fit、焦点向下偏移让 top 变正值 → 顶部露黑框）。改人物 PIP/竖屏框裁剪前必读。
type: gotcha
---

## 涉及文件
- `视频项目/*/05-Remotion工程/src/components/SpeakerVideo.tsx`（coverFocusStyle 的 left/top 计算）

## 必保行为
1. **cover 裁剪的位置必须 clamp**：`scale = max(cw/SRC_W, ch/SRC_H)` 后，焦点对齐公式 `left = cw/2 - videoW*FOCAL_X`、`top = ch/2 - videoH*FOCAL_Y` 得到的结果**必须 clamp 到 `[container - video, 0]`**，否则会越界露黑边。
2. **为什么必须 clamp**：当容器是正方形（380×380）而源是 16:9（1920×1080）时，高度方向刚好 fit（videoH=380=containerH），此时 top 的合法范围是 `[0,0]`（只有 0 一个值，不能偏移）。但焦点 Y=0.32 会算出 `top = 190 - 380×0.32 = 68.4`（正值），视频被往下推 68px，容器顶部 0~68px 露黑边。
3. **正确实现**：
   ```ts
   const left = Math.min(0, Math.max(containerW - videoW, containerW/2 - videoW*FOCAL_X));
   const top  = Math.min(0, Math.max(containerH - videoH, containerH/2 - videoH*FOCAL_Y));
   ```
   即：某维度溢出（video > container）时焦点可自由移动并 clamp 在 `[container-video, 0]`；某维度刚好 fit（video == container）时强制为 0，不露黑边。
4. **语义**：正方形 PIP 应「从 16:9 画面里裁出中间的正方形区域」再缩放到框里，画面内容填满整个框；绝不是把整个 16:9 画面缩放后在框内留黑边。
5. 违反后果（实际发生过）：2026-09-17 第18期完整成片用户实报「人物剪裁上面有一个黑框，不要留黑边，你是在人物口播的画面里面剪裁」。

## 回归测试
- 渲染一张 PIP 帧，裁剪 PIP 框顶部 12px 区域，平均 RGB 应接近人物画面（肤色/背景），不应是纯黑（r/g/b 都 <30 才算黑边）。验证命令：PIL 裁 `(w-44-380, h-40-380, w-44, h-40)` 后取顶部 `(0,0,380,12)` 条带算均值。

来源：2026-09-17 用户实报 PIP 顶部黑边 → 定位 coverFocusStyle 缺 clamp → 加 clamp 后顶部条带实测 RGB=(39,33,24) 非黑边，v2 重渲通过
