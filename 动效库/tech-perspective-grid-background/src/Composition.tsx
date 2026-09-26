import {zColor} from "@remotion/zod-types";
import React from "react";
import {
  AbsoluteFill,
  interpolate,
  useCurrentFrame,
  useVideoConfig,
} from "remotion";
import {z} from "zod";

export const perspectiveGridSchema = z.object({
  backgroundColor: zColor(),
  gridColor: zColor(),
  glowColor: zColor(),
  gridOpacity: z.number().min(0.05).max(1).step(0.05),
  glowIntensity: z.number().min(0).max(1.5).step(0.05),
  fogStrength: z.number().min(0).max(1).step(0.05),
  gridDensity: z.number().min(10).max(28).step(1),
  travelCells: z.number().min(1).max(8).step(1),
  horizonRatio: z.number().min(0.32).max(0.58).step(0.01),
});

type PerspectiveGridProps = z.infer<typeof perspectiveGridSchema>;

const rgba = (hex: string, alpha: number) => {
  const normalized = hex.replace("#", "");
  const expanded =
    normalized.length === 3
      ? normalized
          .split("")
          .map((character) => character + character)
          .join("")
      : normalized;

  const red = Number.parseInt(expanded.slice(0, 2), 16);
  const green = Number.parseInt(expanded.slice(2, 4), 16);
  const blue = Number.parseInt(expanded.slice(4, 6), 16);

  return `rgba(${red}, ${green}, ${blue}, ${alpha})`;
};

const range = (length: number) =>
  Array.from({length}, (_value, index) => index);

const PerspectiveMesh: React.FC<
  PerspectiveGridProps & {
    phase: number;
    width: number;
    height: number;
  }
> = ({
  phase,
  width,
  height,
  gridColor,
  glowColor,
  gridOpacity,
  glowIntensity,
  fogStrength,
  gridDensity,
  horizonRatio,
}) => {
  const horizonY = height * horizonRatio;
  const vanishingX = width * 0.5;
  const density = Math.round(gridDensity);
  const columnSpacing = width / density;
  const horizontalCount = 18;
  const columnCount = density + 20;
  const columnOffset = phase * columnSpacing;

  const columns = range(columnCount).map((index) => {
    const bottomX = (index - 10) * columnSpacing + columnOffset;
    const farX = vanishingX + (bottomX - vanishingX) * 0.022;
    return {bottomX, farX};
  });

  const depthFrames = range(horizontalCount).map((index) => {
    const normalized = (index + 1) / horizontalCount;
    const eased = normalized ** 2.45;
    return {
      yTop: horizonY - eased * (horizonY + 120),
      yBottom: horizonY + eased * (height - horizonY + 160),
      xLeft: vanishingX - eased * (width * 0.72),
      xRight: vanishingX + eased * (width * 0.72),
      opacity: 0.16 + normalized * 0.84,
    };
  });

  return (
    <svg
      viewBox={`0 0 ${width} ${height}`}
      width={width}
      height={height}
      style={{position: "absolute", inset: 0}}
    >
      <defs>
        <linearGradient id="ground-fade" x1="0" y1="0" x2="0" y2="1">
          <stop offset="0%" stopColor="white" stopOpacity="0" />
          <stop
            offset={`${16 + fogStrength * 14}%`}
            stopColor="white"
            stopOpacity={0.05}
          />
          <stop offset="68%" stopColor="white" stopOpacity="0.8" />
          <stop offset="100%" stopColor="white" stopOpacity="1" />
        </linearGradient>
        <linearGradient id="ceiling-fade" x1="0" y1="1" x2="0" y2="0">
          <stop offset="0%" stopColor="white" stopOpacity="0" />
          <stop
            offset={`${17 + fogStrength * 16}%`}
            stopColor="white"
            stopOpacity={0.035}
          />
          <stop offset="72%" stopColor="white" stopOpacity="0.56" />
          <stop offset="100%" stopColor="white" stopOpacity="0.76" />
        </linearGradient>
        <radialGradient id="horizon-fade" cx="50%" cy="50%" r="50%">
          <stop offset="0%" stopColor="white" stopOpacity="0" />
          <stop offset={`${24 + fogStrength * 22}%`} stopColor="white" stopOpacity="0.06" />
          <stop offset="72%" stopColor="white" stopOpacity="0.72" />
          <stop offset="100%" stopColor="white" stopOpacity="1" />
        </radialGradient>
        <mask id="ground-mask">
          <rect
            x="0"
            y={horizonY}
            width={width}
            height={height - horizonY}
            fill="url(#ground-fade)"
          />
        </mask>
        <mask id="ceiling-mask">
          <rect
            x="0"
            y="0"
            width={width}
            height={horizonY}
            fill="url(#ceiling-fade)"
          />
        </mask>
        <mask id="tunnel-mask">
          <rect width={width} height={height} fill="url(#horizon-fade)" />
        </mask>
        <filter id="soft-glow" x="-40%" y="-40%" width="180%" height="180%">
          <feGaussianBlur stdDeviation={6 + glowIntensity * 10} />
        </filter>
        <filter id="far-blur" x="-30%" y="-80%" width="160%" height="260%">
          <feGaussianBlur stdDeviation={3 + fogStrength * 9} />
        </filter>
      </defs>

      <g
        mask="url(#tunnel-mask)"
        fill="none"
        stroke={glowColor}
        strokeWidth={10 + glowIntensity * 10}
        opacity={0.045 * glowIntensity}
        filter="url(#soft-glow)"
      >
        {depthFrames.map((frameLine, index) => (
          <path
            key={`glow-frame-${index}`}
            d={`M ${frameLine.xLeft} ${frameLine.yTop} L ${frameLine.xRight} ${frameLine.yTop} L ${frameLine.xRight} ${frameLine.yBottom} L ${frameLine.xLeft} ${frameLine.yBottom} Z`}
          />
        ))}
      </g>

      <g
        mask="url(#tunnel-mask)"
        fill="none"
        stroke={gridColor}
        strokeWidth={1.15}
        opacity={gridOpacity * 0.48}
      >
        {depthFrames.map((frameLine, index) => (
          <path
            key={`depth-frame-${index}`}
            d={`M ${frameLine.xLeft} ${frameLine.yTop} L ${frameLine.xRight} ${frameLine.yTop} L ${frameLine.xRight} ${frameLine.yBottom} L ${frameLine.xLeft} ${frameLine.yBottom} Z`}
            opacity={frameLine.opacity}
          />
        ))}
      </g>

      <g
        mask="url(#ground-mask)"
        fill="none"
        stroke={glowColor}
        strokeWidth={8 + glowIntensity * 8}
        opacity={0.055 * glowIntensity}
        filter="url(#soft-glow)"
      >
        {columns.map(({bottomX, farX}, index) => (
          <path
            key={`ground-glow-${index}`}
            d={`M ${farX} ${horizonY + 2} L ${bottomX} ${height + 80}`}
          />
        ))}
      </g>

      <g
        mask="url(#ground-mask)"
        fill="none"
        stroke={gridColor}
        strokeWidth={1.3}
        opacity={gridOpacity}
      >
        {columns.map(({bottomX, farX}, index) => (
          <path
            key={`ground-column-${index}`}
            d={`M ${farX} ${horizonY + 2} L ${bottomX} ${height + 80}`}
          />
        ))}
        {depthFrames.map((frameLine, index) => (
          <path
            key={`ground-row-${index}`}
            d={`M ${frameLine.xLeft} ${frameLine.yBottom} L ${frameLine.xRight} ${frameLine.yBottom}`}
            opacity={frameLine.opacity}
          />
        ))}
      </g>

      <g
        mask="url(#ceiling-mask)"
        fill="none"
        stroke={gridColor}
        strokeWidth={1.05}
        opacity={gridOpacity * 0.6}
      >
        {columns.map(({bottomX, farX}, index) => {
          const topX = vanishingX + (bottomX - vanishingX) * 1.15;
          return (
            <path
              key={`ceiling-column-${index}`}
              d={`M ${farX} ${horizonY - 2} L ${topX} -80`}
            />
          );
        })}
        {depthFrames.map((frameLine, index) => (
          <path
            key={`ceiling-row-${index}`}
            d={`M ${frameLine.xLeft} ${frameLine.yTop} L ${frameLine.xRight} ${frameLine.yTop}`}
            opacity={frameLine.opacity * 0.7}
          />
        ))}
      </g>

      <g
        opacity={0.28 * glowIntensity}
        filter="url(#far-blur)"
      >
        <ellipse
          cx={vanishingX}
          cy={horizonY}
          rx={width * 0.28}
          ry={height * 0.035}
          fill={rgba(glowColor, 0.18)}
        />
      </g>
    </svg>
  );
};

export const TechPerspectiveGridBackground: React.FC<PerspectiveGridProps> = (
  props,
) => {
  const frame = useCurrentFrame();
  const {durationInFrames, height, width} = useVideoConfig();
  const loopProgress = frame / durationInFrames;
  const phase = loopProgress * props.travelCells;

  return (
    <AbsoluteFill
      style={{
        backgroundColor: props.backgroundColor,
        overflow: "hidden",
      }}
    >
      <AbsoluteFill
        style={{
          backgroundImage: `
            radial-gradient(ellipse 64% 19% at 50% ${props.horizonRatio * 100}%, ${rgba(props.glowColor, 0.12 * props.glowIntensity)} 0%, ${rgba(props.glowColor, 0.035 * props.glowIntensity)} 38%, transparent 72%),
            radial-gradient(circle at 78% 14%, ${rgba(props.glowColor, 0.04)} 0%, transparent 34%),
            linear-gradient(135deg, ${rgba(props.gridColor, 0.025)} 0%, transparent 35%, ${rgba(props.glowColor, 0.018)} 74%, transparent 100%)
          `,
        }}
      />

      <PerspectiveMesh
        {...props}
        phase={phase}
        width={width}
        height={height}
      />

      <AbsoluteFill
        style={{
          backgroundImage: `radial-gradient(circle, ${rgba(props.gridColor, 0.12)} 0.7px, transparent 0.9px)`,
          backgroundSize: "7px 7px",
          opacity: 0.16,
          translate: `${interpolate(
            frame,
            [0, durationInFrames],
            ["0px 0px", "7px 0px"],
          )}`,
        }}
      />

      <AbsoluteFill
        style={{
          backgroundImage: `
            linear-gradient(to bottom, ${rgba(props.backgroundColor, 0.52)} 0%, transparent 23%, transparent 76%, ${rgba(props.backgroundColor, 0.48)} 100%),
            radial-gradient(ellipse at center, transparent 40%, ${rgba(props.backgroundColor, 0.48)} 76%, ${rgba("#000000", 0.82)} 100%)
          `,
        }}
      />

      <AbsoluteFill
        style={{
          background: `linear-gradient(90deg, ${rgba(props.backgroundColor, 0.22)}, transparent 18%, transparent 82%, ${rgba(props.backgroundColor, 0.22)})`,
          mixBlendMode: "multiply",
        }}
      />
    </AbsoluteFill>
  );
};
