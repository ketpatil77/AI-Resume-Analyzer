import { ChevronDown, Target } from "lucide-react";
import { useState } from "react";

interface JDInputProps {
  value: string;
  onChange: (value: string) => void;
}

export function JDInput({ value, onChange }: JDInputProps) {
  const [open, setOpen] = useState(false);

  return (
    <section className="surface p-6">
      <button
        type="button"
        className="flex w-full items-center justify-between gap-4 text-left"
        onClick={() => setOpen((current) => !current)}
        aria-expanded={open}
      >
        <span className="flex items-center gap-3">
          <Target className="text-[var(--accent-teal)]" size={22} aria-hidden="true" />
          <span>
            <span className="section-title block">Add Job Description</span>
            <span className="caption mt-1 block">Optional role match analysis</span>
          </span>
        </span>
        <ChevronDown
          className={`shrink-0 transition-transform ${open ? "rotate-180" : ""}`}
          size={22}
          aria-hidden="true"
        />
      </button>
      {open ? (
        <textarea
          className="mt-4 min-h-[200px] w-full resize-y rounded-card border border-[var(--border)] bg-[var(--bg-secondary)] p-4 text-sm text-[var(--text-primary)] placeholder:text-[var(--text-muted)]"
          value={value}
          onChange={(event) => onChange(event.target.value)}
          placeholder="Paste the job description here..."
          aria-label="Job description"
        />
      ) : null}
    </section>
  );
}
