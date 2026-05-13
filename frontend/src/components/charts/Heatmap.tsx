"use client"
export function Heatmap({ matrix }: { matrix: number[][] }) {
  return (
    <div className="grid grid-cols-8 gap-1">
      {matrix.flatMap((row, i) =>
        row.map((value, j) => (
          <div
            key={`${i}-${j}`}
            className="h-5 rounded"
            style={{ background: `rgba(59,130,246,${Math.min(1, Math.abs(value))})` }}
          />
        ))
      )}
    </div>
  )
}
