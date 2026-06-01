import { cn } from "../../lib/utils"

const tones = {
  neutral: "bg-surface-overlay text-ink-secondary border-border",
  success: "bg-positive/10 text-positive border-positive/20",
  warning: "bg-warning/10 text-warning border-warning/20",
  danger: "bg-negative/10 text-negative border-negative/20",
  info: "bg-info/10 text-info border-info/20",
  accent: "bg-accent-muted text-accent border-accent/30"
} as const

export function Badge({
  children,
  tone = "neutral",
  className,
  dot
}: {
  children: React.ReactNode
  tone?: keyof typeof tones
  className?: string
  dot?: boolean
}) {
  return (
    <span className={cn("inline-flex items-center gap-1.5 rounded-full border px-2 py-0.5 text-2xs font-medium uppercase tracking-wide", tones[tone], className)}>
      {dot ? <span className={cn("h-1.5 w-1.5 rounded-full", tone === "success" ? "bg-positive" : tone === "danger" ? "bg-negative" : tone === "warning" ? "bg-warning" : "bg-accent")} /> : null}
      {children}
    </span>
  )
}
