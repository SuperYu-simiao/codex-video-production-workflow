# 黑灰透视网格科技背景

一个可编辑、可无缝循环的 Remotion 动态背景。

- 尺寸：2560 × 1440（16:9，2K）
- 帧率：30 fps
- 时长：10 秒
- 构图 ID：`TechPerspectiveGrid2K`
- 风格：黑灰、低强度冷白辉光、透视网格、远景雾化
- 运动：网格从左向右匀速漂移，首尾按完整网格周期衔接

## 本地预览

```bash
npm install
npm run dev
```

## 可调参数

在 Remotion Studio 右侧 Props 面板中可调整：

- `backgroundColor`：背景色
- `gridColor`：网格线颜色
- `glowColor`：辉光颜色
- `gridOpacity`：网格透明度
- `glowIntensity`：辉光强度
- `fogStrength`：远景雾化强度
- `gridDensity`：网格密度
- `travelCells`：每 10 秒向右移动的网格数量，保持整数可无缝循环
- `horizonRatio`：消失线的垂直位置

## 导出

```bash
npm run render
```

输出位置：`output/tech-perspective-grid-2k.mp4`
