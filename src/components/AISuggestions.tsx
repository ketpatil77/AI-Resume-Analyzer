import { AlertTriangle, CheckCircle2, Info, Lightbulb } from "lucide-react";
import { useState } from "react";
import type { AnalysisResult, Priority, Suggestion } from "../types/analysis";

interface AISuggestionsProps {
  suggestions: AnalysisResult["suggestions"];
  rawResponse?: string;
}

const tabs = [
  { key: "summary", label: "Summary" },
  { key: "experience", label: "Experience" },
  { key: "skills", label: "Skills" }
] as const;

function priorityClass(priority: Priority) {
  if (priority === "high") return "bg-[color-mix(in_srgb,var(--accent-red)_18%,transparent)] text-[var(--accent-red)]";
  if (priority === "medium") return "bg-[color-mix(in_srgb,var(--accent-amber)_18%,transparent)] text-[var(--accent-amber)]";
  return "bg-[color-mix(in_srgb,var(--accent-green)_18%,transparent)] text-[var(--accent-green)]";
}

function PriorityIcon({ priority }: { priority: Priority }) {
  if (priority === "high") return <AlertTriangle size={16} aria-hidden="true" />;
  if (priority === "medium") return <Info size={16} aria-hidden="true" />;
  return <CheckCircle2 size={16} aria-hidden="true" />;
}

export function AISuggestions({ suggestions, rawResponse }: AISuggestionsProps) {
  const [active, setActive] = useState<(typeof tabs)[number]["key"]>("summary");
  const items: Suggestion[] = suggestions[active] || [];

  return (
    <section className="surface animate-fadeUp p-6 [animation-delay:220ms]">
      <div className="mb-4 flex flex-wrap items-center justify-between gap-3">
        <h2 className="section-title">AI Suggestions</h2>
        <div className="flex rounded-card border border-[var(--border)] bg-[var(--bg-secondary)] p-1">
          {tabs.map((tab) => (
            <button
              key={tab.key}
              type="button"
              className={`rounded-card px-3 py-2 text-sm font-semibold transition ${
                active === tab.key
                  ? "bg-[var(--accent-blue)] text-white"
                  : "text-[var(--text-secondary)] hover:bg-[var(--bg-hover)]"
              }`}
              onClick={() => setActive(tab.key)}
            >
              {tab.label}
            </button>
          ))}
        </div>
      </div>
      <div className="space-y-3">
        {items.length ? items.map((item, index) => (
          <details key={`${item.text}-${index}`} open={index === 0} className="rounded-card border border-[var(--border)] bg-[var(--bg-secondary)] p-4">
            <summary className="flex cursor-pointer list-none items-center justify-between gap-4">
              <span className="flex items-center gap-3 text-sm font-semibold">
                <Lightbulb className="text-[var(--accent-blue-light)]" size={18} aria-hidden="true" />
                {tabs.find((tab) => tab.key === active)?.label}
              </span>
              <span className={`inline-flex items-center gap-1 rounded-full px-2 py-1 text-xs font-bold uppercase ${priorityClass(item.priority)}`}>
                <PriorityIcon priority={item.priority} />
                {item.priority}
              </span>
            </summary>
            <p className="mt-3 text-sm leading-6 text-[var(--text-secondary)]">{item.text}</p>
          </details>
        )) : (
          <p className="caption">No suggestions in this section.</p>
        )}
      </div>
      {rawResponse ? (
        <details className="mt-4 rounded-card border border-[var(--border)] bg-[var(--bg-secondary)] p-4">
          <summary className="cursor-pointer text-sm font-semibold text-[var(--accent-amber)]">
            Raw AI response fallback
          </summary>
          <pre className="mt-3 max-h-56 overflow-auto whitespace-pre-wrap text-xs text-[var(--text-secondary)]">
            {rawResponse}
          </pre>
        </details>
      ) : null}
    </section>
  );
}
