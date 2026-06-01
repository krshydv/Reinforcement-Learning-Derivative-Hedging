export function Chip({ label, value }: { label: string; value: string }) {
  return (
    <div className="px-3 py-1 rounded-full bg-slate-800 text-slate-300 text-xs">
      {label}: {value}
    </div>
  )
}
