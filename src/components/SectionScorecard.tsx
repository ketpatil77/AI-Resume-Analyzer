import { AlignLeft, Briefcase, GraduationCap, Layout, User, Zap } from "lucide-react";
import type { SectionScores } from "../types/analysis";

interface SectionScorecardProps {
  scores: SectionScores;
}

const sections = [
  { key: "contact", label: "Contact Info", icon: User },
  { key: "summary", label: "Professional Summary", icon: AlignLeft },
  { key: "experience", label: "Work Experience", icon: Briefcase },
  { key: "skills", label: "Skills", icon: Zap },
  { key: "education", label: "Education", icon: GraduationCap },
  { key: "formatting", label: "Formatting", icon: Layout }
] as const;

function scoreColor(score: number) {
  if (score >= 7) return "var(--accent-green)";
  if (score >= 5) return "var(--accent-amber)";
  return "var(--accent-red)";
}

export function SectionScorecard({ scores }: SectionScorecardProps) {
  return (
    <section className="surface animate-fadeUp p-6 [animation-delay:80ms]">
      <h2 className="card-title mb-4">Section Scorecard</h2>
      <div className="space-y-4">
        {sections.map(({ key, label, icon: Icon }, index) => {
          const score = scores[key];
          return (
            <div key={key}>
              <div className="mb-2 flex items-center justify-between gap-3">
                <span className="flex items-center gap-2 text-sm font-semibold">
                  <Icon size={16} style={{ color: scoreColor(score) }} aria-hidden="true" />
                  {label}
                </span>
                <span className="score-number text-sm font-bold">{score}/10</span>
              </div>
              <div className="h-2 overflow-hidden rounded-full bg-[var(--bg-hover)]">
                <div
                  className="h-full rounded-full transition-[width] duration-700 ease-out"
                  style={{
                    width: `${Math.max(0, Math.min(score, 10)) * 10}%`,
                    background: scoreColor(score),
                    transitionDelay: `${index * 100}ms`
                  }}
                />
              </div>
            </div>
          );
        })}
      </div>
    </section>
  );
}
