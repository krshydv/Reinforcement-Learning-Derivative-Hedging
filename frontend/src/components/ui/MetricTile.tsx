import { cn } from "../../lib/utils"
import { fmtCompact, fmtNumber } from "../../lib/format"
import { TrendingDown, TrendingUp } from "lucide-react"

export function MetricTile({
  label,
  value,
  format = "number",
  delta,
  hint,
  className,
  loading
}: {
  label: string
  value: number
  format?: "number" | "compact" | "currency" | "pct"
  delta?: number
  hint?: string
  className?: string
  loading?: boolean
}) {
  const display =
    format === "compact" ? fmtCompact(value) : format === "currency" ? fmtNumber(value, 0) : format === "pct" ? `${fmtNumber(value * 100, 2)}%` : fmtNumber(value, 4)

  if (loading) {
    return (
      <div className={cn("panel p-4", className)}>
        <div className="skeleton h-3 w-20" />
        <div className="skeleton mt-3 h-8 w-28" />
      </div>
    )
  }

  return (
    <div className={cn("panel p-4", className)}>
      <div className="text-2xs font-medium uppercase tracking-wider text-ink-muted">{label}</div>
      <div className="mt-2 flex items-end justify-between gap-2">
        <div className="font-mono text-2xl font-semibold tracking-tight text-ink-primary">{display}</div>
        {delta !== undefined && Number.isFinite(delta) ? (
          <span className={cn("inline-flex items-center gap-0.5 text-xs font-medium", delta >= 0 ? "text-positive" : "text-negative")}>
            {delta >= 0 ? <TrendingUp size={12} /> : <TrendingDown size={12} />}
            {fmtNumber(Math.abs(delta), 2)}
          </span>
        ) : null}
      </div>
      {hint ? <div className="mt-1.5 text-2xs text-ink-faint">{hint}</div> : null}
    </div>
  )
}

export function StatCard({ label, value }: { label: string; value: number }) {
  return <MetricTile label={label} value={value} />
}
