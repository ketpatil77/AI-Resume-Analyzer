import { BrainCircuit, LogIn, Moon, Sun } from "lucide-react";
import type { ThemeName } from "../hooks/useTheme";

interface HeaderProps {
  theme: ThemeName;
  onToggleTheme: () => void;
  onAdminClick: () => void;
}

export function Header({ theme, onToggleTheme, onAdminClick }: HeaderProps) {
  const nextTheme = theme === "dark" ? "light" : "dark";

  return (
    <header className="mb-6 flex items-center justify-between gap-4">
      <div className="flex min-w-0 items-center gap-3">
        <div className="flex h-12 w-12 shrink-0 items-center justify-center rounded-card border border-[var(--border)] bg-[var(--bg-card)] text-[var(--accent-blue-light)]">
          <BrainCircuit aria-hidden="true" size={26} />
        </div>
        <div className="min-w-0">
          <h1 className="font-display text-[26px] font-bold leading-tight tracking-normal text-[var(--text-primary)] sm:text-[32px]">
            AI Resume Analyser
          </h1>
          <p className="caption mt-1 max-w-[260px] break-words sm:max-w-none">
            ATS scoring, role match, keywords, and coaching in one report.
          </p>
        </div>
      </div>
      <div className="flex items-center gap-2">
        <button
          type="button"
          className="rounded-full border border-[var(--border)] bg-[var(--bg-card)] px-4 py-2 text-sm font-semibold text-[var(--text-primary)] shadow-[var(--shadow-sm)] transition-transform duration-200 hover:-translate-y-0.5"
          onClick={onAdminClick}
          aria-label="Open admin login"
          title="Open admin login"
        >
          <span className="inline-flex items-center gap-2">
            <LogIn size={16} aria-hidden="true" />
            Admin Login
          </span>
        </button>
        <button
          type="button"
          className="icon-button fixed right-4 top-4 z-20 sm:static"
          onClick={onToggleTheme}
          aria-label={`Switch to ${nextTheme} mode`}
          title={`Switch to ${nextTheme} mode`}
        >
          {theme === "dark" ? <Sun size={20} /> : <Moon size={20} />}
        </button>
      </div>
    </header>
  );
}
