import { Inbox } from "lucide-react"

export function EmptyState({ title, description, action }: { title: string; description?: string; action?: React.ReactNode }) {
  return (
    <div className="flex flex-col items-center justify-center rounded-control border border-dashed border-border px-6 py-12 text-center">
      <div className="mb-3 flex h-10 w-10 items-center justify-center rounded-full bg-surface-overlay text-ink-muted">
        <Inbox size={18} />
      </div>
      <div className="text-sm font-medium text-ink-primary">{title}</div>
      {description ? <p className="mt-1 max-w-sm text-xs text-ink-muted">{description}</p> : null}
      {action ? <div className="mt-4">{action}</div> : null}
    </div>
  )
}
