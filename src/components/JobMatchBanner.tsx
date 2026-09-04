import { Target } from "lucide-react";

interface JobMatchBannerProps {
  score: number | null;
  gaps: string[];
  matchedCount: number;
}

function color(score: number) {
  if (score < 50) return "var(--accent-red)";
  if (score < 75) return "var(--accent-amber)";
  return "var(--accent-green)";
}

export function JobMatchBanner({ score, gaps, matchedCount }: JobMatchBannerProps) {
  if (score === null) return null;
  const c = color(score);

  return (
    <section className="surface animate-fadeUp p-5 [animation-delay:200ms]">
      <div className="mb-3 flex flex-wrap items-center justify-between gap-3">
        <p className="flex items-center gap-2 text-lg font-bold">
          <Target style={{ color: c }} size={22} aria-hidden="true" />
          Role Match Score: <span className="score-number" style={{ color: c }}>{score}%</span>
        </p>
        <p className="caption">
          {matchedCount} strong matches | {gaps.length} gaps identified
        </p>
      </div>
      <div className="h-3 overflow-hidden rounded-full bg-[var(--bg-hover)]" aria-label={`Role match score ${score} percent`}>
        <div className="h-full rounded-full transition-[width] duration-700 ease-out" style={{ width: `${score}%`, background: c }} />
      </div>
    </section>
  );
}
