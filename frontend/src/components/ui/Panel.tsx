import { cn } from "../../lib/utils"

export function Panel({
  title,
  subtitle,
  action,
  children,
  className,
  bodyClassName,
  noPadding
}: {
  title?: string
  subtitle?: string
  action?: React.ReactNode
  children: React.ReactNode
  className?: string
  bodyClassName?: string
  noPadding?: boolean
}) {
  return (
    <section className={cn("panel flex min-h-0 flex-col", className)}>
      {title ? (
        <header className="panel-header">
          <div>
            <h3 className="text-sm font-medium text-ink-primary">{title}</h3>
            {subtitle ? <p className="mt-0.5 text-xs text-ink-muted">{subtitle}</p> : null}
          </div>
          {action ? <div className="shrink-0">{action}</div> : null}
        </header>
      ) : null}
      <div className={cn(!noPadding && "panel-body flex-1 min-h-0", bodyClassName)}>{children}</div>
    </section>
  )
}
