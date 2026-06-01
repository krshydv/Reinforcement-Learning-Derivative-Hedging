"use client"
import { motion, AnimatePresence } from "framer-motion"
import { useEffect, useMemo } from "react"
import { useUIStore } from "../../store/useUIStore"
import Link from "next/link"
import { Search } from "lucide-react"

const commands = [
  { label: "Trading Command Center", href: "/dashboard", hint: "G D" },
  { label: "Analytics Workspace", href: "/analytics", hint: "G A" },
  { label: "RL Training Operations", href: "/training", hint: "G T" },
  { label: "RL Observability", href: "/observability" },
  { label: "Risk Desk", href: "/risk" },
  { label: "Portfolio Explorer", href: "/portfolio" },
  { label: "Benchmarks", href: "/benchmarks" },
  { label: "Telemetry Console", href: "/telemetry" },
  { label: "Experiments", href: "/experiments" },
  { label: "Strategies", href: "/strategies" },
  { label: "Infrastructure", href: "/infra" },
  { label: "System Health", href: "/health" }
]

export function CommandPalette() {
  const { commandOpen, setCommandOpen, searchQuery, setSearchQuery } = useUIStore()

  useEffect(() => {
    const handler = (event: KeyboardEvent) => {
      if ((event.metaKey || event.ctrlKey) && event.key.toLowerCase() === "k") {
        event.preventDefault()
        setCommandOpen(!commandOpen)
      }
      if (event.key === "Escape") setCommandOpen(false)
    }
    window.addEventListener("keydown", handler)
    return () => window.removeEventListener("keydown", handler)
  }, [commandOpen, setCommandOpen])

  const filtered = useMemo(() => {
    const query = searchQuery.toLowerCase().trim()
    if (!query) return commands
    return commands.filter(cmd => cmd.label.toLowerCase().includes(query) || cmd.href.includes(query))
  }, [searchQuery])

  return (
    <AnimatePresence>
      {commandOpen && (
        <motion.div
          className="fixed inset-0 z-50 flex items-start justify-center bg-black/70 p-4 pt-[12vh] backdrop-blur-sm"
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
          exit={{ opacity: 0 }}
          onClick={() => setCommandOpen(false)}
        >
          <motion.div
            className="w-full max-w-xl overflow-hidden rounded-panel border border-border-strong bg-surface-raised shadow-elevated"
            initial={{ y: -12, opacity: 0, scale: 0.98 }}
            animate={{ y: 0, opacity: 1, scale: 1 }}
            exit={{ y: -8, opacity: 0, scale: 0.98 }}
            onClick={e => e.stopPropagation()}
          >
            <div className="flex items-center gap-2 border-b border-border px-4 py-3">
              <Search size={16} className="text-ink-faint" />
              <input
                autoFocus
                className="w-full bg-transparent text-sm text-ink-primary outline-none placeholder:text-ink-faint"
                placeholder="Search commands, pages, actions..."
                value={searchQuery}
                onChange={event => setSearchQuery(event.target.value)}
              />
              <span className="kbd">esc</span>
            </div>
            <div className="max-h-80 overflow-y-auto p-2">
              {filtered.map(cmd => (
                <Link
                  key={cmd.href}
                  href={cmd.href}
                  className="flex items-center justify-between rounded-control px-3 py-2.5 text-sm text-ink-secondary transition hover:bg-surface-overlay hover:text-ink-primary"
                  onClick={() => setCommandOpen(false)}
                >
                  <span>{cmd.label}</span>
                  {cmd.hint ? <span className="text-2xs text-ink-faint">{cmd.hint}</span> : <span className="text-2xs text-ink-faint">Open</span>}
                </Link>
              ))}
            </div>
          </motion.div>
        </motion.div>
      )}
    </AnimatePresence>
  )
}
