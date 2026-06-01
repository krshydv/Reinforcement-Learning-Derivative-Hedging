"use client"
import { cn } from "../../lib/utils"
import { Download, Maximize2 } from "lucide-react"
import { Button } from "./Button"

export function FilterBar({
  children,
  onExport,
  onFullscreen,
  className
}: {
  children?: React.ReactNode
  onExport?: () => void
  onFullscreen?: () => void
  className?: string
}) {
  return (
    <div className={cn("mb-4 flex flex-wrap items-center justify-between gap-3 rounded-control border border-border bg-surface/80 px-3 py-2 backdrop-blur", className)}>
      <div className="flex flex-wrap items-center gap-2">{children}</div>
      <div className="flex items-center gap-2">
        {onExport ? (
          <Button variant="ghost" size="sm" onClick={onExport}>
            <Download size={14} />
            Export
          </Button>
        ) : null}
        {onFullscreen ? (
          <Button variant="ghost" size="sm" onClick={onFullscreen}>
            <Maximize2 size={14} />
            Fullscreen
          </Button>
        ) : null}
      </div>
    </div>
  )
}

export function TimeRangeSelector({
  value,
  onChange,
  ranges = ["1D", "1W", "1M", "3M", "YTD", "ALL"]
}: {
  value: string
  onChange: (range: string) => void
  ranges?: string[]
}) {
  return (
    <div className="inline-flex rounded-control border border-border p-0.5">
      {ranges.map(range => (
        <button
          key={range}
          type="button"
          onClick={() => onChange(range)}
          className={cn(
            "rounded-[6px] px-2.5 py-1 text-2xs font-medium uppercase tracking-wide transition",
            value === range ? "bg-accent-muted text-accent" : "text-ink-muted hover:text-ink-secondary"
          )}
        >
          {range}
        </button>
      ))}
    </div>
  )
}
