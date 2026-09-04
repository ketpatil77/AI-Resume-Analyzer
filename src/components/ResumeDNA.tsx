import { Dna, Info } from "lucide-react";
import { useState } from "react";
import type { AnalysisResult } from "../types/analysis";

interface ResumeDNAProps {
  result: AnalysisResult;
}

const sectionLabels: Record<keyof AnalysisResult["section_scores"], string> = {
  contact: "Contact",
  summary: "Summary",
  experience: "Experience",
  skills: "Skills",
  education: "Education",
  formatting: "ATS Format"
};

function tone(score: number) {
  if (score >= 7) return "good";
  if (score >= 5) return "warn";
  return "bad";
}

export function ResumeDNA({ result }: ResumeDNAProps) {
  const entries = Object.entries(result.section_scores) as Array<[keyof AnalysisResult["section_scores"], number]>;
  const [active, setActive] = useState(entries[0][0]);
  const activeScore = result.section_scores[active];

  return (
    <section className="surface dna-panel p-6">
      <div className="mb-4 flex items-center justify-between gap-3">
        <div>
          <h2 className="section-title">Resume DNA</h2>
          <p className="caption mt-1">Click any section chip to inspect its signal.</p>
        </div>
        <Dna className="text-[var(--accent-teal)]" size={24} aria-hidden="true" />
      </div>
      <div className="dna-stage">
        <div className="dna-orbit">
          <div className={`dna-core ${tone(activeScore)}`}>
            <strong>{activeScore}/10</strong>
            <span>{sectionLabels[active]}</span>
          </div>
          <div className="dna-node-grid">
          {entries.map(([key, score], index) => (
            <button
              key={key}
              type="button"
              className={`dna-node ${tone(score)} ${active === key ? "active" : ""}`}
              onClick={() => setActive(key)}
              aria-label={`${sectionLabels[key]} score ${score} out of 10`}
            >
              <span>{score}</span>
            </button>
          ))}
          </div>
        </div>
        <div className="dna-readout">
          <p className="flex items-center gap-2 text-sm font-bold text-[var(--text-primary)]">
            <Info size={16} aria-hidden="true" />
            {sectionLabels[active]} signal
          </p>
          <p className="mt-2 text-sm leading-6 text-[var(--text-secondary)]">
            {activeScore >= 8
              ? "Strong. Keep this section clean and do not over-edit."
              : activeScore >= 5
                ? "Average. Add proof, keywords, and cleaner wording."
                : "Weak. This section can block ATS and recruiter trust."}
          </p>
        </div>
      </div>
    </section>
  );
}
