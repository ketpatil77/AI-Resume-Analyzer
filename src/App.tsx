import { AlertCircle } from "lucide-react";
import { useState, type FormEvent } from "react";
import { AISuggestions } from "./components/AISuggestions";
import { AnalyseButton } from "./components/AnalyseButton";
import { ATSScoreMeter } from "./components/ATSScoreMeter";
import { ActionTimeline } from "./components/ActionTimeline";
import { DynamicBackdrop } from "./components/DynamicBackdrop";
import { ExportButton } from "./components/ExportButton";
import { Header } from "./components/Header";
import { InsightTicker } from "./components/InsightTicker";
import { JDInput } from "./components/JDInput";
import { JobMatchBanner } from "./components/JobMatchBanner";
import { KeywordHeatmap } from "./components/KeywordHeatmap";
import { ScoreAnalytics } from "./components/ScoreAnalytics";
import { ScrollReveal } from "./components/ScrollReveal";
import { ScrollProgress } from "./components/ScrollProgress";
import { SectionScorecard } from "./components/SectionScorecard";
import { SkillsAnalysis } from "./components/SkillsAnalysis";
import { ResumeSummary } from "./components/ResumeSummary";
import { ResumeDNA } from "./components/ResumeDNA";
import { UploadZone } from "./components/UploadZone";
import { useResumeParser } from "./hooks/useResumeParser";
import { useTheme } from "./hooks/useTheme";
import { analyseResume } from "./lib/analyseResume";
import type { AnalysisResult } from "./types/analysis";

function App() {
  const { theme, toggleTheme } = useTheme();
  const { resume, parseFile, parseError, isParsing, clearResume } = useResumeParser();
  const [jobDescription, setJobDescription] = useState("");
  const [result, setResult] = useState<AnalysisResult | null>(null);
  const [error, setError] = useState("");
  const [loading, setLoading] = useState(false);
  const [adminOpen, setAdminOpen] = useState(false);
  const [adminEmail, setAdminEmail] = useState("");
  const [adminPassword, setAdminPassword] = useState("");
  const [adminError, setAdminError] = useState("");
  const [adminUnlocked, setAdminUnlocked] = useState(false);

  const adminUsername = import.meta.env.VITE_DEMO_ADMIN_USERNAME ?? "";
  const adminSecret = import.meta.env.VITE_DEMO_ADMIN_PASSWORD ?? "";

  const handleAnalyse = async () => {
    setError("");

    if (!resume) {
      setError("Upload a resume before analysis.");
      return;
    }

    if (resume.text.length < 100) {
      setError("Resume seems too short.");
      return;
    }

    setLoading(true);
    try {
      const analysis = await analyseResume({
        resumeText: resume.text,
        jobDescription: jobDescription.trim() || undefined
      });
      setResult(analysis);
      requestAnimationFrame(() => {
        document.getElementById("results-dashboard")?.scrollIntoView({ behavior: "smooth", block: "start" });
      });
    } catch (err) {
      setError(err instanceof Error ? err.message : "Analysis failed. Please try again.");
    } finally {
      setLoading(false);
    }
  };

  const handleAdminSubmit = (event: FormEvent<HTMLFormElement>) => {
    event.preventDefault();
    setAdminError("");

    if (adminUsername && adminSecret && adminEmail.trim() === adminUsername && adminPassword === adminSecret) {
      setAdminUnlocked(true);
      setAdminOpen(false);
      return;
    }

    setAdminUnlocked(false);
    setAdminError("Invalid admin credentials.");
  };

  return (
    <main className="app-shell">
      <DynamicBackdrop />
      <ScrollProgress />
      <Header
        theme={theme}
        onToggleTheme={toggleTheme}
        onAdminClick={() => {
          setAdminOpen((open) => !open);
        }}
      />

      {adminOpen ? (
        <section className="surface mb-4 border border-[var(--border)] p-4">
          <div className="mb-3 flex items-end justify-between gap-3">
            <div>
              <h2 className="font-display text-xl font-bold">Admin Login</h2>
              <p className="caption mt-1">Use the new admin creds.</p>
            </div>
            <button
              type="button"
              className="rounded-full border border-[var(--border)] px-3 py-1 text-xs font-semibold text-[var(--text-primary)]"
              onClick={() => setAdminOpen(false)}
            >
              Close
            </button>
          </div>
          <form className="grid gap-3 md:grid-cols-[1fr_1fr_auto]" onSubmit={handleAdminSubmit}>
            <input
              className="rounded-card border border-[var(--border)] bg-[var(--bg-secondary)] px-4 py-3 text-sm text-[var(--text-primary)] outline-none"
              placeholder="Admin username"
              value={adminEmail}
              onChange={(event) => setAdminEmail(event.target.value)}
            />
            <input
              className="rounded-card border border-[var(--border)] bg-[var(--bg-secondary)] px-4 py-3 text-sm text-[var(--text-primary)] outline-none"
              placeholder="Admin password"
              type="password"
              value={adminPassword}
              onChange={(event) => setAdminPassword(event.target.value)}
            />
            <button type="submit" className="rounded-card bg-[var(--accent-blue)] px-5 py-3 font-semibold text-white">
              Unlock
            </button>
          </form>
          {adminError ? <p className="mt-3 text-sm font-semibold text-[var(--accent-red)]">{adminError}</p> : null}
          {adminUnlocked ? <p className="mt-3 text-sm font-semibold text-[var(--accent-blue)]">Admin unlocked.</p> : null}
        </section>
      ) : null}

      <div className="grid gap-4 lg:grid-cols-[1.2fr_0.8fr]">
        <UploadZone
          resume={resume}
          error={parseError}
          isParsing={isParsing}
          onFile={parseFile}
          onClear={() => {
            clearResume();
            setResult(null);
          }}
        />
        <div className="flex flex-col gap-4">
          <JDInput value={jobDescription} onChange={setJobDescription} />
          <div className="surface p-4">
            <AnalyseButton disabled={!resume || isParsing} loading={loading} onClick={handleAnalyse} />
            {error ? (
              <p className="mt-3 flex items-center gap-2 text-sm font-semibold text-[var(--accent-red)]">
                <AlertCircle size={16} aria-hidden="true" />
                {error}
              </p>
            ) : null}
          </div>
        </div>
      </div>

      {result ? (
        <section id="results-dashboard" className="mt-8 scroll-mt-6">
          <div className="mb-4 flex flex-wrap items-end justify-between gap-3">
            <div>
              <h2 className="font-display text-[32px] font-bold tracking-normal">Results Dashboard</h2>
              <p className="caption mt-1">Scores, gaps, keywords, and action plan from the latest analysis.</p>
            </div>
          </div>

          <InsightTicker result={result} />

          <ScrollReveal>
            <div className="results-grid">
              <ATSScoreMeter score={result.ats_score} verdict={result.overall_verdict} />
              <SectionScorecard scores={result.section_scores} />
              <SkillsAnalysis matched={result.matched_skills} missing={result.missing_skills} />
            </div>
          </ScrollReveal>

          <ScrollReveal className="mt-4" delay={80}>
            <JobMatchBanner
              score={result.job_match_score}
              gaps={result.job_match_gaps}
              matchedCount={result.matched_skills.length}
            />
          </ScrollReveal>

          <ScrollReveal className="mt-4" delay={120}>
            <ScoreAnalytics result={result} />
          </ScrollReveal>

          <ScrollReveal className="mt-4" delay={140}>
            <ResumeDNA result={result} />
          </ScrollReveal>

          <ScrollReveal className="dashboard-grid mt-4" delay={160}>
            <AISuggestions suggestions={result.suggestions} rawResponse={result.raw_response} />
            <KeywordHeatmap keywords={result.keywords} />
          </ScrollReveal>

          <ScrollReveal className="mt-4" delay={200}>
            <ActionTimeline result={result} />
          </ScrollReveal>

          <ScrollReveal className="mt-4" delay={240}>
            <ResumeSummary result={result} />
          </ScrollReveal>

          <ExportButton />
        </section>
      ) : (
        <section className="mt-8 rounded-card border border-[var(--border)] bg-[var(--bg-secondary)] p-6 text-center">
          <p className="break-words font-semibold text-[var(--text-primary)]">Upload a resume to unlock the dashboard.</p>
          <p className="caption mt-1">No analysis data is saved in localStorage.</p>
        </section>
      )}
    </main>
  );
}

export default App;
