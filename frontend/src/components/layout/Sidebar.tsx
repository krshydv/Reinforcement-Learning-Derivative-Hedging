"use client"
import Link from "next/link"
import { usePathname } from "next/navigation"
import { Route } from "next"
import { cn } from "../../lib/utils"
import { useUIStore } from "../../store/useUIStore"
import {
  Activity,
  AreaChart,
  BarChart3,
  FlaskConical,
  Gauge,
  Layers,
  Monitor,
  Radar,
  Server,
  ShieldCheck,
  TerminalSquare,
  Database,
  LineChart
} from "lucide-react"

const sections = [
  {
    label: "Trading",
    links: [
      { href: "/dashboard", label: "Command Center", icon: Activity },
      { href: "/portfolio", label: "Portfolio", icon: Layers },
      { href: "/risk", label: "Risk Desk", icon: ShieldCheck }
    ]
  },
  {
    label: "Research",
    links: [
      { href: "/analytics", label: "Analytics", icon: BarChart3 },
      { href: "/research", label: "Research Lab", icon: LineChart },
      { href: "/benchmarks", label: "Benchmarks", icon: AreaChart }
    ]
  },
  {
    label: "Machine Learning",
    links: [
      { href: "/training", label: "RL Training", icon: Gauge },
      { href: "/experiments", label: "Experiments", icon: FlaskConical },
      { href: "/observability", label: "Observability", icon: Radar },
      { href: "/telemetry", label: "Telemetry", icon: TerminalSquare }
    ]
  },
  {
    label: "Platform",
    links: [
      { href: "/strategies", label: "Strategies", icon: Database },
      { href: "/infra", label: "Infrastructure", icon: Server },
      { href: "/health", label: "System Health", icon: Monitor }
    ]
  }
] as const

function SidebarNav({ onNavigate }: { onNavigate?: () => void }) {
  const pathname = usePathname()

  return (
    <>
      {sections.map(section => (
        <div key={section.label}>
          <div className="mb-2 px-3 text-2xs font-semibold uppercase tracking-widest text-ink-faint">{section.label}</div>
          <div className="space-y-0.5">
            {section.links.map(link => {
              const Icon = link.icon
              const active = pathname === link.href
              return (
                <Link
                  key={link.href}
                  href={link.href as Route}
                  onClick={onNavigate}
                  className={cn(
                    "group flex items-center gap-3 rounded-control px-3 py-2.5 text-sm transition",
                    active
                      ? "bg-accent-muted text-accent shadow-glow"
                      : "text-ink-muted hover:bg-surface-overlay hover:text-ink-primary"
                  )}
                >
                  <Icon size={16} className={cn(active ? "text-accent" : "text-ink-faint group-hover:text-ink-secondary")} />
                  <span className="font-medium">{link.label}</span>
                </Link>
              )
            })}
          </div>
        </div>
      ))}
    </>
  )
}

export function Sidebar() {
  const mobileOpen = useUIStore(s => s.mobileNavOpen)
  const setMobileNavOpen = useUIStore(s => s.setMobileNavOpen)

  return (
    <>
      {mobileOpen ? (
        <button
          type="button"
          className="fixed inset-0 z-40 bg-black/60 backdrop-blur-sm lg:hidden"
          aria-label="Close navigation"
          onClick={() => setMobileNavOpen(false)}
        />
      ) : null}
      <aside
        className={cn(
          "fixed inset-y-0 left-0 z-50 flex w-72 flex-col border-r border-border bg-surface/95 backdrop-blur-xl transition-transform lg:static lg:z-auto lg:w-60 lg:translate-x-0 xl:w-64",
          mobileOpen ? "translate-x-0" : "-translate-x-full",
          "lg:translate-x-0"
        )}
      >
      <div className="border-b border-border-subtle px-5 py-5">
        <div className="flex items-center gap-3">
          <div className="flex h-9 w-9 items-center justify-center rounded-control bg-accent-muted shadow-glow">
            <Activity className="text-accent" size={18} />
          </div>
          <div>
            <div className="text-sm font-semibold tracking-tight text-ink-primary">Quantum Hedge</div>
            <div className="text-2xs uppercase tracking-wider text-ink-faint">Institutional OS</div>
          </div>
        </div>
      </div>
      <nav className="flex-1 space-y-6 overflow-y-auto px-3 py-4">
        <SidebarNav onNavigate={() => setMobileNavOpen(false)} />
      </nav>
      <div className="border-t border-border-subtle px-4 py-4 text-2xs text-ink-faint">
        <div className="rounded-control border border-border bg-surface-raised px-3 py-2">
          <div className="font-medium text-ink-muted">Enterprise</div>
          <div className="mt-0.5">SOC2-ready deployment</div>
        </div>
      </div>
    </aside>
    </>
  )
}
