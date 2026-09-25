# Agent 治理

> 本文件按《agent-governance-template.md》组织；阶段顺序与过程的权威是 `skills/video-editing-workflow/SKILL.md`，授权门/目录/读序的机器契约是 `workflow.json`，制作约束在 `memory/`，关键决策在 `docs/adr/`。

## 1. 项目定位

- **一句话**：本地 AI 视频制作工作流——把真人口播视频经「Word 逐字稿盘点 → 补录清单 → 素材收集/录屏 → 素材复核 → 统一包装 → 精剪对齐 → Shotcraft 动效 → Remotion 合成 → 小样 → 成片」产出一条视频。
- **核心用户**：内容创作者本人，默认只在本机运行，不面向外部客户。
- **技术栈**：Python3（脚本、转录、校验）、Node / Remotion / React（包装合成与渲染）、FFmpeg（代理、抽帧、合成）、外部 Skills（video-use、video-shotcraft、transcribe）、可选 API（ELEVENLABS_API_KEY、OPENAI_API_KEY）。
- **架构一句话**：`skills/video-editing-workflow/SKILL.md` 是唯一剪辑入口（阶段顺序与过程）；`workflow.json` 是机器契约（授权门、目录、read_order）；`memory/` 存制作约束与剪辑细则；`docs/adr/` 存关键决策；`.agents/skills/video-production-bootstrap/SKILL.md` 负责环境、项目隔离与审批边界。
- **当前状态**：见各 `视频项目/<项目名>/project.json` 的「当前阶段」字段，不在本文件维护。
- **开工必读**：先读 `skills/video-editing-workflow/SKILL.md`、`workflow.json` 和当前项目 `project.json`；设置环境时读 `docs/00-先读我.md` 与 `dependencies.json`；只有素材复核通过、进入包装阶段后，才读 `effects.json`、`特效与切屏规范.md`、包装 Skill，以及**每期必读的两份质量基准**：`memory/reference/AI剪辑参考会话沉淀.md`（人物 PIP 与人脸居中、转场、节奏、先小样后全片）和 `memory/reference/特效使用模板.md`（逐字稿语义→特效选型）。

## 2. 汇报纪律

- **始终用中文与用户交互**；回复、注释、提交信息都用中文。
- **用户是老板，非程序员。** 汇报只说「结果和效果」：能不能用、跑通没跑通、下一步是什么。
- **禁止报技术过程**：不报测试条数、不报模块名、不报 agent 派发细节、不报 TDD 循环。
- 用户要技术细节时再展开。

## 3. 架构防腐（强制，加任何东西前先过这关）

往项目里加东西（台账条目 / 文档 / 计划 / agent / 技能），**不许破坏这套结构**：

1. **入口文件保持「薄」**：只加指针不加细节；新文档在「记忆索引」表加一行，正文别塞进入口文件。
2. **新增台账条目** → 同一轮在 `memory/MEMORY.md` 加索引行。
3. **新计划** → `plans/NNNN-YYYY-MM-DD-标题/`，并更新入口的「当前状态」指针。
4. **新决策** → 写 `docs/adr/` 或该计划的 `findings.md`，保证从记忆索引能找到。
5. **新文档 / 新 agent / 新技能** → 放对位置（`docs/`、`.pi/agents/`、`.pi/skills/`），别乱塞根目录。
6. **改 agent 边界或派发协议** → 同步检查入口的分工表是否还一致。

> 加东西前先问自己：**这该放哪？要不要更新索引/指针？**

## 4. 记忆台账（「越用越聪明」的核心）

### 4.1 渐进式披露

- 唯一入口是 `memory/MEMORY.md`：**一行一条 + 链接**，按 description 判断相关性再展开。
- **不要一次性读整个 `memory/` 目录**。先读索引，命中哪条读哪条。
- 目的：知识库越涨越大，每次开工的上下文负担不增加。

### 4.2 什么该记（满足任一条就记）

- 违反后果是线上 / 用户实报的 bug，且**从代码本身看不出为什么要这么写**。
- 来自某个**外部系统的反直觉行为**（第三方接口的存储布局、框架插件的隐式行为、数据库只读约束等）。
- **跨两处以上必须同步修改**的契约。

### 4.3 条目格式

`memory/TEMPLATE.md`：

```markdown
---
name: <项目前缀>-<主题>
description: 一行说明，索引里靠它判断相关性
type: 必保行为 | gotcha | runbook | reference | project
---

## 涉及文件
- `精确路径`（按改动面列全）
- 测试：`...test.ts`

## 必保行为
（具体到可验证，写清违反后果——最好是实际发生过的那个后果）

## 回归测试
（命令）

来源：`{{日期 + 谁实报 / 线上问题 / 排查过程}}`
```

### 4.4 索引

在 `memory/MEMORY.md` 按名称字母序加一行：

```
- `[[<name>]]` —— 一句话说明 + 何时读它（改 X 前必读）
```

## 5. 犯错即记（铁律，任何 agent 包括主 agent）

**犯了错，同一轮立刻记台账，不等用户追问。**

1. **主 agent 犯错** → 立即：① 写 `memory/constraints/`（若属跨代码/操作纪律）或 `memory/pitfalls/`（踩坑经过）；② 更新 `memory/MEMORY.md` 索引；③ 若是某个子代理的活，同步追加到该子代理的「犯错记录」。
2. **子 agent 犯错** → 主 agent 验收时发现，同一轮按上述入台账 + 补子代理的犯错记录。
3. **改数据（生产库 / 线上配置 / 权限 / 业务规则）必须先问用户**。写错数据立刻如实报告 + 恢复 + 记台账，**不掩盖**。

> 记台账不是罚站，是让下一次默认就不犯。

## 6. 台账防腐（强制）

台账过期比没有台账更危险。

- **改动了被台账覆盖的代码，必须同一轮回头更新对应条目。**
- 更新时**保留旧结论被推翻的痕迹**：写明「原为 X，YYYY-MM-DD 改为 Y，原因…」，不要直接抹掉。
- 条目里的「涉及文件」随代码搬家同步更新。

## 7. 计划文件夹（跨会话续接）

多步任务（5 次以上工具调用、跨会话）开工前先建文件夹：

```
plans/NNNN-YYYY-MM-DD-标题/
  task_plan.md    # 目标、已确认的关键决策、Phase 分解（带勾选状态）
  findings.md     # 调研结论、被否掉的方案
  progress.md     # 进度日志
```

- 在入口文件的「当前状态」写清当前计划路径和下一步。
- **冷启动顺序**：读 `AGENTS.md` → 读当前计划的「下一步」→ 按需展开记忆索引。
- 上下文丢失 / `/clear` 之后，靠这些文件恢复，不靠记忆。

> 本项目补充：每条独立视频 = 一个计划文件夹，用 `create_video_project.py` 建 `视频项目/<项目名>/project.json`；同一条视频的补录、修改、换会话继续原目录，不新建、不搬家。

## 8. 技能（Skills）

技能是「按需加载的能力包」，平时只占一行描述，命中任务才读正文。

### 8.1 放在哪

| 位置 | 作用域 | 说明 |
| --- | --- | --- |
| `~/.pi/agent/skills/<name>/SKILL.md` | 全局（所有项目） | 个人通用技能 |
| `~/.agents/skills/<name>/SKILL.md` | 全局（跨工具共享） | 多个 agent 工具共用 |
| `.pi/skills/<name>/SKILL.md` | 项目 | 项目专属技能，随仓库走 |
| `.agents/skills/<name>/SKILL.md` | 项目 | 跨工具共享的项目技能 |

> 项目级目录需要该目录被信任（首次进入 pi 会问一次）。

### 8.2 怎么写

```markdown
---
name: my-skill
description: 这个技能做什么 + 什么时候用它。这句决定 agent 会不会加载它，写具体。
---

# 技能标题

## 用法
（步骤、命令、脚本，用相对路径引用同目录的 scripts/、references/）
```

- `name`：小写字母、数字、连字符，≤64 字符。
- `description`：**写清「做什么」+「什么时候用」**。只写「帮助处理 X」等于没写。
- 目录里可以放 `scripts/`、`references/`、`assets/`，正文用相对路径引用。

### 8.3 怎么被引用

- **自动**：agent 看到任务匹配 description 就自己读。
- **手动**：`/skill:技能名`，后面可跟参数。
- **在入口文件里显式点名**（推荐，避免模型漏读）：

  ```markdown
  ## 技能优先级
  - 排查 bug → 优先用 `diagnosing-bugs`
  - 写计划 → 优先用 `planning-with-files`，计划落到 `plans/`
  - 架构评审 / 重构 → 优先用 `codebase-design`
  ```

### 8.4 推荐的通用开发技能（可选，按需安装）

| 技能 | 什么时候用 |
| --- | --- |
| `brainstorming` | 动手写代码前，把需求/设计问清楚 |
| `planning-with-files` | 多步任务落盘到 `plans/`，跨会话可续 |
| `writing-plans` | 有 spec 后写实现计划 |
| `executing-plans` | 带检查点地执行已写好的计划 |
| `test-driven-development` | 实现任何功能/修复前先写测试 |
| `diagnosing-bugs` | 排查硬 bug / 性能回归（先建可复现命令） |
| `systematic-debugging` | 通用调试 |
| `codebase-design` | 设计深模块、定接口边界、找重构点 |
| `domain-modeling` | 维护术语表 + 架构决策记录 |
| `requesting-code-review` | 完工前自查 |
| `receiving-code-review` | 收到评审意见后，先验证再改 |
| `verification-before-completion` | 宣布「完成」前，先跑验证 |
| `using-git-worktrees` | 需要隔离工作区时 |
| `subagent-driven-development` | 用子代理执行计划 |
| `dispatching-parallel-agents` | 2 个以上独立任务并行 |
| `writing-skills` | 写新技能 / 改技能 |

安装方式：把技能目录放进上面任一位置即可。让 pi 帮你写新技能，直接说「帮我写一个 X 技能」。

> 本项目技能：`.agents/skills/video-production-bootstrap/`（环境、依赖检查、项目隔离、审批边界，先跑只读 `check_dependencies.py`）、`skills/video-editing-workflow/`（唯一剪辑入口，路由 video-use → video-shotcraft → Remotion）、`skills/video-packaging-structure/`、`skills/transcribe/` 等，见各自 `SKILL.md`。

## 9. 子代理（Subagents）

子代理 = **独立上下文窗口里干活的专家**。主 agent 只拿它的结论，不继承它读过的所有文件。

### 9.1 为什么要用

- **上下文隔离**：子代理读 50 个文件，主 agent 只收一段报告，不被淹没。
- **职责专一**：每个子代理一个身份、一套边界、一份交付契约。
- **可并行**：互不依赖的活同时跑。

### 9.2 什么时候该派子代理（判断）

**该派：**

- 活**上下文很重**（要读大量文件、跑很多命令、查很多数据）。
- 活**独立可并行**，且相互之间没有共享状态。
- 活**边界清晰**，验收标准能用一两句话写出来。

**不该派（主 agent 自己干）：**

- 需要**业务判断 / 架构决策**的活——那是主 agent 的责任，不能外包。
- 任务**太小**（改个函数、加个日志），派发成本比干活还高。
- **验收标准说不清**——说明任务还没想清楚，先想清楚再派。
- 任务之间有**顺序依赖 / 共享状态**——不能并行，硬派会互相踩。

> 一句话：**能写清「验收标准」的活才派；说不清的就是主 agent 自己没想明白。**

### 9.3 什么时候该造一个新子代理（判断，四问）

不要每次派活都新建 agent。先过这四问：

1. **职责能一句话写清吗？**（它是什么专家）
2. **边界能写清、且和现有 agent 不重叠吗？**（它不做什么）
3. **这类活会重复出现吗？**（≥2 次；一次性的活不值得造）
4. **交付契约和验收标准能写清吗？**（它交什么、主 agent 怎么验）

**四问全 YES → 造。** 否则：

| 情况 | 该怎么做 |
| --- | --- |
| 和现有 agent 职责重叠 80% | **改现有 agent**，别新建 |
| 只是「这次活特别多」 | 那是**并行派发**，不是新 agent |
| 边界说不清 | 任务没想清楚，**先想清楚** |
| 只需要主 agent 的判断 | 主 agent 自己干 |

**边界互不重叠是硬要求。** 造之前先看入口文件里的「分工表」，新 agent 必须能填进一个现有表里没有的空位。

### 9.4 怎么造（落盘位置 + 模板）

**位置：**

- 项目级：`.pi/agents/<name>.md` —— 随仓库走，**需要 `agentScope: "both"` 才会加载**（默认只加载用户级）。
- 全局：`~/.pi/agent/agents/<name>.md` —— 所有项目可用。

**命名**：小写字母、数字、连字符（如 `test-runner`、`data-analyst`）。

**模板：**

```markdown
---
name: <agent 名>
description: <一句话：它是什么专家 + 什么时候该派它。主 agent 靠这句判断派不派>
tools: read, write, edit, grep, find, ls, bash   # 最小权限：只读就把 write/edit 砍掉
model: <模型 id>                                  # 贵的给判断，便宜的给执行；省略则继承主 agent
---

你是<角色>。核心职责：**<一句话>**。

## 开工前必读（背景，不是答案）
1. `AGENTS.md`
2. `memory/MEMORY.md`（按 description 判断本任务是否触及红线）
3. <任务相关的契约 / 规范文档路径>
4. 主 agent 给的 brief

## 核心工作流
1. …
2. …

## 边界（不做什么）
- <和现有 agent 不重叠的那条边界>
- 不做架构决策、不派 subagent、不跑全量构建

## 交付契约
回报四件事：
1. **结果**：完成 / 未完成，为什么
2. **改动文件**：`git diff --name-only` 清单
3. **验证**：跑了哪些命令、结果（贴关键输出）
4. **偏离 / 坑**：与 brief 的差异、踩到的坑

## 犯错记录（前车之鉴，每次犯错追加一条，别删、别合并）
（暂无，从第一次犯错开始记）
```

**造完必须做**：在入口文件的分工表里加一行（agent / 职责 / 不做什么）。

### 9.5 派发 brief 模板

```markdown
## 任务
（一句话：要做什么，为什么）

## 背景
（相关 spec / ADR 路径、术语表位置、必要上下文）

## 涉及文件
- 创建/修改：`精确路径`
- 测试：`精确测试路径`（主 agent 已写好，让它通过即可）

## 约束
- （硬约束：生产数据只读、权限只在核心模块强制、不要动 X 等）

## 验收
- （可验证的完成标准，通常是「测试通过」+「具体行为」）

## 不要做
- （边界：架构决策、写测试、派 subagent、改数据等）
```

### 9.6 报告契约

子代理完成后**必须**回报：

1. **结果**：完成 / 未完成，为什么
2. **改动文件**：`git diff --name-only` 清单
3. **验证**：跑了哪些命令、结果（贴关键输出）
4. **偏离**：与 brief 的差异（改了 brief 之外的东西必须显式说明）
5. **坑**：踩到的坑、外部系统反直觉行为（主 agent 决定是否入台账）

### 9.7 验收循环

1. 主 agent 读报告 → 对照 brief 的「验收」逐条核对。
2. 跑**定向验证**（只跑相关测试，不跑全量）。
3. 通过 → 决定是否入台账（踩坑 / 必保行为）→ 收工。
4. 不通过 → 带着「具体失败点」回派，附可复现命令，让子代理修。

> 主 agent 是控制器：**写 spec + 写测试用例**（懂业务/边界）→ 拆任务 → 派发 → review。
> 子代理不写测试、不做架构决策。

## 10. 验证纪律（默认只做定向验证）

除非用户明确要求「全量测试 / 完整回归 / 准备提交 / 准备部署」，否则**禁止擅自跑全量测试、全量类型检查或完整构建**。

- **默认验证范围** = 本轮实际改动的文件 + 直接相关测试。
- **只改文档 / 注释 / 计划文件时不跑任何代码测试。**
- 需要全量验证时，**先说明原因、命令、预计耗时，得到明确同意再跑**。
- 预计超过 2 分钟的单条命令，提前说明。

## 11. 禁止事项

- **只用项目指定的包管理器**，不混用（本项目：`npm`（Remotion 编辑器）、`python3` / `uv`（脚本与外部 Skills））。
- **用户没要求时不擅自 commit / push / upload**；本项目默认只在本地运行。
- 不提交临时排查文件、草稿、凭证；**真实密钥 / 令牌绝不进 git**；**不读 `.env` 或凭据**。
- 不把数据源 / 第三方接口的特判散落到核心调用路径（收在各自插件 / 适配器里）。
- **原始素材只读**：`01-原始素材/` 与 legacy 输入不重命名、不移动、不覆盖、不就地归一、不删除；生成内容只写对应 `02`～`07` 阶段目录。
- 不擅自部署、不擅自删数据、不擅自改环境变量——**改之前先问用户**；只安装用户明确要求的外部 Skill，安装授权 ≠ 剪辑/渲染授权。
- 不扫描其他视频项目、旧项目、整个动效库或无关路径；每次只处理用户明确指定、含 `project.json` 的当前项目。
- **补录清单阶段禁止**打开、播放、抽帧、提取音频、转录或用 `ffprobe` 分析口播视频；Word 缺失 / 损坏 / 不唯一时询问用户，不得改读视频。
- **确认点原样执行**：「先看小样」「禁止直接做视频」「不允许 render」不能因工具已装而跳过。
- 代理、批量抽帧、进程检查是独立辅助操作，不授权剪辑、预览渲染、最终渲染、杀进程、上传。
- 禁止 `git add -A`、`git add .` 等宽泛暂存；`.gitignore` 不冒充 watcher 排除。
- 不虚构 UI、操作成功、代码、百分比或资料包；原始事实不足时说明缺口。

## 12. 常用命令

```bash
# 只读依赖检查（设置/排查环境前先跑）
python3 .agents/skills/video-production-bootstrap/scripts/check_dependencies.py

# 安装锁定版本的外部 Skills（需用户明确授权）
python3 .agents/skills/video-production-bootstrap/scripts/install_dependencies.py --install

# 一键安装统一 Skill + 外部 Skills（需用户明确授权）
python3 .agents/skills/video-production-bootstrap/scripts/install_workflow.py --all

# 新建一条独立视频的项目（--dry-run 仅预览结构）
python3 .agents/skills/video-production-bootstrap/scripts/create_video_project.py --name "<项目名称>"

# 本地 Remotion 包装编辑器（默认端口 5178）
cd tools/remotion-editor && npm run dev

# 短代理 / 批量抽帧（默认 dry-run，写盘需 --execute）
python3 .agents/skills/video-production-bootstrap/scripts/create_short_proxy.py --help
python3 .agents/skills/video-production-bootstrap/scripts/batch_extract_frames.py --help

# 疑似渲染进程只读检查（无终止模式）
python3 .agents/skills/video-production-bootstrap/scripts/check_render_processes.py
```
