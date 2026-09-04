import { Download, Loader2 } from "lucide-react";
import { useState } from "react";
import { exportReport } from "../lib/exportPDF";

export function ExportButton() {
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  const handleExport = async () => {
    setError("");
    setLoading(true);
    try {
      await exportReport();
    } catch (err) {
      setError(err instanceof Error ? err.message : "Report export failed.");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="mt-6">
      <button type="button" className="btn-primary w-full sm:w-auto sm:px-6" onClick={handleExport} disabled={loading}>
        {loading ? <Loader2 className="animate-spin" size={18} aria-hidden="true" /> : <Download size={18} aria-hidden="true" />}
        Download Full Report
      </button>
      {error ? <p className="mt-2 text-sm font-medium text-[var(--accent-red)]">{error}</p> : null}
    </div>
  );
}
