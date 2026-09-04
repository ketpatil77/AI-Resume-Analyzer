import { Loader2, Sparkles } from "lucide-react";

interface AnalyseButtonProps {
  disabled: boolean;
  loading: boolean;
  onClick: () => void;
}

export function AnalyseButton({ disabled, loading, onClick }: AnalyseButtonProps) {
  return (
    <button
      type="button"
      className="btn-primary w-full"
      disabled={disabled || loading}
      onClick={onClick}
      aria-label="Analyse resume"
    >
      {loading ? (
        <>
          <Loader2 className="animate-spin" size={20} aria-hidden="true" />
          Analysing your resume...
        </>
      ) : (
        <>
          <Sparkles size={20} aria-hidden="true" />
          Analyse Resume
        </>
      )}
    </button>
  );
}
