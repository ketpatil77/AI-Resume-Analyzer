import { Award, CircleAlert, TrendingUp } from "lucide-react";
import { useEffect, useMemo, useState } from "react";

interface ATSScoreMeterProps {
  score: number;
  verdict: string;
}

function zoneColor(score: number) {
  if (score < 50) return "var(--accent-red)";
  if (score < 75) return "var(--accent-amber)";
  return "var(--accent-green)";
}

export function ATSScoreMeter({ score, verdict }: ATSScoreMeterProps) {
  const [displayScore, setDisplayScore] = useState(0);
  const radius = 54;
  const circumference = 2 * Math.PI * radius;
  const strokeDashoffset = circumference - (score / 100) * circumference;
  const color = zoneColor(score);
  const Icon = score >= 75 ? Award : score >= 50 ? TrendingUp : CircleAlert;

  useEffect(() => {
    let frame = 0;
    const total = 50;
    const tick = () => {
      frame += 1;
      const eased = 1 - Math.pow(1 - frame / total, 3);
      setDisplayScore(Math.round(score * eased));
      if (frame < total) requestAnimationFrame(tick);
    };
    requestAnimationFrame(tick);
  }, [score]);

  const label = useMemo(() => {
    if (score >= 85) return "Excellent";
    if (score >= 75) return "Good";
    if (score >= 50) return "Needs Work";
    return "Poor";
  }, [score]);

  return (
    <section className="surface animate-fadeUp p-6">
      <div className="mb-4 flex items-center justify-between gap-3">
        <h2 className="card-title">ATS Score Meter</h2>
        <Icon style={{ color }} size={20} aria-hidden="true" />
      </div>
      <div className="flex flex-col items-center">
        <svg
          width="150"
          height="150"
          viewBox="0 0 150 150"
          role="img"
          aria-label={`ATS Score: ${score} out of 100`}
        >
          <circle
            cx="75"
            cy="75"
            r={radius}
            fill="none"
            stroke="var(--border)"
            strokeWidth="12"
          />
          <circle
            cx="75"
            cy="75"
            r={radius}
            fill="none"
            stroke={color}
            strokeLinecap="round"
            strokeWidth="12"
            strokeDasharray={circumference}
            strokeDashoffset={strokeDashoffset}
            transform="rotate(-90 75 75)"
            style={{ transition: "stroke-dashoffset 1.2s ease-out" }}
          />
          <text
            x="75"
            y="82"
            textAnchor="middle"
            className="score-number fill-[var(--text-primary)] text-[48px] font-bold"
          >
            {displayScore}
          </text>
        </svg>
        <p className="mt-2 text-sm font-semibold text-[var(--text-primary)]">ATS Score</p>
        <p className="caption mt-1">{verdict || label}</p>
      </div>
    </section>
  );
}
