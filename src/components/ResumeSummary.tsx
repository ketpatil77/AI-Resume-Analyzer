import { AlertOctagon, CheckCircle2, ClipboardList, Gauge, Hammer, ShieldAlert } from "lucide-react";
import { useMemo, useState } from "react";
import type { AnalysisResult } from "../types/analysis";

interface ResumeSummaryProps {
  result: AnalysisResult;
}

const tabs = [
  { id: "perfect", label: "Perfect", icon: CheckCircle2 },
  { id: "problems", label: "Wrong", icon: AlertOctagon },
  { id: "improvements", label: "Improve", icon: Hammer },
  { id: "ats_warnings", label: "ATS Risk", icon: ShieldAlert }
] as const;

type TabId = (typeof tabs)[number]["id"];

function evidenceClass(status: "good" | "warn" | "bad") {
  if (status === "good") return "summary-evidence good";
  if (status === "warn") return "summary-evidence warn";
  return "summary-evidence bad";
}

export function ResumeSummary({ result }: ResumeSummaryProps) {
  const [active, setActive] = useState<TabId>("problems");
  const activeTab = tabs.find((tab) => tab.id === active) || tabs[0];
  const Icon = activeTab.icon;
  const items = result.resume_summary[active];

  const verdictTone = useMemo(() => {
    if (result.ats_score >= 72) return "good";
    if (result.ats_score >= 50) return "warn";
    return "bad";
  }, [result.ats_score]);

  return (
    <section className="surface summary-panel p-6">
      <div className="mb-5 flex flex-wrap items-start justify-between gap-4">
        <div className="max-w-3xl">
          <div className="mb-2 flex items-center gap-2 text-[var(--accent-blue-light)]">
            <ClipboardList size={20} aria-hidden="true" />
            <span className="caption uppercase tracking-[0.18em]">Resume Summary</span>
          </div>
          <h2 className="section-title">What is right, what is wrong, what to fix</h2>
          <p className="mt-2 text-sm leading-6 text-[var(--text-secondary)]">{result.resume_summary.headline}</p>
        </div>
        <div className={`summary-score ${verdictTone}`}>
          <Gauge size={20} aria-hidden="true" />
          <span className="score-number">{result.ats_score}</span>
          <small>{result.overall_verdict}</small>
        </div>
      </div>

      <div className="summary-evidence-grid mb-5">
        {result.resume_summary.evidence.map((item) => (
          <div className={evidenceClass(item.status)} key={item.label}>
            <span>{item.label}</span>
            <strong>{item.value}</strong>
          </div>
        ))}
      </div>

      <div className="summary-tabs" role="tablist" aria-label="Resume summary sections">
        {tabs.map((tab) => {
          const TabIcon = tab.icon;
          return (
            <button
              key={tab.id}
              type="button"
              role="tab"
              aria-selected={active === tab.id}
              className={`summary-tab ${active === tab.id ? "active" : ""}`}
              onClick={() => setActive(tab.id)}
            >
              <TabIcon size={16} aria-hidden="true" />
              {tab.label}
            </button>
          );
        })}
      </div>

      <div className="summary-list" key={active}>
        {items.map((item, index) => (
          <article className={`summary-item ${active}`} style={{ animationDelay: `${index * 70}ms` }} key={item}>
            <span className="summary-item-index">{String(index + 1).padStart(2, "0")}</span>
            <div>
              <p className="mb-1 flex items-center gap-2 text-sm font-bold text-[var(--text-primary)]">
                <Icon size={16} aria-hidden="true" />
                {activeTab.label}
              </p>
              <p className="text-sm leading-6 text-[var(--text-secondary)]">{item}</p>
            </div>
          </article>
        ))}
      </div>
    </section>
  );
}
