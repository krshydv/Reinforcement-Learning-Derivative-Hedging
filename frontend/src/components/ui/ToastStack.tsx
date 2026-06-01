"use client"
import { useToastStore } from "../../store/useToastStore"
import { cn } from "../../lib/utils"
import { X } from "lucide-react"

const toneStyles = {
  success: "border-positive/30 bg-surface-raised",
  error: "border-negative/30 bg-surface-raised",
  info: "border-info/30 bg-surface-raised",
  warning: "border-warning/30 bg-surface-raised"
}

export function ToastStack() {
  const { items, dismiss } = useToastStore()
  if (!items.length) return null

  return (
    <div className="pointer-events-none fixed bottom-4 right-4 z-[100] flex w-full max-w-sm flex-col gap-2">
      {items.map(item => (
        <div
          key={item.id}
          className={cn("pointer-events-auto animate-slide-up rounded-panel border px-4 py-3 shadow-elevated", toneStyles[item.tone])}
        >
          <div className="flex items-start justify-between gap-3">
            <div>
              <div className="text-sm font-medium text-ink-primary">{item.title}</div>
              {item.description ? <div className="mt-1 text-xs text-ink-muted">{item.description}</div> : null}
            </div>
            <button type="button" onClick={() => dismiss(item.id)} className="text-ink-faint hover:text-ink-secondary">
              <X size={14} />
            </button>
          </div>
        </div>
      ))}
    </div>
  )
}
