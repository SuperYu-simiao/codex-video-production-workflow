#!/usr/bin/env node
/**
 * 特效库模板1 的只读结构检查。
 * 默认从本模板目录读取 JSON，并尝试读取本机 video-shotcraft Gallery。
 * 不读取视频内容、不启动 Remotion、不渲染、不修改项目文件。
 */
import fs from 'node:fs';
import path from 'node:path';
import {fileURLToPath} from 'node:url';

const here = path.dirname(fileURLToPath(import.meta.url));
const templateDir = path.resolve(here, '..');
const manifestPath = path.join(templateDir, '特效库模板1.json');
const manifest = JSON.parse(fs.readFileSync(manifestPath, 'utf8'));

const failures = [];
if (manifest.schemaVersion !== 1) failures.push(`schemaVersion=${manifest.schemaVersion}`);
if (manifest.templateId !== 'effect-library-template-1') failures.push(`templateId=${manifest.templateId}`);
if (!Array.isArray(manifest.modules) || manifest.modules.length < 1) failures.push('modules is empty');
if (!Array.isArray(manifest.shotcraftValidation) || manifest.shotcraftValidation.length < 1) failures.push('shotcraftValidation is empty');

const ids = new Set((manifest.modules ?? []).map((module) => module.id));
for (const rule of manifest.cueRules ?? []) {
  if (rule.module && !ids.has(rule.module) && !rule.fallback) failures.push(`cueRule references unknown module: ${rule.module}`);
}

const galleryCandidates = [
  process.env.SHOTCRAFT_GALLERY,
  '/Users/yusimiao/.codex/skills/video-shotcraft/gallery/api/library.json',
].filter(Boolean);
let galleryPath;
for (const candidate of galleryCandidates) {
  if (fs.existsSync(candidate)) {
    galleryPath = candidate;
    break;
  }
}
let missingCards = [];
if (galleryPath) {
  const gallery = JSON.parse(fs.readFileSync(galleryPath, 'utf8'));
  const names = new Set((gallery.cards ?? []).map((card) => card.name));
  missingCards = (manifest.shotcraftValidation ?? [])
    .filter((entry) => !names.has(entry.card))
    .map((entry) => entry.card);
  if (missingCards.length) failures.push(`missing Gallery cards: ${missingCards.join(', ')}`);
}

const result = {
  templateId: manifest.templateId,
  version: manifest.version,
  modules: manifest.modules?.length ?? 0,
  validatedCards: manifest.shotcraftValidation?.length ?? 0,
  galleryChecked: Boolean(galleryPath),
  missingGalleryCards: missingCards.length,
  status: failures.length ? 'fail' : 'ok',
};
console.log(JSON.stringify(result, null, 2));
if (failures.length) {
  console.error(failures.map((failure) => `- ${failure}`).join('\n'));
  process.exitCode = 1;
}
