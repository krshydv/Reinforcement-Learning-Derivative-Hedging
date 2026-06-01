"use client"
import { useMemo, useState } from "react"
import { fmtNumber } from "../../lib/format"

export function Heatmap({
  matrix,
  rowLabels,
  colLabels,
  title
}: {
  matrix: number[][]
  rowLabels?: string[]
  colLabels?: string[]
  title?: string
}) {
  const [hover, setHover] = useState<{ i: number; j: number; value: number } | null>(null)
  const flat = useMemo(() => matrix.flat(), [matrix])
  const max = useMemo(() => Math.max(...flat.map(v => Math.abs(v)), 1e-6), [flat])

  if (!matrix.length) {
    return <div className="flex h-48 items-center justify-center text-xs text-ink-muted">No matrix data</div>
  }

  return (
    <div className="space-y-3">
      {title ? <div className="text-xs text-ink-muted">{title}</div> : null}
      <div className="overflow-auto">
        <div
          className="inline-grid gap-px rounded-control border border-border-subtle bg-border-subtle p-px"
          style={{ gridTemplateColumns: `repeat(${matrix[0]?.length ?? 0}, minmax(28px, 1fr))` }}
        >
          {matrix.flatMap((row, i) =>
            row.map((value, j) => {
              const intensity = Math.abs(value) / max
              const hue = value >= 0 ? "56, 189, 248" : "248, 113, 113"
              return (
                <div
                  key={`${i}-${j}`}
                  className="relative h-7 min-w-[28px] cursor-crosshair transition"
                  style={{ background: `rgba(${hue}, ${0.12 + intensity * 0.75})` }}
                  onMouseEnter={() => setHover({ i, j, value })}
                  onMouseLeave={() => setHover(null)}
                  title={`${rowLabels?.[i] ?? i}, ${colLabels?.[j] ?? j}: ${fmtNumber(value, 4)}`}
                />
              )
            })
          )}
        </div>
      </div>
      {hover ? (
        <div className="flex items-center justify-between rounded-control border border-border bg-surface-overlay px-3 py-2 text-2xs">
          <span className="text-ink-muted">
            Cell [{hover.i}, {hover.j}]
          </span>
          <span className="font-mono text-ink-primary">{fmtNumber(hover.value, 4)}</span>
        </div>
      ) : null}
    </div>
  )
}
