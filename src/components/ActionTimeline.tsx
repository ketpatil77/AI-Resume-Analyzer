import { ArrowRight, Flame, ShieldCheck, Wrench } from "lucide-react";
import type { AnalysisResult, Priority } from "../types/analysis";

interface ActionTimelineProps {
  result: AnalysisResult;
}

function priorityRank(priority: Priority) {
  if (priority === "high") return 0;
  if (priority === "medium") return 1;
  return 2;
}

export function ActionTimeline({ result }: ActionTimelineProps) {
  const suggestions = [
    ...result.suggestions.summary.map((item) => ({ ...item, section: "Summary" })),
    ...result.suggestions.experience.map((item) => ({ ...item, section: "Experience" })),
    ...result.suggestions.skills.map((item) => ({ ...item, section: "Skills" }))
  ].sort((a, b) => priorityRank(a.priority) - priorityRank(b.priority)).slice(0, 5);

  return (
    <section className="surface p-6">
      <div className="mb-5 flex items-center justify-between gap-3">
        <div>
          <h2 className="section-title">Fix Timeline</h2>
          <p className="caption mt-1">Priority order. Brutal first, polish later.</p>
        </div>
        <ShieldCheck className="text-[var(--accent-green)]" size={22} aria-hidden="true" />
      </div>
      <div className="timeline">
        {suggestions.map((item, index) => {
          const Icon = item.priority === "high" ? Flame : item.priority === "medium" ? Wrench : ArrowRight;
          return (
            <article className="timeline-item" key={`${item.section}-${item.text}`}>
              <div className={`timeline-dot ${item.priority}`}>
                <Icon size={15} aria-hidden="true" />
              </div>
              <div className="min-w-0">
                <p className="text-sm font-bold text-[var(--text-primary)]">
                  Step {index + 1}: {item.section}
                </p>
                <p className="mt-1 text-sm leading-6 text-[var(--text-secondary)]">{item.text}</p>
              </div>
            </article>
          );
        })}
      </div>
    </section>
  );
}
