import { CheckCircle2, PlusCircle } from "lucide-react";

interface SkillsAnalysisProps {
  matched: string[];
  missing: string[];
}

export function SkillsAnalysis({ matched, missing }: SkillsAnalysisProps) {
  return (
    <section className="surface animate-fadeUp p-6 [animation-delay:160ms]">
      <h2 className="card-title mb-4">Skills Analysis</h2>
      <div className="space-y-5">
        <div>
          <p className="mb-3 flex items-center gap-2 text-sm font-semibold text-[var(--accent-green)]">
            <CheckCircle2 size={16} aria-hidden="true" /> Matched Skills
          </p>
          <div className="flex flex-wrap gap-2">
            {matched.length ? matched.map((skill, index) => (
              <span key={skill} className="skill-tag matched" style={{ animationDelay: `${index * 50}ms` }}>
                {skill}
              </span>
            )) : <span className="caption">No strong matches found.</span>}
          </div>
        </div>
        <div>
          <p className="mb-3 flex items-center gap-2 text-sm font-semibold text-[var(--accent-amber)]">
            <PlusCircle size={16} aria-hidden="true" /> Missing Skills
          </p>
          <div className="flex flex-wrap gap-2">
            {missing.length ? missing.map((skill, index) => (
              <span key={skill} className="skill-tag missing" style={{ animationDelay: `${index * 50}ms` }}>
                + {skill}
              </span>
            )) : <span className="caption">No major gaps identified.</span>}
          </div>
        </div>
      </div>
    </section>
  );
}
