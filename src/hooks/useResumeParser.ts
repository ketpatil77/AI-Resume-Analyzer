import { useCallback, useState } from "react";
import * as pdfjs from "pdfjs-dist";
import pdfWorker from "pdfjs-dist/build/pdf.worker.mjs?url";
import mammoth from "mammoth";
import type { ResumeFileState } from "../types/analysis";

pdfjs.GlobalWorkerOptions.workerSrc = pdfWorker;

const allowedTypes = [
  "application/pdf",
  "application/vnd.openxmlformats-officedocument.wordprocessingml.document"
];

export function useResumeParser() {
  const [resume, setResume] = useState<ResumeFileState | null>(null);
  const [parseError, setParseError] = useState("");
  const [isParsing, setIsParsing] = useState(false);

  const parseFile = useCallback(async (file: File) => {
    setParseError("");
    setIsParsing(true);

    try {
      const isPdf = file.type === "application/pdf" || file.name.toLowerCase().endsWith(".pdf");
      const isDocx =
        file.type === allowedTypes[1] || file.name.toLowerCase().endsWith(".docx");

      if (!isPdf && !isDocx) {
        throw new Error("Only PDF and DOCX files are supported.");
      }

      const buffer = await file.arrayBuffer();
      let text = "";

      if (isPdf) {
        const pdf = await pdfjs.getDocument({ data: buffer }).promise;
        const pages: string[] = [];
        for (let pageNumber = 1; pageNumber <= pdf.numPages; pageNumber += 1) {
          const page = await pdf.getPage(pageNumber);
          const content = await page.getTextContent();
          pages.push(content.items.map((item) => ("str" in item ? item.str : "")).join(" "));
        }
        text = pages.join("\n\n");
      } else {
        const result = await mammoth.extractRawText({ arrayBuffer: buffer });
        text = result.value;
      }

      if (text.trim().length < 100) {
        throw new Error("Resume seems too short. Upload a complete PDF or DOCX resume.");
      }

      const nextResume = { file, text: text.trim() };
      setResume(nextResume);
      return nextResume;
    } catch (error) {
      const message = error instanceof Error ? error.message : "Could not parse resume.";
      setParseError(message);
      setResume(null);
      throw error;
    } finally {
      setIsParsing(false);
    }
  }, []);

  return { resume, parseFile, parseError, isParsing, clearResume: () => setResume(null) };
}
