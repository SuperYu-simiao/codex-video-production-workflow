import {z} from 'zod';

export const assetKindSchema = z.enum(['color', 'image', 'video']);
export const layoutPresetSchema = z.enum([
  'fullscreen',
  'pip-br',
  'pip-bl',
  'left-rail',
  'right-rail',
]);
export const effectIdSchema = z.enum([
  'none',
  'flash-cut',
  'line-carry-transition',
  'glow-wake-sleep-panel',
]);

export const assetSchema = z.object({
  id: z.string().min(1),
  label: z.string().min(1),
  kind: assetKindSchema,
  src: z.string().optional(),
  color: z.string().optional(),
});

export const sceneSchema = z.object({
  id: z.string().min(1),
  title: z.string(),
  assetId: z.string().min(1),
  layout: layoutPresetSchema,
  effect: effectIdSchema,
  effectIntensity: z.number().min(0).max(1),
  pipScale: z.number().min(0.16).max(0.42),
  from: z.number().int().min(0),
  durationInFrames: z.number().int().min(1),
  visible: z.boolean(),
});

export const editorConfigSchema = z.object({
  schemaVersion: z.literal(1),
  title: z.string().min(1),
  width: z.number().int().positive(),
  height: z.number().int().positive(),
  fps: z.number().positive(),
  durationInFrames: z.number().int().positive(),
  backgroundColor: z.string().min(1),
  assets: z.array(assetSchema),
  scenes: z.array(sceneSchema).min(1),
});

export type Asset = z.infer<typeof assetSchema>;
export type LayoutPreset = z.infer<typeof layoutPresetSchema>;
export type EffectId = z.infer<typeof effectIdSchema>;
export type Scene = z.infer<typeof sceneSchema>;
export type EditorConfig = z.infer<typeof editorConfigSchema>;

export function parseEditorConfig(value: unknown): EditorConfig {
  return editorConfigSchema.parse(value);
}
