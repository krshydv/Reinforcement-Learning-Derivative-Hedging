export function StatCard({ label, value }: { label: string; value: number }) {
  return (
    <div className="glass rounded-xl p-4">
      <div className="text-xs text-slate-400 uppercase">{label}</div>
      <div className="text-2xl font-semibold text-white mt-2">{Number.isFinite(value) ? value.toFixed(4) : value}</div>
    </div>
  )
}
