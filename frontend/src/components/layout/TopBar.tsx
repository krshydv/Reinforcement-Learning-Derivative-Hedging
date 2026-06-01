"use client"
import { usePathname } from "next/navigation"
import { Search, Command, Menu } from "lucide-react"
import { useAuthStore } from "../../store/useAppStore"
import { useTelemetryStore } from "../../store/useTelemetryStore"
import { useUIStore } from "../../store/useUIStore"
import { Badge } from "../ui/Badge"
import { Button } from "../ui/Button"
import { cn } from "../../lib/utils"

const titles: Record<string, string> = {
  "/dashboard": "Trading Command Center",
  "/analytics": "Analytics Workspace",
  "/training": "RL Training Operations",
  "/observability": "RL Observability",
  "/risk": "Risk Management",
  "/benchmarks": "Quant Benchmarks",
  "/telemetry": "Telemetry Console",
  "/experiments": "Experiment Registry",
  "/strategies": "Strategy Library",
  "/research": "Research Lab",
  "/portfolio": "Portfolio Explorer",
  "/infra": "Infrastructure",
  "/health": "System Health"
}

export function TopBar() {
  const pathname = usePathname()
  const { token } = useAuthStore()
  const status = useTelemetryStore(state => state.status)
  const { setCommandOpen, setMobileNavOpen, searchQuery, setSearchQuery } = useUIStore()

  const title = titles[pathname] ?? "Platform"
  const telemetryTone = status === "connected" ? "success" : status === "connecting" ? "warning" : "danger"

  return (
    <header className="sticky top-0 z-40 border-b border-border bg-canvas/80 backdrop-blur-xl">
      <div className="flex flex-wrap items-center justify-between gap-3 px-4 py-3 md:px-6">
        <div className="flex min-w-0 items-center gap-2">
          <Button
            variant="ghost"
            size="sm"
            className="lg:hidden"
            aria-label="Open navigation"
            onClick={() => setMobileNavOpen(true)}
          >
            <Menu size={18} />
          </Button>
          <div className="min-w-0">
          <div className="text-2xs uppercase tracking-widest text-ink-faint">Live Market Hedging Desk</div>
          <h2 className="truncate text-base font-semibold text-ink-primary md:text-lg">{title}</h2>
          </div>
        </div>
        <div className="flex flex-1 flex-wrap items-center justify-end gap-2 md:gap-3">
          <Badge tone={telemetryTone} dot>
            Telemetry {status}
          </Badge>
          <Badge tone={token ? "success" : "neutral"}>{token ? "Session Secured" : "Unauthenticated"}</Badge>
          <div className="relative hidden sm:block">
            <Search className="pointer-events-none absolute left-2.5 top-2.5 text-ink-faint" size={14} />
            <input
              className="control-input w-44 pl-8 md:w-56"
              placeholder="Search workspace..."
              value={searchQuery}
              onChange={e => setSearchQuery(e.target.value)}
            />
          </div>
          <Button variant="secondary" size="sm" onClick={() => setCommandOpen(true)} aria-label="Open command palette">
            <Command size={14} />
            <span className="hidden md:inline">Command</span>
            <span className="kbd hidden lg:inline">⌘K</span>
          </Button>
        </div>
      </div>
    </header>
  )
}
