import React from 'react';
import {AbsoluteFill, Easing, interpolate} from 'remotion';

export const TEMPLATE1_FONT =
  'PingFang SC, Hiragino Sans GB, Noto Sans CJK SC, Arial Unicode MS, sans-serif';
export const TEMPLATE1_MONO = 'SFMono-Regular, Menlo, Monaco, Consolas, monospace';
export const TEMPLATE1_CLAMP = {
  extrapolateLeft: 'clamp' as const,
  extrapolateRight: 'clamp' as const,
};
export const TEMPLATE1_EASE = Easing.bezier(0.2, 0.76, 0.24, 1);

export const template1Fade = (
  frame: number,
  start: number,
  end: number,
  edge = 12,
): number =>
  interpolate(
    frame,
    [start, start + edge, Math.max(start + edge, end - edge), end],
    [0, 1, 1, 0],
    TEMPLATE1_CLAMP,
  );

export const Template1Grid: React.FC<{accent?: string}> = ({accent = '#72d9ff'}) => (
  <AbsoluteFill
    style={{
      pointerEvents: 'none',
      background: `radial-gradient(circle at 50% 45%, ${accent}22, transparent 52%), linear-gradient(rgba(255,255,255,.035) 1px, transparent 1px), linear-gradient(90deg, rgba(255,255,255,.025) 1px, transparent 1px), #06080d`,
      backgroundSize: '100% 100%, 120px 120px, 120px 120px, 100% 100%',
    }}
  />
);

export const Template1Panel: React.FC<{
  children: React.ReactNode;
  left?: number;
  top?: number;
  width?: number;
  height?: number;
  accent?: string;
  style?: React.CSSProperties;
}> = ({children, left = 0, top = 0, width = 600, height = 300, accent = '#72d9ff', style}) => (
  <div
    style={{
      position: 'absolute',
      left,
      top,
      width,
      height,
      overflow: 'hidden',
      borderRadius: 22,
      background: 'rgba(13,17,26,.94)',
      border: `1px solid ${accent}75`,
      boxShadow: `0 24px 70px rgba(0,0,0,.42), 0 0 30px ${accent}18`,
      ...style,
    }}
  >
    {children}
  </div>
);

export const Template1Label: React.FC<{
  children: React.ReactNode;
  color?: string;
  style?: React.CSSProperties;
}> = ({children, color = '#9aa7b6', style}) => (
  <div
    style={{
      color,
      fontFamily: TEMPLATE1_MONO,
      fontSize: 16,
      fontWeight: 800,
      letterSpacing: 2.2,
      ...style,
    }}
  >
    {children}
  </div>
);

type Template1SpeakerState = 'fullscreen' | 'left-rail' | 'right-rail' | 'pip-br';

export const Template1SpeakerFrame: React.FC<{
  children: React.ReactNode;
  state?: 'fullscreen' | 'left-rail' | 'right-rail' | 'pip-br';
  focus?: string;
  style?: React.CSSProperties;
}> = ({children, state = 'fullscreen', focus = '50% 50%', style}) => {
  const layouts: Record<Template1SpeakerState, React.CSSProperties> = {
    fullscreen: {inset: 0, width: '100%', height: '100%'},
    'left-rail': {left: '3.5%', top: '16%', width: '30%', height: '68%'},
    'right-rail': {left: '69%', top: '16%', width: '27%', height: '66%'},
    'pip-br': {right: '5%', bottom: '9%', width: '24%', height: '25%'},
  };
  return (
    <div
      style={{
        position: 'absolute',
        objectFit: 'cover',
        objectPosition: focus,
        overflow: 'hidden',
        borderRadius: state === 'fullscreen' ? 0 : 18,
        border: state === 'fullscreen' ? undefined : '1px solid rgba(255,255,255,.22)',
        boxShadow: state === 'fullscreen' ? undefined : '0 16px 46px rgba(0,0,0,.44)',
        ...layouts[state],
        ...style,
      }}
    >
      {children}
    </div>
  );
};

export const Template1PrivacyMask: React.FC<{
  regions: Array<{left: number; top: number; width: number; height: number}>;
  replacement?: string;
}> = ({regions, replacement = '[REDACTED]'}) => (
  <>
    {regions.map((region, index) => (
      <div
        key={`${region.left}-${region.top}-${index}`}
        style={{
          position: 'absolute',
          left: region.left,
          top: region.top,
          width: region.width,
          height: region.height,
          display: 'grid',
          placeItems: 'center',
          color: '#dce2ea',
          background: 'rgba(4,6,10,.98)',
          fontFamily: TEMPLATE1_FONT,
          fontSize: 20,
          fontWeight: 800,
          letterSpacing: 0.5,
        }}
      >
        {replacement}
      </div>
    ))}
  </>
);
