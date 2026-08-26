type Tone = "good" | "warning" | "critical" | "muted";

const TONE_CLASSES: Record<Tone, string> = {
  good: "bg-status-good/15 text-status-good",
  warning: "bg-status-warning/15 text-status-warning",
  critical: "bg-status-critical/15 text-status-critical",
  muted: "bg-white/[0.06] text-ink-muted",
};

const DOT_CLASSES: Record<Tone, string> = {
  good: "bg-status-good",
  warning: "bg-status-warning",
  critical: "bg-status-critical",
  muted: "bg-ink-muted",
};

export function StatusChip({ tone, label }: { tone: Tone; label: string }) {
  return (
    <span
      className={`inline-flex items-center gap-1.5 rounded-full px-2.5 py-1 text-xs font-medium ${TONE_CLASSES[tone]}`}
    >
      <span className={`h-1.5 w-1.5 rounded-full ${DOT_CLASSES[tone]}`} aria-hidden="true" />
      {label}
    </span>
  );
}
