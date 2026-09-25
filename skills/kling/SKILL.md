---
name: kling
description: 可灵 Kling 图生视频：把本地静态照片变成电影级运镜视频（苹果发布会式产品片）。当用户要把猫/产品照片"动起来"、生成特写→远景运镜视频、或用 AI 生成视频素材时使用。需要可灵 API Key（Bearer 鉴权）。
---

# 可灵 Kling 图生视频

把一张本地照片变成一段运镜视频，用于滚动驱动（scroll-video-parallax）等场景。

## 用法

```bash
# 1. 一次性保存 API key（存 skills/kling/auth.json，已被 .gitignore 排除）
python3 skills/kling/scripts/kling.py auth <API_KEY>

# 2. 一条龙：提交 + 轮询 + 下载
python3 skills/kling/scripts/kling.py gen \
  -i "猫照片.jpg" \
  -p "提示词" \
  -d 10 -r 1080p -o 输出.mp4

# 或分步：
python3 skills/kling/scripts/kling.py submit -i 猫.jpg -p "提示词" -d 10
python3 skills/kling/scripts/kling.py status <task_id>
python3 skills/kling/scripts/kling.py wait <task_id> -o 输出.mp4
```

## 提示词模板（苹果发布会猫片）

```
顶级商业产品广告摄影，苹果发布会风格。镜头从猫脸特写缓缓拉远至猫全身，
猫的毛发自然飘动，耳朵轻微抖动，眼睛自然眨动，胡须微颤，猫缓慢转头看向镜头。
纯白无缝背景，柔和影棚灯光，浅景深，超高清毛发细节，电影感，优雅。
```

- 想要"多镜头"可在提示词里用：`镜头 1, 5, 特写猫脸; 镜头 2, 5, 拉远到全身;`（分镜时长之和 = 视频总时长）
- 图生视频只支持「首帧图」或「首帧+尾帧」；竖版照片会生成竖版视频。

## 关键事实

- 域名：`https://api-beijing.klingai.com`（中国区）
- 图生视频：`POST /image-to-video/kling-3.0`，鉴权 `Authorization: Bearer <API_KEY>`
- 图片可用 base64 传，**不要加 `data:image/...;base64,` 前缀**，纯编码字符串即可
- 查询任务：`GET /tasks?task_ids=<id>`，状态 submitted/processing/succeeded/failed
- 生成的视频 URL 是防盗链格式，**30 天后清理**，拿到后必须立即下载转存（脚本 `wait`/`gen` 已自动下载）

## 错误排查

- 401 → API key 错误或未带 Bearer
- base64 报错 → 检查是否误加了 `data:` 前缀
- 图片宽高比须在 1:2.5 ~ 2.5:1 之间、≥300px、≤50MB
