import type { AnalysisResult, Priority } from "../types/analysis";

interface AnalysePayload {
  resumeText: string;
  jobDescription?: string;
}

const technicalSkills = [
  "python", "java", "javascript", "typescript", "react", "angular", "vue", "node", "express",
  "sql", "mysql", "postgresql", "mongodb", "excel", "power bi", "tableau", "looker",
  "machine learning", "deep learning", "data analysis", "data visualization", "statistics",
  "pandas", "numpy", "scikit-learn", "tensorflow", "pytorch", "aws", "azure", "gcp", "docker",
  "kubernetes", "git", "github", "html", "css", "tailwind", "django", "flask", "rest api",
  "graphql", "linux", "spark", "hadoop", "etl", "airflow", "jira", "figma"
];

const softSkills = [
  "communication", "leadership", "teamwork", "problem solving", "stakeholder", "collaboration",
  "ownership", "mentoring", "presentation", "documentation"
];

const actionVerbs = [
  "built", "created", "developed", "implemented", "designed", "optimized", "improved", "reduced",
  "increased", "automated", "managed", "led", "delivered", "launched", "analyzed", "migrated",
  "integrated", "tested", "deployed", "maintained", "trained", "collaborated"
];

const weakPhrases = [
  "hard working", "quick learner", "team player", "self motivated", "seeking a challenging",
  "responsible for", "good communication", "basic knowledge", "familiar with", "worked on"
];

const sectionAliases = {
  contact: [/email|phone|mobile|linkedin|github|portfolio/],
  summary: [/summary|profile|objective|about me|professional overview/],
  experience: [/experience|employment|work history|internship|professional experience/],
  skills: [/skills|technical skills|technologies|tools|competencies/],
  education: [/education|degree|university|college|bachelor|master|b\.?tech|bsc|msc|cgpa|gpa/],
  projects: [/projects|portfolio|case study|capstone/],
  certifications: [/certification|certificate|certified|coursework|training/]
};

const stopWords = new Set([
  "and", "the", "for", "with", "from", "that", "this", "you", "your", "are", "was", "were",
  "have", "has", "had", "will", "can", "job", "role", "work", "team", "using", "into", "more",
  "resume", "project", "skills", "experience", "education", "summary", "data", "company", "about",
  "their", "they", "them", "our", "all", "any", "who", "what", "when", "where", "which"
]);

function clamp(value: number, min: number, max: number) {
  return Math.max(min, Math.min(max, Math.round(value)));
}

function titleCase(value: string) {
  return value.split(" ").map((part) => part[0]?.toUpperCase() + part.slice(1)).join(" ");
}

function escapeRegExp(value: string) {
  return value.replace(/[.*+?^${}()|[\]\\]/g, "\\$&");
}

function includesTerm(text: string, term: string) {
  return new RegExp(`(^|[^a-z0-9+#.])${escapeRegExp(term)}([^a-z0-9+#.]|$)`, "i").test(text);
}

function countRegex(text: string, regex: RegExp) {
  return text.match(regex)?.length || 0;
}

function hasSection(text: string, key: keyof typeof sectionAliases) {
  return sectionAliases[key].some((pattern) => pattern.test(text));
}

function extractSkills(text: string, catalog = [...technicalSkills, ...softSkills]) {
  return catalog.filter((skill) => includesTerm(text, skill)).map(titleCase);
}

function getLines(text: string) {
  return text.split(/\n+/).map((line) => line.trim()).filter(Boolean);
}

function getBullets(lines: string[]) {
  return lines.filter((line) => /^[-*•▪●]|\b(built|created|developed|implemented|designed|optimized|improved|reduced|increased|automated|managed|led|delivered|launched|analyzed)\b/i.test(line));
}

function keywordList(text: string) {
  return [...new Set(text
    .toLowerCase()
    .replace(/[^a-z0-9+#.\s-]/g, " ")
    .split(/\s+/)
    .map((word) => word.trim())
    .filter((word) => word.length > 2 && !stopWords.has(word)))];
}

function extractKeywords(text: string, jdTerms: string[] = []) {
  const counts = new Map<string, number>();
  const lower = text.toLowerCase();

  for (const word of keywordList(lower)) {
    counts.set(word, countRegex(lower, new RegExp(`\\b${escapeRegExp(word)}\\b`, "g")));
  }

  for (const skill of [...technicalSkills, ...softSkills, ...jdTerms]) {
    const frequency = countRegex(lower, new RegExp(`\\b${escapeRegExp(skill)}\\b`, "gi"));
    if (frequency > 0) counts.set(skill, frequency + (counts.get(skill) || 0));
  }

  return [...counts.entries()]
    .filter(([, frequency]) => frequency > 0)
    .sort((a, b) => b[1] - a[1])
    .slice(0, 20)
    .map(([word, frequency]) => ({ word, frequency }));
}

function suggestion(text: string, priority: Priority) {
  return { text, priority };
}

function scoreVerdict(score: number): AnalysisResult["overall_verdict"] {
  if (score >= 88) return "Excellent";
  if (score >= 72) return "Good";
  if (score >= 50) return "Needs Work";
  return "Poor";
}

function hashText(value: string) {
  let hash = 0;
  for (let index = 0; index < value.length; index += 1) {
    hash = (hash * 31 + value.charCodeAt(index)) >>> 0;
  }
  return hash;
}

function pick<T>(items: T[], seed: number) {
  return items[seed % items.length];
}

function unique(items: string[], limit: number) {
  const seen = new Set<string>();
  return items.filter((item) => {
    const key = item.toLowerCase().replace(/\d+/g, "#");
    if (seen.has(key)) return false;
    seen.add(key);
    return true;
  }).slice(0, limit);
}

function jobTerms(jobDescription: string) {
  const base = keywordList(jobDescription).filter((word) => word.length > 3);
  const skills = technicalSkills.filter((skill) => includesTerm(jobDescription, skill));
  return [...new Set([...skills, ...base])].slice(0, 45);
}

function scoreResume(resumeText: string, jobDescription = "") {
  const raw = resumeText;
  const text = raw.toLowerCase();
  const jd = jobDescription.toLowerCase();
  const lines = getLines(raw);
  const bullets = getBullets(lines);
  const wordCount = keywordList(text).length;
  const numbers = countRegex(raw, /\b\d+([.%+xX]|,\d{3})?\b/g);
  const quantifiedBullets = bullets.filter((line) => /\b\d+([.%+xX]|,\d{3})?\b/.test(line)).length;
  const actionBulletCount = bullets.filter((line) => actionVerbs.some((verb) => includesTerm(line.toLowerCase(), verb))).length;
  const weakPhraseCount = weakPhrases.filter((phrase) => text.includes(phrase)).length;
  const matchedSkills = extractSkills(text);
  const jdKeywordTerms = jd ? jobTerms(jd) : [];
  const jdSkillTerms = jd ? technicalSkills.filter((skill) => includesTerm(jd, skill)) : [];
  const jdMatchedTerms = jdKeywordTerms.filter((term) => includesTerm(text, term));
  const jdMatchedSkills = jdSkillTerms.filter((skill) => includesTerm(text, skill)).map(titleCase);
  const missingSkills = jd
    ? jdSkillTerms.filter((skill) => !includesTerm(text, skill)).map(titleCase).slice(0, 12)
    : technicalSkills.filter((skill) => !includesTerm(text, skill)).map(titleCase).slice(0, 10);

  const contact = clamp(
    (/[a-z0-9._%+-]+@[a-z0-9.-]+\.[a-z]{2,}/i.test(raw) ? 3 : 0) +
      (/\+?\d[\d\s().-]{8,}/.test(raw) ? 2 : 0) +
      (text.includes("linkedin") ? 2 : 0) +
      (text.includes("github") || text.includes("portfolio") ? 2 : 0) +
      (lines.slice(0, 8).some((line) => line.length > 4 && line.length < 80) ? 1 : 0),
    0,
    10
  );

  const summary = clamp(
    (hasSection(text, "summary") ? 3 : 0) +
      (wordCount >= 180 ? 2 : wordCount >= 90 ? 1 : 0) +
      (numbers > 0 ? 2 : 0) +
      (matchedSkills.length >= 4 ? 2 : matchedSkills.length >= 2 ? 1 : 0) -
      (weakPhraseCount > 0 ? 2 : 0),
    0,
    10
  );

  const experience = clamp(
    (hasSection(text, "experience") ? 2 : 0) +
      (bullets.length >= 6 ? 2 : bullets.length >= 3 ? 1 : 0) +
      (actionBulletCount >= 5 ? 2 : actionBulletCount >= 2 ? 1 : 0) +
      (quantifiedBullets >= 3 ? 3 : quantifiedBullets >= 1 ? 1 : 0) +
      (hasSection(text, "projects") ? 1 : 0),
    0,
    10
  );

  const skills = clamp(
    (hasSection(text, "skills") ? 2 : 0) +
      (matchedSkills.length >= 12 ? 5 : matchedSkills.length >= 8 ? 4 : matchedSkills.length >= 5 ? 3 : matchedSkills.length >= 3 ? 2 : matchedSkills.length) +
      (jd ? (jdMatchedSkills.length >= 6 ? 3 : jdMatchedSkills.length >= 3 ? 2 : jdMatchedSkills.length >= 1 ? 1 : 0) : 2),
    0,
    10
  );

  const education = clamp(
    (hasSection(text, "education") ? 3 : 0) +
      (/(bachelor|master|degree|b\.?tech|m\.?tech|bsc|msc|mba|phd)/i.test(raw) ? 3 : 0) +
      (/(university|college|institute|school)/i.test(raw) ? 2 : 0) +
      (/(cgpa|gpa|grade|percentage|20\d{2})/i.test(raw) ? 2 : 0),
    0,
    10
  );

  const formatting = clamp(
    (wordCount >= 220 && wordCount <= 900 ? 2 : wordCount > 900 ? 1 : 0) +
      (["summary", "experience", "skills", "education"].filter((key) => hasSection(text, key as keyof typeof sectionAliases)).length * 1.5) +
      (bullets.length >= 4 ? 1 : 0) +
      (raw.includes("\t") ? -1 : 0) +
      (lines.some((line) => line.length > 180) ? -2 : 0),
    0,
    10
  );

  const jobMatchScore = jd
    ? clamp((jdMatchedTerms.length / Math.max(jdKeywordTerms.length, 1)) * 70 + (jdMatchedSkills.length / Math.max(jdSkillTerms.length, 1)) * 30, 0, 100)
    : null;

  const sectionWeighted =
    contact * 0.12 +
    summary * 0.13 +
    experience * 0.24 +
    skills * 0.22 +
    education * 0.09 +
    formatting * 0.2;

  const hardPenalty =
    (contact < 5 ? 7 : 0) +
    (experience < 5 ? 8 : 0) +
    (skills < 5 ? 6 : 0) +
    (formatting < 5 ? 6 : 0) +
    (weakPhraseCount >= 2 ? 4 : 0) +
    (jd && jobMatchScore !== null && jobMatchScore < 35 ? 10 : 0);

  const atsScore = clamp(sectionWeighted * 10 + (jd && jobMatchScore !== null ? (jobMatchScore - 50) * 0.18 : 0) - hardPenalty, 0, 100);

  return {
    scores: { contact, summary, experience, skills, education, formatting },
    atsScore,
    matchedSkills,
    missingSkills,
    jobMatchScore,
    jobMatchGaps: missingSkills,
    jdKeywordTerms,
    weakPhraseCount,
    bullets,
    quantifiedBullets,
    actionBulletCount,
    wordCount,
    numbers,
    longLineCount: lines.filter((line) => line.length > 180).length,
    missingSections: (["summary", "experience", "skills", "education"] as const).filter((key) => !hasSection(text, key)),
    topKeywords: extractKeywords(resumeText, jdKeywordTerms).slice(0, 6).map((item) => item.word)
  };
}

function buildResumeSummary(
  resumeText: string,
  result: ReturnType<typeof scoreResume>,
  hasJd: boolean
): AnalysisResult["resume_summary"] {
  const seed = hashText(resumeText + result.atsScore + result.matchedSkills.join("|"));
  const weakSections = Object.entries(result.scores)
    .filter(([, score]) => score < 6)
    .sort((a, b) => a[1] - b[1])
    .map(([section, score]) => `${titleCase(section)} (${score}/10)`);
  const strongSections = Object.entries(result.scores)
    .filter(([, score]) => score >= 8)
    .sort((a, b) => b[1] - a[1])
    .map(([section, score]) => `${titleCase(section)} (${score}/10)`);
  const topSkillText = result.matchedSkills.slice(0, 5).join(", ");
  const gapText = result.missingSkills.slice(0, 5).join(", ");
  const keywordText = result.topKeywords.slice(0, 4).join(", ");

  const headline = pick([
    `${scoreVerdict(result.atsScore)} profile: ${result.atsScore}/100 ATS, ${result.matchedSkills.length} skills found, ${result.quantifiedBullets} quantified bullets.`,
    `Resume signal: ${result.atsScore}/100. Strong in ${strongSections[0] || "no major section yet"}; weakest in ${weakSections[0] || "no critical section"}.`,
    `ATS read: ${result.atsScore}/100 with ${result.wordCount} keyword signals and ${result.missingSkills.length} visible skill gaps.`
  ], seed);

  const perfect = unique([
    ...(strongSections.length ? [`Best section strength: ${strongSections.join(", ")}.`] : []),
    result.matchedSkills.length >= 8
      ? `Skill coverage is solid: ${topSkillText}.`
      : result.matchedSkills.length >= 4
        ? `Core skills are visible: ${topSkillText}.`
        : "",
    result.scores.contact >= 8 ? "Contact block is recruiter-friendly: email/phone/profile links are detectable." : "",
    result.quantifiedBullets >= 3
      ? `Impact proof exists: ${result.quantifiedBullets} bullet(s) include numbers.`
      : "",
    result.scores.formatting >= 8 ? "ATS format looks clean: normal headings, bullets, and readable section structure." : "",
    keywordText ? `Keyword identity is clear: ${keywordText}.` : ""
  ].filter(Boolean), 5);

  const problems = unique([
    ...(weakSections.length ? [`Weak scoring sections: ${weakSections.join(", ")}.`] : []),
    result.quantifiedBullets < 2 ? `Low proof: only ${result.quantifiedBullets} quantified bullet(s). Recruiters cannot measure impact.` : "",
    result.actionBulletCount < 3 ? `Passive experience: only ${result.actionBulletCount} strong action-led bullet(s) detected.` : "",
    result.weakPhraseCount > 0 ? `Generic language found: ${result.weakPhraseCount} weak phrase(s). This lowers credibility.` : "",
    result.longLineCount > 0 ? `${result.longLineCount} line(s) are too long. ATS and humans scan them poorly.` : "",
    result.missingSections.length ? `Missing/unclear sections: ${result.missingSections.map(titleCase).join(", ")}.` : "",
    hasJd && result.jobMatchScore !== null && result.jobMatchScore < 60 ? `Role fit is weak: JD match is ${result.jobMatchScore}%.` : ""
  ].filter(Boolean), 6);

  const improvements = unique([
    gapText ? `Add only truthful missing skills and prove them in bullets: ${gapText}.` : "Keep skills grouped by language, framework, database, cloud, and tools.",
    result.quantifiedBullets < 3 ? "Rewrite 3-5 bullets with metric format: action + tool + result + number." : "Upgrade good bullets by tying numbers to business outcome.",
    result.scores.summary < 7 ? "Replace generic summary with 3 lines: target role, top stack/domain, strongest measured result." : "Tune first summary line to exact job title and domain.",
    result.scores.formatting < 7 ? "Use plain ATS structure: Summary, Skills, Experience, Projects, Education. Avoid tables/text boxes." : "Keep layout simple; do not hide key skills inside graphics.",
    hasJd ? "Mirror exact JD wording where true, especially tools, role title, and domain nouns." : "Paste a JD for sharper role-match gaps; current scan uses general ATS rules."
  ], 6);

  const ats_warnings = unique([
    result.scores.contact < 6 ? "ATS may miss contact/profile links." : "",
    result.scores.formatting < 6 ? "Formatting risk: complex layout may parse badly." : "",
    result.scores.experience < 6 ? "Experience proof risk: bullets do not show enough measurable outcomes." : "",
    result.scores.skills < 6 ? "Keyword risk: skills section is too thin for ATS filters." : "",
    hasJd && result.jobMatchScore !== null && result.jobMatchScore < 50 ? "JD filter risk: resume may fail role keyword screen." : ""
  ].filter(Boolean), 5);

  return {
    headline,
    perfect: perfect.length ? perfect : ["No standout section yet. Resume needs stronger proof before calling anything perfect."],
    problems: problems.length ? problems : ["No critical red flags found. Main work now is sharpening wording and role targeting."],
    improvements,
    ats_warnings: ats_warnings.length ? ats_warnings : ["No major ATS parsing warning from local scan."],
    evidence: [
      { label: "Skills found", value: String(result.matchedSkills.length), status: result.matchedSkills.length >= 8 ? "good" : result.matchedSkills.length >= 4 ? "warn" : "bad" },
      { label: "Numbered proof", value: String(result.quantifiedBullets), status: result.quantifiedBullets >= 3 ? "good" : result.quantifiedBullets >= 1 ? "warn" : "bad" },
      { label: "Action bullets", value: String(result.actionBulletCount), status: result.actionBulletCount >= 5 ? "good" : result.actionBulletCount >= 2 ? "warn" : "bad" },
      { label: "Weak phrases", value: String(result.weakPhraseCount), status: result.weakPhraseCount === 0 ? "good" : result.weakPhraseCount <= 1 ? "warn" : "bad" },
      { label: "JD match", value: result.jobMatchScore === null ? "N/A" : `${result.jobMatchScore}%`, status: result.jobMatchScore === null ? "warn" : result.jobMatchScore >= 70 ? "good" : result.jobMatchScore >= 50 ? "warn" : "bad" }
    ]
  };
}

export async function analyseResume({ resumeText, jobDescription }: AnalysePayload): Promise<AnalysisResult> {
  await new Promise((resolve) => setTimeout(resolve, 500));

  const result = scoreResume(resumeText, jobDescription || "");
  const hasJd = Boolean(jobDescription?.trim());
  const summaryPriority: Priority = result.scores.summary < 5 ? "high" : result.scores.summary < 7 ? "medium" : "low";
  const experiencePriority: Priority = result.scores.experience < 6 ? "high" : result.scores.experience < 8 ? "medium" : "low";
  const skillsPriority: Priority = result.scores.skills < 6 || result.missingSkills.length > 5 ? "high" : result.missingSkills.length > 2 ? "medium" : "low";

  return {
    ats_score: result.atsScore,
    overall_verdict: scoreVerdict(result.atsScore),
    section_scores: result.scores,
    matched_skills: result.matchedSkills.slice(0, 16),
    missing_skills: result.missingSkills.slice(0, 12),
    keywords: extractKeywords(resumeText, result.jdKeywordTerms),
    suggestions: {
      summary: [
        suggestion(
          result.scores.summary >= 8
            ? "Summary is strong. Keep it tight and align first sentence to the exact target role."
            : "Summary is weak. Add target role, years/level, top tools, domain, and one measurable outcome. Avoid generic lines.",
          summaryPriority
        ),
        suggestion(
          result.weakPhraseCount > 0
            ? "Remove generic phrases like hard working, quick learner, team player. Replace with proof and numbers."
            : "Keep the summary factual. No adjectives without evidence.",
          result.weakPhraseCount > 0 ? "high" : "medium"
        )
      ],
      experience: [
        suggestion(
          result.quantifiedBullets >= 3
            ? "Experience has measurable proof. Make sure each bullet states action, tool, and business result."
            : "Experience lacks measurable impact. Add numbers: accuracy, revenue, users, time saved, cost reduced, scale, or percentage improvement.",
          experiencePriority
        ),
        suggestion(
          result.actionBulletCount < 3
            ? "Too many passive bullets. Start bullets with strong verbs: built, automated, optimized, reduced, improved, deployed."
            : "Action verbs are present. Now remove weak responsibilities and keep outcome-based bullets.",
          result.actionBulletCount < 3 ? "high" : "medium"
        )
      ],
      skills: [
        suggestion(
          result.missingSkills.length
            ? `${hasJd ? "JD gap found" : "Common skill gap found"}: ${result.missingSkills.slice(0, 6).join(", ")}. Add only if true and prove in project/experience bullets.`
            : "Skill match is strong. Group skills by language, framework, database, tools, and domain.",
          skillsPriority
        ),
        suggestion(
          result.scores.formatting < 6
            ? "ATS formatting risk. Use simple headings, plain bullets, no tables, no text boxes, no icons for key data."
            : "Formatting looks ATS friendly. Keep section names simple and consistent.",
          result.scores.formatting < 6 ? "high" : "low"
        )
      ]
    },
    job_match_score: result.jobMatchScore,
    job_match_gaps: result.jobMatchGaps.slice(0, 8),
    resume_summary: buildResumeSummary(resumeText, result, hasJd)
  };
}
