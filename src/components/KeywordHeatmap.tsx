import type { KeywordStat } from "../types/analysis";

interface KeywordHeatmapProps {
  keywords: KeywordStat[];
}

export function KeywordHeatmap({ keywords }: KeywordHeatmapProps) {
  const top = [...keywords].sort((a, b) => b.frequency - a.frequency).slice(0, 20);
  const max = Math.max(...top.map((keyword) => keyword.frequency), 1);

  return (
    <section className="surface animate-fadeUp p-6 [animation-delay:260ms]">
      <h2 className="card-title mb-4">Keyword Heatmap</h2>
      <div className="flex flex-wrap gap-2">
        {top.length ? top.map((keyword) => {
          const weight = keyword.frequency / max;
          const size = 12 + weight * 10;
          const alpha = 12 + weight * 30;
          return (
            <span
              key={keyword.word}
              className="rounded-card border border-[var(--border)] px-3 py-2 font-semibold text-[var(--accent-blue-light)]"
              style={{
                fontSize: `${size}px`,
                background: `color-mix(in srgb, var(--accent-blue) ${alpha}%, transparent)`
              }}
              title={`Found ${keyword.frequency} times`}
            >
              {keyword.word}
            </span>
          );
        }) : <p className="caption">No keywords returned.</p>}
      </div>
    </section>
  );
}
