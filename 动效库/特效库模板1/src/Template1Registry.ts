export type Template1SpeakerState = 'fullscreen' | 'left-rail' | 'right-rail' | 'pip-br' | 'hidden';

export type Template1Slot =
  | 'word'
  | 'headline'
  | 'heroImage'
  | 'centerImage'
  | 'conceptImage'
  | 'pageImage'
  | 'recording'
  | 'publicScreenshots'
  | 'documents'
  | 'safeCode'
  | 'labels'
  | 'steps'
  | 'milestones'
  | 'nodes';

export type Template1Module = {
  id: string;
  label: string;
  semanticCue: string;
  shotcraftCard: string;
  styleKeys: string[];
  durationSeconds: {min: number; max: number};
  requiredSlots: Template1Slot[];
  speakerState: Template1SpeakerState;
  renderClass: 'content-bound' | 'transition' | 'overlay-cacheable';
  implementationHint: string;
};

export const TEMPLATE1_ID = 'effect-library-template-1';
export const TEMPLATE1_VERSION = '1.0.0';
export const TEMPLATE1_FPS = 25;

export const template1Modules: readonly Template1Module[] = [
  {
    id: 'hero-news',
    label: '人像/新闻全屏',
    semanticCue: '人物、新闻或公开来源的第一视觉信号',
    shotcraftCard: 'graze-face-tour',
    styleKeys: ['graze-face-tour'],
    durationSeconds: {min: 4, max: 5},
    requiredSlots: ['heroImage'],
    speakerState: 'hidden',
    renderClass: 'content-bound',
    implementationHint: '全屏 image terrain；镜头只做克制推近和横移。',
  },
  {
    id: 'word-fracture',
    label: '产品名碎片聚合',
    semanticCue: '第一次说出产品名或核心名词',
    shotcraftCard: 'fracture',
    styleKeys: ['fracture'],
    durationSeconds: {min: 3, max: 5.2},
    requiredSlots: ['word'],
    speakerState: 'hidden',
    renderClass: 'overlay-cacheable',
    implementationHint: '固定种子拆分字形；聚合后保留至少 0.8s 阅读。',
  },
  {
    id: 'integration-hub',
    label: '完全体/能力接入',
    semanticCue: '“完全体”“接入”“挂载能力”',
    shotcraftCard: 'integration-hub-map',
    styleKeys: ['integration-hub-map'],
    durationSeconds: {min: 4.5, max: 5},
    requiredSlots: ['centerImage', 'nodes'],
    speakerState: 'hidden',
    renderClass: 'content-bound',
    implementationHint: '真实公开截图做中心 hub，节点只写已核验能力。',
  },
  {
    id: 'kill-shot',
    label: '结论重音',
    semanticCue: '“杀招”“关键在于”“真正的原因”',
    shotcraftCard: 'montage-rhythm-moves',
    styleKeys: ['drop-blackout-slam', 'slam-entrance-moves'],
    durationSeconds: {min: 3, max: 5},
    requiredSlots: ['headline'],
    speakerState: 'hidden',
    renderClass: 'overlay-cacheable',
    implementationHint: '黑场落下、单句 slam、冲击余波后静止。',
  },
  {
    id: 'skill-wall',
    label: '多 Skill 首页墙',
    semanticCue: '“可以挂载各种 Skill”或多工具并列',
    shotcraftCard: 'page-waterfall-wall',
    styleKeys: ['page-waterfall-wall'],
    durationSeconds: {min: 4, max: 6},
    requiredSlots: ['publicScreenshots'],
    speakerState: 'hidden',
    renderClass: 'content-bound',
    implementationHint: '公开首页截图按倾斜墙落定；阅读期间停止镜头运动。',
  },
  {
    id: 'chapter-transition',
    label: '章节换场',
    semanticCue: '从安装/解释进入某个 Skill 章节，或章节结束回到人物',
    shotcraftCard: 'aurora-bloom-bg-flip',
    styleKeys: ['aurora-bloom-bg-flip', 'line-carry-transition', 'mosaic-reframe'],
    durationSeconds: {min: 2, max: 5.2},
    requiredSlots: [],
    speakerState: 'hidden',
    renderClass: 'transition',
    implementationHint: '先完成底色/边界变化，再显示新章节名；换句之间留空档。',
  },
  {
    id: 'bridge-flock',
    label: '停顿桥接',
    semanticCue: '口播句结束后的真实停顿或章节换气',
    shotcraftCard: 'card-flock-tumble',
    styleKeys: ['card-flock-tumble', 'paper-plane-messenger'],
    durationSeconds: {min: 3.5, max: 5},
    requiredSlots: ['publicScreenshots'],
    speakerState: 'hidden',
    renderClass: 'transition',
    implementationHint: '桥接段暂停源口播，BGM/SFX 单独进入；恢复同一源帧。',
  },
  {
    id: 'definition-sop',
    label: '概念解释/SOP',
    semanticCue: '“什么是 Skill”“大白话来说”“SOP 手册”',
    shotcraftCard: 'research-card-stack-scroll',
    styleKeys: ['paper-plane-messenger', 'research-card-stack-scroll'],
    durationSeconds: {min: 4, max: 6},
    requiredSlots: ['conceptImage', 'labels'],
    speakerState: 'hidden',
    renderClass: 'content-bound',
    implementationHint: '左侧概念证据 + 右侧纸张卡片堆叠；正文必须来自脚本。',
  },
  {
    id: 'identity-switch',
    label: '身份切换',
    semanticCue: '“快速切换身份”“变成程序员/研究员/分析师”',
    shotcraftCard: 'ai-stream-response',
    styleKeys: ['ai-stream-response'],
    durationSeconds: {min: 4, max: 5},
    requiredSlots: ['nodes'],
    speakerState: 'hidden',
    renderClass: 'content-bound',
    implementationHint: '先落可读摘要，再逐条汇入角色/证据，最后完成态。',
  },
  {
    id: 'install-steps',
    label: '三步安装链',
    semanticCue: '“分三步”“第一步/第二步/第三步”',
    shotcraftCard: 'beat-step-list-theme-cycle',
    styleKeys: ['doc-park-left-pill-deal', 'list-stack-press', 'fui-hud-moves', 'line-unfold-panel'],
    durationSeconds: {min: 4, max: 8},
    requiredSlots: ['steps'],
    speakerState: 'left-rail',
    renderClass: 'content-bound',
    implementationHint: '每步完整落定后再进入下一步；命令/配置只显示脱敏原文。',
  },
  {
    id: 'recording-runway',
    label: '真实录屏跑道',
    semanticCue: '“完整演示一遍”“打开工具”“输入指令”',
    shotcraftCard: 'runway-ground-skim',
    styleKeys: ['line-unfold-panel', 'doc-park-left-pill-deal'],
    durationSeconds: {min: 4, max: 12},
    requiredSlots: ['recording'],
    speakerState: 'right-rail',
    renderClass: 'content-bound',
    implementationHint: '录屏优先 contain；先做隐私 mask，再做外部字幕和标签。',
  },
  {
    id: 'prompt-density',
    label: '提示词负担',
    semanticCue: '“最烦”“重复输入一大段提示词”',
    shotcraftCard: 'scanline-annotate-focus',
    styleKeys: ['scanline-annotate-focus'],
    durationSeconds: {min: 3.5, max: 5},
    requiredSlots: ['labels'],
    speakerState: 'hidden',
    renderClass: 'overlay-cacheable',
    implementationHint: '提示词可以是概念示意；不得泄露真实项目内容。',
  },
  {
    id: 'process-flash',
    label: '流程闪切',
    semanticCue: '“标准流程”“精读/提炼/整理”并列动作',
    shotcraftCard: 'flash-cut',
    styleKeys: ['flash-cut'],
    durationSeconds: {min: 2.5, max: 4.5},
    requiredSlots: ['steps'],
    speakerState: 'hidden',
    renderClass: 'content-bound',
    implementationHint: '每个闪切只承载一个动作；白闪不能盖住字幕。',
  },
  {
    id: 'clone-assistant',
    label: '工作方法克隆',
    semanticCue: '“克隆成助手”“随时在线”“直接调用”',
    shotcraftCard: 'slam-entrance-moves',
    styleKeys: ['kanada-perspective-snap'],
    durationSeconds: {min: 4, max: 5},
    requiredSlots: ['labels'],
    speakerState: 'hidden',
    renderClass: 'overlay-cacheable',
    implementationHint: '主卡 slam 入场后只做一次 perspective snap，随后停住。',
  },
  {
    id: 'research-hero',
    label: '深度调研章节',
    semanticCue: '第二个 Skill/anysearch/深度调研',
    shotcraftCard: 'spotlight-hero-card',
    styleKeys: ['spotlight-hero-card'],
    durationSeconds: {min: 4, max: 5},
    requiredSlots: ['pageImage'],
    speakerState: 'hidden',
    renderClass: 'content-bound',
    implementationHint: '真实公开首页截图做主卡；扫光结束后保留阅读。',
  },
  {
    id: 'evidence-strip',
    label: '专业材料胶片',
    semanticCue: '“金融财报、法律条文、学术论文”',
    shotcraftCard: 'word-relay-filmstrip',
    styleKeys: ['word-relay-filmstrip'],
    durationSeconds: {min: 4.5, max: 7},
    requiredSlots: ['documents'],
    speakerState: 'hidden',
    renderClass: 'content-bound',
    implementationHint: '每张材料卡只用对应真实截图或明确标注的概念图。',
  },
  {
    id: 'vertical-sources',
    label: '垂直信息源连接',
    semanticCue: '“更专业的垂直信息源”',
    shotcraftCard: 'word-relay-geometry',
    styleKeys: ['word-relay-geometry'],
    durationSeconds: {min: 4.5, max: 6},
    requiredSlots: ['labels'],
    speakerState: 'hidden',
    renderClass: 'overlay-cacheable',
    implementationHint: '三个来源节点依次连接，连线只表达脚本中的关系。',
  },
  {
    id: 'result-bento',
    label: '结果逐格点亮',
    semanticCue: '“可以让它找”“扒出干货”“整理成文档”',
    shotcraftCard: 'wall-reveal-moves',
    styleKeys: ['bento-light-up'],
    durationSeconds: {min: 4, max: 6},
    requiredSlots: ['publicScreenshots', 'labels'],
    speakerState: 'hidden',
    renderClass: 'content-bound',
    implementationHint: '结果卡按语义逐格亮起；静态阅读时停止连续运动。',
  },
  {
    id: 'third-skill-morph',
    label: '第三个 Skill 揭示',
    semanticCue: '“第三个”“Superpowers/思考制动器”',
    shotcraftCard: 'ui-to-brand-morph',
    styleKeys: ['icon-flip-bloom'],
    durationSeconds: {min: 4, max: 5},
    requiredSlots: ['pageImage'],
    speakerState: 'hidden',
    renderClass: 'content-bound',
    implementationHint: '图标翻转到品牌卡；标题必须来自已确认名称。',
  },
  {
    id: 'thinking-rush',
    label: 'AI 过快示意',
    semanticCue: '“其实是它太急了”“瞎猜瞎写”',
    shotcraftCard: 'typing-code-block',
    styleKeys: ['typing-code-block'],
    durationSeconds: {min: 3.5, max: 5},
    requiredSlots: ['safeCode'],
    speakerState: 'hidden',
    renderClass: 'overlay-cacheable',
    implementationHint: '只使用安全伪代码或脚本原文，不显示 key、路径和真实数据。',
  },
  {
    id: 'planning-timeline',
    label: '思考制动时间线',
    semanticCue: '“理解需求、拆解任务、制定计划、逻辑验证、执行”',
    shotcraftCard: 'timeline-travel',
    styleKeys: ['timeline-travel'],
    durationSeconds: {min: 4, max: 5},
    requiredSlots: ['milestones'],
    speakerState: 'hidden',
    renderClass: 'overlay-cacheable',
    implementationHint: '节点逐项出现，最后一个节点再使用成功色。',
  },
  {
    id: 'floating-tags',
    label: '辅助关键词层',
    semanticCue: '需要补充语义关键词但不抢主画面时',
    shotcraftCard: 'flying-words',
    styleKeys: ['floating-glossy-label-pills', 'dashboard-glow-highlight-pill'],
    durationSeconds: {min: 2, max: 6},
    requiredSlots: ['labels'],
    speakerState: 'fullscreen',
    renderClass: 'overlay-cacheable',
    implementationHint: '只做从属层；避开脸部、字幕和网页正文。',
  },
];

export const template1ModuleById = Object.fromEntries(
  template1Modules.map((module) => [module.id, module]),
) as Record<string, Template1Module>;

export const framesFromSeconds = (seconds: number, fps = TEMPLATE1_FPS): number =>
  Math.max(1, Math.round(seconds * fps));

export const secondsFromFrames = (frames: number, fps = TEMPLATE1_FPS): number =>
  frames / fps;

export const validateTemplate1Module = (moduleId: string, availableSlots: readonly string[]) => {
  const module = template1ModuleById[moduleId];
  if (!module) throw new Error(`Unknown 特效库模板1 module: ${moduleId}`);
  const missing = module.requiredSlots.filter((slot) => !availableSlots.includes(slot));
  if (missing.length) {
    throw new Error(`Missing slots for ${moduleId}: ${missing.join(', ')}`);
  }
  return module;
};
