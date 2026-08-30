# Remotion 包装组件编辑器

这是工作流的通用编辑器原型。它只编辑包装层参数，不读取或复制任何具体视频项目、原始素材、转录或成片。

## 能做什么

- 切换场景的素材槽位；
- 修改标题；
- 切换人物/素材布局；
- 切换主转场；
- 调节特效强度和人物 PIP 大小；
- 调整场景开始帧与持续帧数；
- 通过 `@remotion/player` 实时预览；
- 导入或下载经过 Zod 校验的 `video.config.json`。

示例素材使用纯色占位块，不包含私人媒体。接入具体项目时，把 `assets` 中的逻辑 ID 映射到当前项目的授权素材路径即可。

## 启动

```bash
cd tools/remotion-editor
npm install
npm run dev
```

浏览器打开 Vite 输出的本地地址，默认端口为 `5178`。

## 配置协议

`src/types.ts` 定义了编辑器和 Remotion 组件共享的配置协议。`src/default-config.ts` 是无私人素材的示例配置。真正的视频项目应把配置保存到项目自己的 `05-Remotion工程/config/video.config.json`，而不是覆盖 `01-原始素材/`。

## 接入当前视频项目

1. 将 `src/types.ts` 和 `src/remotion/EditableComposition.tsx` 的协议与组件复制到目标项目的 `05-Remotion工程/`；
2. 把示例 `assets` 替换成当前项目明确选定的素材 ID；
3. 把 `AssetVisual` 中的 `src` 解析到当前项目素材路径；
4. 将目标项目的 Composition 传给 `Player`；
5. 先做指定场景预览，再按现有 `workflow.json` 审批门槛执行最终渲染。

这个目录是可复用原型，不会自动扫描或混用仓库内其他视频项目。
