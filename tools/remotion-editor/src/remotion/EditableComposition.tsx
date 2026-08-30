import React from 'react';
import {Video} from '@remotion/media';
import {
  AbsoluteFill,
  Easing,
  Img,
  Sequence,
  interpolate,
  useCurrentFrame,
  useVideoConfig,
} from 'remotion';
import type {Asset, EditorConfig, Scene} from '../types';

type EditableCompositionProps = {
  config: EditorConfig;
};

const fontStack = 'Inter, -apple-system, BlinkMacSystemFont, "Helvetica Neue", sans-serif';

function AssetVisual({asset}: {asset: Asset}) {
  if (asset.kind === 'image' && asset.src) {
    return <Img src={asset.src} style={{width: '100%', height: '100%', objectFit: 'cover'}} />;
  }

  if (asset.kind === 'video' && asset.src) {
    return <Video src={asset.src} muted style={{width: '100%', height: '100%', objectFit: 'cover'}} />;
  }

  return (
    <AbsoluteFill
      style={{
        backgroundColor: asset.color ?? '#263033',
        justifyContent: 'center',
        alignItems: 'center',
      }}
    >
      <div
        style={{
          color: '#f3f6f4',
          fontFamily: fontStack,
          fontSize: 46,
          fontWeight: 650,
          letterSpacing: 0,
          textAlign: 'center',
        }}
      >
        {asset.label}
      </div>
      <div
        style={{
          marginTop: 18,
          color: 'rgba(243,246,244,0.66)',
          fontFamily: fontStack,
          fontSize: 22,
        }}
      >
        可替换素材槽位
      </div>
    </AbsoluteFill>
  );
}

function PresenterPip({scale}: {scale: number}) {
  return (
    <div
      style={{
        position: 'absolute',
        right: '4%',
        bottom: '7%',
        width: `${scale * 100}%`,
        aspectRatio: '16 / 9',
        border: '2px solid rgba(239, 246, 242, 0.75)',
        borderRadius: 18,
        backgroundColor: '#191d20',
        boxShadow: '0 18px 55px rgba(0, 0, 0, 0.35)',
        display: 'flex',
        alignItems: 'center',
        justifyContent: 'center',
        overflow: 'hidden',
      }}
    >
      <div
        style={{
          width: '28%',
          aspectRatio: '1',
          borderRadius: '50%',
          backgroundColor: '#d57b42',
          color: '#191d20',
          fontFamily: fontStack,
          fontSize: 34,
          fontWeight: 800,
          display: 'grid',
          placeItems: 'center',
        }}
      >
        口播
      </div>
    </div>
  );
}

function SceneEffect({scene}: {scene: Scene}) {
  const frame = useCurrentFrame();
  const {fps} = useVideoConfig();
  const intensity = scene.effectIntensity;

  if (scene.effect === 'flash-cut') {
    const opacity = interpolate(frame, [0, 3, 10], [intensity, 0, 0], {
      easing: Easing.out(Easing.cubic),
      extrapolateLeft: 'clamp',
      extrapolateRight: 'clamp',
    });
    return <AbsoluteFill style={{backgroundColor: '#f6f8f4', opacity, pointerEvents: 'none'}} />;
  }

  if (scene.effect === 'line-carry-transition') {
    const width = interpolate(frame, [0, 0.45 * fps], [0, 100], {
      easing: Easing.out(Easing.cubic),
      extrapolateLeft: 'clamp',
      extrapolateRight: 'clamp',
    });
    return (
      <div
        style={{
          position: 'absolute',
          top: '18%',
          left: 0,
          width: `${width}%`,
          height: Math.max(3, 12 * intensity),
          backgroundColor: '#d57b42',
          boxShadow: '0 0 28px rgba(213,123,66,0.55)',
          pointerEvents: 'none',
        }}
      />
    );
  }

  if (scene.effect === 'glow-wake-sleep-panel') {
    const opacity = interpolate(frame, [0, 0.5 * fps, 1.2 * fps], [0, intensity, intensity * 0.35], {
      easing: Easing.out(Easing.cubic),
      extrapolateLeft: 'clamp',
      extrapolateRight: 'clamp',
    });
    return (
      <AbsoluteFill
        style={{
          border: `${Math.max(2, 8 * intensity)}px solid rgba(213,123,66,${opacity})`,
          boxShadow: `inset 0 0 90px rgba(213,123,66,${opacity * 0.48})`,
          pointerEvents: 'none',
        }}
      />
    );
  }

  return null;
}

function SceneLayer({scene, asset}: {scene: Scene; asset: Asset}) {
  const isRail = scene.layout === 'left-rail' || scene.layout === 'right-rail';
  const mainInset =
    scene.layout === 'left-rail'
      ? {left: '31%', right: '4%'}
      : scene.layout === 'right-rail'
        ? {left: '4%', right: '31%'}
        : {left: '0%', right: '0%'};

  return (
    <AbsoluteFill style={{fontFamily: fontStack}}>
      <div
        style={{
          position: 'absolute',
          top: '4%',
          left: isRail ? '35%' : '5%',
          right: isRail ? '6%' : '5%',
          zIndex: 3,
          color: '#f3f6f4',
          fontSize: 44,
          fontWeight: 700,
          letterSpacing: 0,
        }}
      >
        {scene.title}
      </div>
      <div
        style={{
          position: 'absolute',
          top: '15%',
          bottom: '8%',
          ...mainInset,
          border: '1px solid rgba(239,246,242,0.28)',
          borderRadius: 20,
          overflow: 'hidden',
          boxShadow: '0 22px 60px rgba(0,0,0,0.28)',
        }}
      >
        <AssetVisual asset={asset} />
      </div>
      {scene.layout !== 'fullscreen' && <PresenterPip scale={scene.pipScale} />}
      {(scene.layout === 'left-rail' || scene.layout === 'right-rail') && (
        <div
          style={{
            position: 'absolute',
            top: '15%',
            bottom: '8%',
            left: scene.layout === 'left-rail' ? '4%' : undefined,
            right: scene.layout === 'right-rail' ? '4%' : undefined,
            width: '25%',
            borderRadius: 20,
            backgroundColor: '#191d20',
            border: '1px solid rgba(239,246,242,0.28)',
            display: 'grid',
            placeItems: 'center',
            color: 'rgba(243,246,244,0.72)',
            fontSize: 28,
          }}
        >
          人物栏
        </div>
      )}
      <SceneEffect scene={scene} />
    </AbsoluteFill>
  );
}

export function EditableComposition({config}: EditableCompositionProps) {
  return (
    <AbsoluteFill style={{backgroundColor: config.backgroundColor}}>
      <AbsoluteFill
        style={{
          backgroundImage:
            'linear-gradient(rgba(239,246,242,0.045) 1px, transparent 1px), linear-gradient(90deg, rgba(239,246,242,0.045) 1px, transparent 1px)',
          backgroundSize: '72px 72px',
          opacity: 0.34,
        }}
      />
      {config.scenes
        .filter((scene) => scene.visible)
        .map((scene) => {
          const asset = config.assets.find((candidate) => candidate.id === scene.assetId);
          if (!asset) return null;
          return (
            <Sequence
              key={scene.id}
              name={scene.id}
              from={scene.from}
              durationInFrames={scene.durationInFrames}
              premountFor={config.fps}
            >
              <SceneLayer scene={scene} asset={asset} />
            </Sequence>
          );
        })}
    </AbsoluteFill>
  );
}
