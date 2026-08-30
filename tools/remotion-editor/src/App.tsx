import React, {useMemo, useRef, useState} from 'react';
import {Player} from '@remotion/player';
import {defaultConfig} from './default-config';
import {EditableComposition} from './remotion/EditableComposition';
import {
  effectIdSchema,
  editorConfigSchema,
  layoutPresetSchema,
  parseEditorConfig,
  type EditorConfig,
  type Scene,
} from './types';
import './styles.css';

const layoutLabels: Record<Scene['layout'], string> = {
  fullscreen: '人物/素材全屏',
  'pip-br': '右下角 PIP',
  'pip-bl': '左下角 PIP',
  'left-rail': '左侧人物栏',
  'right-rail': '右侧人物栏',
};

const effectLabels: Record<Scene['effect'], string> = {
  none: '无主转场',
  'flash-cut': 'Flash Cut',
  'line-carry-transition': 'Line Carry',
  'glow-wake-sleep-panel': 'Glow Panel',
};

function App() {
  const [config, setConfig] = useState<EditorConfig>(defaultConfig);
  const [selectedSceneId, setSelectedSceneId] = useState(defaultConfig.scenes[0].id);
  const [error, setError] = useState('');
  const importRef = useRef<HTMLInputElement>(null);
  const selectedScene = useMemo(
    () => config.scenes.find((scene) => scene.id === selectedSceneId) ?? config.scenes[0],
    [config.scenes, selectedSceneId],
  );

  function updateScene(patch: Partial<Scene>) {
    setConfig((current) => {
      const scenes = current.scenes.map((scene) =>
        scene.id === selectedScene.id ? {...scene, ...patch} : scene,
      );
      const maxEnd = Math.max(...scenes.map((scene) => scene.from + scene.durationInFrames));
      return {...current, scenes, durationInFrames: Math.max(current.durationInFrames, maxEnd)};
    });
  }

  function downloadConfig() {
    const blob = new Blob([JSON.stringify(config, null, 2)], {type: 'application/json'});
    const url = URL.createObjectURL(blob);
    const anchor = document.createElement('a');
    anchor.href = url;
    anchor.download = 'video.config.json';
    anchor.click();
    window.setTimeout(() => URL.revokeObjectURL(url), 0);
  }

  async function importConfig(file: File) {
    try {
      const parsed = parseEditorConfig(JSON.parse(await file.text()));
      setConfig(parsed);
      setSelectedSceneId(parsed.scenes[0]?.id ?? '');
      setError('');
    } catch (caught) {
      setError(caught instanceof Error ? caught.message : '配置文件无法读取');
    }
  }

  function resetConfig() {
    setConfig(defaultConfig);
    setSelectedSceneId(defaultConfig.scenes[0].id);
    setError('');
  }

  const selectedAsset = config.assets.find((asset) => asset.id === selectedScene.assetId);

  return (
    <main className="editor-shell">
      <header className="topbar">
        <div>
          <p className="eyebrow">LOCAL REMOTION WORKBENCH</p>
          <h1>包装组件编辑器</h1>
        </div>
        <div className="top-actions">
          <button type="button" onClick={() => importRef.current?.click()}>
            导入配置
          </button>
          <button type="button" onClick={downloadConfig} className="primary-button">
            保存配置
          </button>
          <button type="button" onClick={resetConfig} className="quiet-button">
            重置示例
          </button>
          <input
            ref={importRef}
            type="file"
            accept="application/json,.json"
            hidden
            onChange={(event) => {
              const file = event.target.files?.[0];
              if (file) void importConfig(file);
              event.target.value = '';
            }}
          />
        </div>
      </header>

      <section className="workspace">
        <aside className="panel scenes-panel">
          <div className="panel-heading">
            <div>
              <span className="panel-kicker">TIMELINE</span>
              <h2>场景</h2>
            </div>
            <span className="count-badge">{config.scenes.length}</span>
          </div>
          <div className="scene-list">
            {config.scenes.map((scene) => (
              <button
                type="button"
                key={scene.id}
                className={`scene-row ${scene.id === selectedScene.id ? 'selected' : ''}`}
                onClick={() => setSelectedSceneId(scene.id)}
              >
                <span className="scene-index">{String(config.scenes.indexOf(scene) + 1).padStart(2, '0')}</span>
                <span className="scene-copy">
                  <strong>{scene.title || '未命名场景'}</strong>
                  <small>
                    {scene.from}–{scene.from + scene.durationInFrames}f
                  </small>
                </span>
                <span className={`visibility-dot ${scene.visible ? 'on' : ''}`} />
              </button>
            ))}
          </div>
          <div className="panel-note">
            这里的场景只控制包装层。口播精剪和原始素材仍然留在项目阶段目录中。
          </div>
        </aside>

        <section className="preview-column">
          <div className="preview-frame">
            <Player
              component={EditableComposition}
              inputProps={{config}}
              durationInFrames={config.durationInFrames}
              compositionWidth={config.width}
              compositionHeight={config.height}
              fps={config.fps}
              controls
              loop
              style={{width: '100%'}}
            />
          </div>
          <div className="preview-meta">
            <span>{config.title}</span>
            <span>{config.width} × {config.height} · {config.fps} fps</span>
          </div>
          {error && <p className="error-message">{error}</p>}
        </section>

        <aside className="panel inspector-panel">
          <div className="panel-heading">
            <div>
              <span className="panel-kicker">INSPECTOR</span>
              <h2>当前场景</h2>
            </div>
            <span className="scene-token">{selectedScene.id}</span>
          </div>

          <label className="field">
            <span>标题</span>
            <input value={selectedScene.title} onChange={(event) => updateScene({title: event.target.value})} />
          </label>

          <div className="field">
            <span>素材槽位</span>
            <div className="asset-grid">
              {config.assets.map((asset) => (
                <button
                  type="button"
                  key={asset.id}
                  className={`asset-chip ${asset.id === selectedScene.assetId ? 'selected' : ''}`}
                  onClick={() => updateScene({assetId: asset.id})}
                >
                  <span className="swatch" style={{backgroundColor: asset.color ?? '#536368'}} />
                  {asset.label}
                </button>
              ))}
            </div>
            <small className="field-help">当前：{selectedAsset?.label ?? '未找到素材'}</small>
          </div>

          <label className="field">
            <span>人物/素材布局</span>
            <select
              value={selectedScene.layout}
              onChange={(event) => {
                const layout = layoutPresetSchema.parse(event.target.value);
                updateScene({layout});
              }}
            >
              {Object.entries(layoutLabels).map(([value, label]) => (
                <option key={value} value={value}>{label}</option>
              ))}
            </select>
          </label>

          <label className="field">
            <span>主转场</span>
            <select
              value={selectedScene.effect}
              onChange={(event) => updateScene({effect: effectIdSchema.parse(event.target.value)})}
            >
              {Object.entries(effectLabels).map(([value, label]) => (
                <option key={value} value={value}>{label}</option>
              ))}
            </select>
          </label>

          <label className="field slider-field">
            <span>特效强度 <output>{Math.round(selectedScene.effectIntensity * 100)}%</output></span>
            <input
              type="range"
              min="0"
              max="1"
              step="0.01"
              value={selectedScene.effectIntensity}
              onChange={(event) => updateScene({effectIntensity: Number(event.target.value)})}
            />
          </label>

          <label className="field slider-field">
            <span>PIP 大小 <output>{Math.round(selectedScene.pipScale * 100)}%</output></span>
            <input
              type="range"
              min="0.16"
              max="0.42"
              step="0.01"
              value={selectedScene.pipScale}
              onChange={(event) => updateScene({pipScale: Number(event.target.value)})}
            />
          </label>

          <div className="timing-fields">
            <label className="field">
              <span>开始帧</span>
              <input
                type="number"
                min="0"
                value={selectedScene.from}
                onChange={(event) => updateScene({from: Math.max(0, Number(event.target.value) || 0)})}
              />
            </label>
            <label className="field">
              <span>持续帧数</span>
              <input
                type="number"
                min="1"
                value={selectedScene.durationInFrames}
                onChange={(event) => updateScene({durationInFrames: Math.max(1, Number(event.target.value) || 1)})}
              />
            </label>
          </div>

          <label className="toggle-field">
            <input
              type="checkbox"
              checked={selectedScene.visible}
              onChange={(event) => updateScene({visible: event.target.checked})}
            />
            <span>在预览中显示这个场景</span>
          </label>
          <p className="panel-note">改动只存在于当前浏览器状态。点击“保存配置”后才会下载 JSON 文件。</p>
        </aside>
      </section>
    </main>
  );
}

void editorConfigSchema;

export default App;
