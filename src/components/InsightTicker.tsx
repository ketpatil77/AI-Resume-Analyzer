import { Activity, AlertTriangle, CheckCircle2, Radar, Sparkles } from "lucide-react";
import type { AnalysisResult } from "../types/analysis";

interface InsightTickerProps {
  result: AnalysisResult;
}

export function InsightTicker({ result }: InsightTickerProps) {
  const weakSections = Object.entries(result.section_scores)
    .filter(([, score]) => score < 6)
    .map(([name]) => name);
  const items = [
    {
      icon: result.ats_score >= 72 ? CheckCircle2 : AlertTriangle,
      text: `ATS verdict: ${result.overall_verdict} (${result.ats_score}/100)`
    },
    {
      icon: Radar,
      text: result.job_match_score === null ? "Role match: add JD for target-role score" : `Role match: ${result.job_match_score}%`
    },
    {
      icon: Activity,
      text: weakSections.length ? `Weak sections: ${weakSections.join(", ")}` : "No section below 6/10"
    },
    {
      icon: Sparkles,
      text: result.missing_skills.length ? `Top gap: ${result.missing_skills[0]}` : "Skill coverage strong"
    }
  ];
  const loop = [...items, ...items];

  return (
    <section className="ticker-shell mb-4" aria-label="Live analysis insights">
      <div className="ticker-track">
        {loop.map((item, index) => {
          const Icon = item.icon;
          return (
            <span className="ticker-pill" key={`${item.text}-${index}`}>
              <Icon size={16} aria-hidden="true" />
              {item.text}
            </span>
          );
        })}
      </div>
    </section>
  );
}
