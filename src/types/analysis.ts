export type Verdict = "Excellent" | "Good" | "Needs Work" | "Poor";
export type Priority = "high" | "medium" | "low";

export interface SectionScores {
  contact: number;
  summary: number;
  experience: number;
  skills: number;
  education: number;
  formatting: number;
}

export interface KeywordStat {
  word: string;
  frequency: number;
}

export interface Suggestion {
  text: string;
  priority: Priority;
}

export interface AnalysisResult {
  ats_score: number;
  overall_verdict: Verdict;
  section_scores: SectionScores;
  matched_skills: string[];
  missing_skills: string[];
  keywords: KeywordStat[];
  suggestions: {
    summary: Suggestion[];
    experience: Suggestion[];
    skills: Suggestion[];
  };
  job_match_score: number | null;
  job_match_gaps: string[];
  resume_summary: {
    headline: string;
    perfect: string[];
    problems: string[];
    improvements: string[];
    ats_warnings: string[];
    evidence: Array<{
      label: string;
      value: string;
      status: "good" | "warn" | "bad";
    }>;
  };
  raw_response?: string;
}

export interface ResumeFileState {
  file: File;
  text: string;
}
