import { FileCheck2, UploadCloud, XCircle } from "lucide-react";
import { useRef, useState } from "react";
import type { ResumeFileState } from "../types/analysis";

interface UploadZoneProps {
  resume: ResumeFileState | null;
  error: string;
  isParsing: boolean;
  onFile: (file: File) => Promise<ResumeFileState>;
  onClear: () => void;
}

function formatSize(bytes: number) {
  if (bytes < 1024 * 1024) return `${(bytes / 1024).toFixed(1)} KB`;
  return `${(bytes / (1024 * 1024)).toFixed(1)} MB`;
}

export function UploadZone({ resume, error, isParsing, onFile, onClear }: UploadZoneProps) {
  const inputRef = useRef<HTMLInputElement | null>(null);
  const [isDragging, setIsDragging] = useState(false);

  const handleFile = async (file?: File) => {
    if (!file) return;
    await onFile(file).catch(() => undefined);
  };

  return (
    <section className="surface upload-panel p-6">
      <div className="mb-4">
        <h2 className="section-title">Upload Resume</h2>
        <p className="caption mt-1">PDF or DOCX. Text parsed locally before analysis.</p>
      </div>
      <button
        type="button"
        className={`flex min-h-[220px] w-full flex-col items-center justify-center gap-4 rounded-card border-2 border-dashed p-6 text-center transition-all ${
          isDragging ? "scale-[1.02] border-[var(--accent-blue)] bg-[var(--bg-hover)]" : "border-[var(--border)] bg-[var(--bg-secondary)]"
        }`}
        onClick={() => inputRef.current?.click()}
        onDragOver={(event) => {
          event.preventDefault();
          setIsDragging(true);
        }}
        onDragLeave={() => setIsDragging(false)}
        onDrop={(event) => {
          event.preventDefault();
          setIsDragging(false);
          void handleFile(event.dataTransfer.files[0]);
        }}
        aria-label="Upload PDF or DOCX resume"
      >
        {resume ? (
          <>
            <FileCheck2 className="text-[var(--accent-green)]" size={42} aria-hidden="true" />
            <div>
              <p className="font-semibold text-[var(--text-primary)]">{resume.file.name}</p>
              <p className="caption mt-1">
                {formatSize(resume.file.size)} | {resume.text.length.toLocaleString()} parsed characters
              </p>
            </div>
          </>
        ) : (
          <>
            <UploadCloud className="text-[var(--accent-blue-light)]" size={46} aria-hidden="true" />
            <div>
              <p className="font-semibold text-[var(--text-primary)]">
                {isParsing ? "Parsing resume..." : "Drop resume here or click to browse"}
              </p>
              <p className="caption mt-1">Supports .pdf and .docx files</p>
            </div>
          </>
        )}
      </button>
      <input
        ref={inputRef}
        className="hidden"
        type="file"
        accept=".pdf,.docx,application/pdf,application/vnd.openxmlformats-officedocument.wordprocessingml.document"
        onChange={(event) => void handleFile(event.target.files?.[0])}
      />
      <div className="mt-3 min-h-6">
        {error ? (
          <p className="flex items-center gap-2 text-sm font-medium text-[var(--accent-red)]">
            <XCircle size={16} aria-hidden="true" /> {error}
          </p>
        ) : resume ? (
          <button
            type="button"
            className="text-sm font-semibold text-[var(--accent-blue-light)]"
            onClick={onClear}
          >
            Remove file
          </button>
        ) : null}
      </div>
    </section>
  );
}
