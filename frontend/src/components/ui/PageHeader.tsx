"use client"
import { cn } from "../../lib/utils"

export function PageHeader({
  title,
  description,
  meta,
  actions,
  className
}: {
  title: string
  description?: string
  meta?: React.ReactNode
  actions?: React.ReactNode
  className?: string
}) {
  return (
    <div className={cn("mb-6 flex flex-col gap-4 border-b border-border-subtle pb-5 lg:flex-row lg:items-end lg:justify-between", className)}>
      <div className="space-y-2">
        {meta ? <div className="flex flex-wrap items-center gap-2">{meta}</div> : null}
        <h1 className="text-display-sm font-semibold tracking-tight text-ink-primary">{title}</h1>
        {description ? <p className="max-w-3xl text-sm leading-relaxed text-ink-muted">{description}</p> : null}
      </div>
      {actions ? <div className="flex flex-wrap items-center gap-2">{actions}</div> : null}
    </div>
  )
}
