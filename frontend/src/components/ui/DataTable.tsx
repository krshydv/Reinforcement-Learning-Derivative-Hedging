import { cn } from "../../lib/utils"
import { EmptyState } from "./EmptyState"

export type Column<T> = {
  key: string
  header: string
  align?: "left" | "right"
  render: (row: T) => React.ReactNode
}

export function DataTable<T>({
  columns,
  rows,
  keyFn,
  loading,
  emptyTitle = "No data",
  emptyDescription,
  className
}: {
  columns: Column<T>[]
  rows: T[]
  keyFn: (row: T) => string
  loading?: boolean
  emptyTitle?: string
  emptyDescription?: string
  className?: string
}) {
  if (loading) {
    return (
      <div className={cn("space-y-2", className)}>
        {Array.from({ length: 5 }).map((_, i) => (
          <div key={i} className="skeleton h-9 w-full" />
        ))}
      </div>
    )
  }

  if (!rows.length) {
    return <EmptyState title={emptyTitle} description={emptyDescription} />
  }

  return (
    <div className={cn("overflow-auto rounded-control border border-border-subtle", className)}>
      <table className="data-table">
        <thead>
          <tr>
            {columns.map(col => (
              <th key={col.key} className={col.align === "right" ? "text-right" : undefined}>
                {col.header}
              </th>
            ))}
          </tr>
        </thead>
        <tbody>
          {rows.map(row => (
            <tr key={keyFn(row)}>
              {columns.map(col => (
                <td key={col.key} className={col.align === "right" ? "text-right" : undefined}>
                  {col.render(row)}
                </td>
              ))}
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  )
}
