import { BarChart3, TrendingUp } from "lucide-react";
import { useMemo, useState } from "react";
import type { AnalysisResult } from "../types/analysis";

interface ScoreAnalyticsProps {
  result: AnalysisResult;
}

const labels: Record<keyof AnalysisResult["section_scores"], string> = {
  contact: "Contact",
  summary: "Summary",
  experience: "Experience",
  skills: "Skills",
  education: "Education",
  formatting: "ATS Format"
};

function cssVar(name: string, fallback: string) {
  if (typeof window === "undefined") {
    return fallback;
  }
  const value = getComputedStyle(document.documentElement).getPropertyValue(name).trim();
  return value || fallback;
}

function clamp(value: number, min: number, max: number) {
  return Math.min(max, Math.max(min, value));
}

function polarPoint(cx: number, cy: number, radius: number, angle: number) {
  return {
    x: cx + Math.cos(angle) * radius,
    y: cy + Math.sin(angle) * radius
  };
}

function renderRadarSvg(data: { section: string; score: number }[], stroke: string, fill: string, grid: string, text: string) {
  const size = 320;
  const cx = size / 2;
  const cy = size / 2;
  const levels = 5;
  const maxRadius = 110;
  const angleOffset = -Math.PI / 2;
  const points = data.map((item, index) => {
    const angle = angleOffset + (Math.PI * 2 * index) / data.length;
    return polarPoint(cx, cy, (item.score / 10) * maxRadius, angle);
  });

  const polygon = points.map((point) => `${point.x},${point.y}`).join(" ");

  return (
    <svg viewBox={`0 0 ${size} ${size}`} className="h-full w-full" role="img" aria-label="Section score radar chart">
      <g opacity="0.9">
        {Array.from({ length: levels }, (_, level) => {
          const radius = ((level + 1) / levels) * maxRadius;
          const ring = data
            .map((_, index) => {
              const angle = angleOffset + (Math.PI * 2 * index) / data.length;
              const point = polarPoint(cx, cy, radius, angle);
              return `${point.x},${point.y}`;
            })
            .join(" ");
          return <polygon key={radius} points={ring} fill="none" stroke={grid} strokeWidth="1" strokeDasharray="4 4" />;
        })}
        {data.map((item, index) => {
          const angle = angleOffset + (Math.PI * 2 * index) / data.length;
          const lineEnd = polarPoint(cx, cy, maxRadius + 10, angle);
          const labelPoint = polarPoint(cx, cy, maxRadius + 30, angle);
          const align = Math.abs(Math.cos(angle)) < 0.3 ? "middle" : Math.cos(angle) > 0 ? "start" : "end";
          return (
            <g key={item.section}>
              <line x1={cx} y1={cy} x2={lineEnd.x} y2={lineEnd.y} stroke={grid} strokeWidth="1" />
              <text x={labelPoint.x} y={labelPoint.y} fill={text} fontSize="11" textAnchor={align} dominantBaseline="middle">
                {item.section}
              </text>
            </g>
          );
        })}
        <polygon points={polygon} fill={fill} fillOpacity="0.28" stroke={stroke} strokeWidth="3" />
        {points.map((point, index) => (
          <circle key={index} cx={point.x} cy={point.y} r="4" fill={stroke} />
        ))}
      </g>
      <text x={cx} y={cy} fill={text} fontSize="22" fontWeight="700" textAnchor="middle" dominantBaseline="middle">
        {Math.round(data.reduce((sum, item) => sum + item.score, 0) / data.length)}
      </text>
    </svg>
  );
}

function renderBarSvg(data: { section: string; score: number }[], fill: string, grid: string, text: string) {
  const width = 320;
  const height = 320;
  const chartHeight = 210;
  const chartWidth = 250;
  const left = 36;
  const top = 24;
  const maxBarWidth = chartWidth / data.length - 10;
  const maxValue = 10;

  return (
    <svg viewBox={`0 0 ${width} ${height}`} className="h-full w-full" role="img" aria-label="Section score bar chart">
      <line x1={left} y1={top + chartHeight} x2={left + chartWidth} y2={top + chartHeight} stroke={grid} />
      {Array.from({ length: 6 }, (_, index) => {
        const y = top + (chartHeight / 5) * index;
        const value = 10 - index * 2;
        return (
          <g key={y}>
            <line x1={left} y1={y} x2={left + chartWidth} y2={y} stroke={grid} strokeDasharray="4 4" />
            <text x={12} y={y + 4} fill={text} fontSize="10">
              {value}
            </text>
          </g>
        );
      })}
      {data.map((item, index) => {
        const barHeight = (item.score / maxValue) * chartHeight;
        const x = left + index * (maxBarWidth + 10);
        const y = top + chartHeight - barHeight;
        return (
          <g key={item.section}>
            <rect x={x} y={y} width={maxBarWidth} height={barHeight} rx="10" fill={fill} />
            <text x={x + maxBarWidth / 2} y={top + chartHeight + 22} fill={text} fontSize="10" textAnchor="middle">
              {item.section}
            </text>
            <text x={x + maxBarWidth / 2} y={y - 6} fill={text} fontSize="10" textAnchor="middle">
              {item.score.toFixed(1)}
            </text>
          </g>
        );
      })}
    </svg>
  );
}

function renderAreaSvg(data: { name: string; value: number }[], stroke: string, fill: string, grid: string, text: string) {
  const width = 360;
  const height = 320;
  const padding = 28;
  const chartWidth = width - padding * 2;
  const chartHeight = height - padding * 2 - 20;
  const maxValue = 100;
  const stepX = data.length > 1 ? chartWidth / (data.length - 1) : chartWidth;
  const points = data.map((item, index) => {
    const x = padding + stepX * index;
    const y = padding + chartHeight - (clamp(item.value, 0, maxValue) / maxValue) * chartHeight;
    return { x, y, value: item.value, name: item.name };
  });

  const path = points.map((point) => `${point.x},${point.y}`).join(" ");
  const areaPath = `M ${padding} ${padding + chartHeight} L ${points.map((point) => `${point.x} ${point.y}`).join(" L ")} L ${padding + chartWidth} ${padding + chartHeight} Z`;

  return (
    <svg viewBox={`0 0 ${width} ${height}`} className="h-full w-full" role="img" aria-label="ATS flow graph">
      {Array.from({ length: 5 }, (_, index) => {
        const y = padding + (chartHeight / 4) * index;
        return <line key={y} x1={padding} y1={y} x2={padding + chartWidth} y2={y} stroke={grid} strokeDasharray="4 4" />;
      })}
      <path d={areaPath} fill={fill} fillOpacity="0.28" />
      <polyline points={path} fill="none" stroke={stroke} strokeWidth="3" strokeLinejoin="round" strokeLinecap="round" />
      {points.map((point) => (
        <g key={point.name}>
          <circle cx={point.x} cy={point.y} r="4" fill={stroke} />
          <text x={point.x} y={height - 6} fill={text} fontSize="10" textAnchor="middle">
            {point.name}
          </text>
        </g>
      ))}
    </svg>
  );
}

export function ScoreAnalytics({ result }: ScoreAnalyticsProps) {
  const [mode, setMode] = useState<"radar" | "bars">("radar");
  const radarData = useMemo(
    () =>
      Object.entries(result.section_scores).map(([key, score]) => ({
        section: labels[key as keyof AnalysisResult["section_scores"]],
        score
      })),
    [result.section_scores]
  );
  const flowData = useMemo(
    () => [
      { name: "Contact", value: result.section_scores.contact * 10 },
      { name: "Content", value: Math.round(((result.section_scores.summary + result.section_scores.experience) / 20) * 100) },
      { name: "Skills", value: result.section_scores.skills * 10 },
      { name: "Format", value: result.section_scores.formatting * 10 },
      { name: "ATS", value: result.ats_score }
    ],
    [result.ats_score, result.section_scores]
  );

  const blue = cssVar("--accent-blue-light", "#60A5FA");
  const teal = cssVar("--accent-teal", "#14B8A6");
  const amber = cssVar("--accent-amber", "#F59E0B");
  const grid = cssVar("--border", "#2A2D3A");
  const text = cssVar("--text-secondary", "#94A3B8");

  return (
    <section className="grid gap-4 lg:grid-cols-[0.9fr_1.1fr]">
      <div className="surface chart-card p-6">
        <div className="mb-4 flex items-center justify-between gap-3">
          <div>
            <h2 className="card-title">Interactive Score Graph</h2>
            <p className="caption mt-1">Switch graph type. Hover for exact score.</p>
          </div>
          <BarChart3 className="text-[var(--accent-blue-light)]" size={20} aria-hidden="true" />
        </div>
        <div className="chart-switch mb-4" role="tablist" aria-label="Score chart mode">
          <button type="button" className={mode === "radar" ? "active" : ""} onClick={() => setMode("radar")}>
            Radar
          </button>
          <button type="button" className={mode === "bars" ? "active" : ""} onClick={() => setMode("bars")}>
            Bars
          </button>
        </div>
        <div className="h-[280px]">
          {mode === "radar" ? renderRadarSvg(radarData, blue, blue, grid, text) : renderBarSvg(radarData, amber, grid, text)}
        </div>
      </div>
      <div className="surface chart-card p-6">
        <div className="mb-4 flex items-center justify-between gap-3">
          <h2 className="card-title">ATS Flow Graph</h2>
          <TrendingUp className="text-[var(--accent-teal)]" size={20} aria-hidden="true" />
        </div>
        <div className="h-[280px]">
          {renderAreaSvg(flowData, teal, teal, grid, text)}
        </div>
      </div>
    </section>
  );
}
