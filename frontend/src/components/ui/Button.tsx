import { cn } from "../../lib/utils"

const variants = {
  primary: "bg-accent text-canvas hover:bg-sky-300 shadow-glow border border-accent/40",
  secondary: "bg-surface-raised text-ink-primary border border-border hover:border-border-strong hover:bg-surface-overlay",
  ghost: "text-ink-secondary hover:text-ink-primary hover:bg-surface-overlay border border-transparent",
  danger: "bg-negative/15 text-negative border border-negative/30 hover:bg-negative/25"
} as const

export function Button({
  children,
  className,
  variant = "secondary",
  size = "md",
  ...props
}: React.ButtonHTMLAttributes<HTMLButtonElement> & {
  variant?: keyof typeof variants
  size?: "sm" | "md"
}) {
  return (
    <button
      className={cn(
        "inline-flex items-center justify-center gap-2 rounded-control font-medium transition focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-accent/40 disabled:pointer-events-none disabled:opacity-50",
        size === "sm" ? "px-2.5 py-1.5 text-xs" : "px-3.5 py-2 text-sm",
        variants[variant],
        className
      )}
      {...props}
    >
      {children}
    </button>
  )
}
