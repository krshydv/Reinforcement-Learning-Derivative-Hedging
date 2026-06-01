export function ChartTooltip({
  active,
  payload,
  label
}: {
  active?: boolean
  payload?: { value: number; name: string; color: string }[]
  label?: string
}) {
  if (!active || !payload?.length) return null
  return (
    <div className="rounded-control border border-border-strong bg-surface-overlay/95 px-3 py-2 shadow-elevated backdrop-blur">
      <div className="mb-1 font-mono text-2xs text-ink-muted">t = {label}</div>
      {payload.map(entry => (
        <div key={entry.name} className="flex items-center justify-between gap-4 text-xs">
          <span className="text-ink-muted">{entry.name}</span>
          <span className="font-mono font-medium" style={{ color: entry.color }}>
            {Number(entry.value).toFixed(4)}
          </span>
        </div>
      ))}
    </div>
  )
}
