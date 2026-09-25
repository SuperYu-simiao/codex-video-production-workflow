---
name: 第17期-python脚本批量清理破坏结构
description: 用 python/sed 批量文本替换清理"双层 SpeakerVideo 套壳"时，误删 GrokHook.tsx 片头人物 pip 容器尺寸，导致片头人物消失。批量替换前必须确认每处匹配的上下文语义一致。
type: gotcha
---

## 涉及文件
- `视频项目/第17期 grokbot/05-Remotion工程/src/scenes/GrokHook.tsx`（HeadLayer 内联 Video 被误删尺寸）
- 其他 7 个场景（CloudPcScene/GrokTeach/GrokUsage/GrokSolo/GrokSoul/GrokTeam）用 SpeakerVideo 组件，未受影响

## 必保行为
- **GrokHook 的 HeadLayer 用的是内联 `<Video>`（不是 SpeakerVideo 组件）**，python 脚本按"SpeakerVideo 套壳"规则统一处理，把 pip 外层 div 的 `width/height/borderRadius/overflow` 全删了，只剩 `position:absolute; right/bottom; opacity`。
- 后果：pip 容器尺寸 0×0，内联 Video 的 `width:100%/height:100%` 解析为 0，句1 的 full→pip 交叉淡化（14-30 帧）完成后人物完全消失，片头 16 秒没有人物。
- **批量文本替换铁律**：替换前必须逐一确认每处匹配的上下文语义一致；内联 Video 和 SpeakerVideo 组件是两套结构，不能混为一谈。

## 回归测试
```bash
cd "视频项目/第17期 grokbot/05-Remotion工程"
# 片头 frame 30 / 200 右下角 pip 框应有肤色像素（人物居中 dx≈0）
npx remotion still GrokHook out/preview_stills/hook2-200.png --frame=200
python3 -c "from PIL import Image; ..."  # 肤色中心 x 应 ≈ 190
```

## 修复
GrokHook HeadLayer 改用 `SpeakerVideo` 组件（与其余 7 段统一），pip 尺寸 380×380 由组件内部保证 + 32% 人脸焦点 cover 裁切。

来源：2026-09-16 用户实报「完全没改好，片头那些都没了」→ 排查发现 python 脚本误删 GrokHook HeadLayer pip 容器尺寸。
