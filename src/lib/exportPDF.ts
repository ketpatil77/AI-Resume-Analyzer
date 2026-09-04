export async function exportReport(elementId = "results-dashboard") {
  const element = document.getElementById(elementId);
  if (!element) {
    throw new Error("Report area not found.");
  }
  const title = "AI Resume Analyzer Report";
  const body = element.innerText.replace(/\n{3,}/g, "\n\n").trim();
  const report = `${title}\n${"=".repeat(title.length)}\n\n${body}\n`;
  const blob = new Blob([report], { type: "text/plain;charset=utf-8" });
  const url = URL.createObjectURL(blob);
  const anchor = document.createElement("a");
  anchor.href = url;
  anchor.download = `resume-analysis-${Date.now()}.txt`;
  anchor.click();
  URL.revokeObjectURL(url);
}
