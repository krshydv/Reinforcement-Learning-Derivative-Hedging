"use client"
import { useState } from "react"
import { motion } from "framer-motion"
import Link from "next/link"
import { ArrowRight, Shield, Zap, LineChart } from "lucide-react"
import { apiBase } from "../lib/api"
import { useAuthStore } from "../store/useAppStore"
import { useToastStore } from "../store/useToastStore"
import { Button } from "../components/ui/Button"
import { Badge } from "../components/ui/Badge"

export default function Page() {
  const { token, setToken } = useAuthStore()
  const pushToast = useToastStore(s => s.push)
  const [error, setError] = useState<string | null>(null)
  const [submitting, setSubmitting] = useState(false)

  return (
    <div className="relative min-h-screen overflow-hidden">
      <div className="pointer-events-none absolute inset-0 bg-grid-fade" />
      <div className="relative mx-auto flex min-h-screen max-w-6xl flex-col px-6 py-10 lg:px-10">
        <header className="flex items-center justify-between">
          <div className="flex items-center gap-3">
            <div className="flex h-10 w-10 items-center justify-center rounded-control bg-accent-muted shadow-glow">
              <LineChart className="text-accent" size={20} />
            </div>
            <div>
              <div className="text-sm font-semibold text-ink-primary">Quantum Hedge</div>
              <div className="text-2xs uppercase tracking-widest text-ink-faint">Institutional Platform</div>
            </div>
          </div>
          <Badge tone={token ? "success" : "neutral"} dot>
            {token ? "Authenticated" : "Guest"}
          </Badge>
        </header>

        <div className="mt-16 grid flex-1 items-center gap-12 lg:grid-cols-2">
          <motion.div initial={{ opacity: 0, y: 16 }} animate={{ opacity: 1, y: 0 }} transition={{ duration: 0.5 }}>
            <Badge tone="accent" className="mb-4">
              Venture-grade quant infrastructure
            </Badge>
            <h1 className="text-display font-semibold tracking-tight text-ink-primary lg:text-5xl lg:leading-tight">
              Reinforcement learning derivative hedging at institutional scale
            </h1>
            <p className="mt-5 max-w-xl text-base leading-relaxed text-ink-muted">
              A unified operating system for portfolio managers, risk teams, and quant researchers — live telemetry,
              RL training operations, and enterprise risk analytics in one cockpit.
            </p>
            <div className="mt-8 flex flex-wrap gap-3">
              <Link href="/dashboard">
                <Button variant="primary">
                  Enter Command Center
                  <ArrowRight size={16} />
                </Button>
              </Link>
              <Link href="/training">
                <Button variant="secondary">View RL Operations</Button>
              </Link>
            </div>
            <div className="mt-10 grid grid-cols-3 gap-4">
              {[
                { icon: Shield, label: "Enterprise security", desc: "JWT, RBAC, audit-ready" },
                { icon: Zap, label: "Real-time streams", desc: "WebSocket telemetry" },
                { icon: LineChart, label: "Quant engine", desc: "Pricing, Greeks, RL" }
              ].map(item => (
                <div key={item.label} className="panel p-4">
                  <item.icon size={16} className="text-accent" />
                  <div className="mt-2 text-xs font-medium text-ink-primary">{item.label}</div>
                  <div className="mt-1 text-2xs text-ink-faint">{item.desc}</div>
                </div>
              ))}
            </div>
          </motion.div>

          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.55, delay: 0.08 }}
            className="panel p-8 shadow-elevated"
          >
            <h2 className="text-xl font-semibold text-ink-primary">Secure access</h2>
            <p className="mt-2 text-sm text-ink-muted">Authenticate to unlock live portfolio, risk, and training streams.</p>
            <form
              className="mt-6 space-y-4"
              onSubmit={async e => {
                e.preventDefault()
                setError(null)
                setSubmitting(true)
                try {
                  const form = e.currentTarget as HTMLFormElement
                  const email = (form.elements.namedItem("email") as HTMLInputElement).value
                  const password = (form.elements.namedItem("password") as HTMLInputElement).value
                  const body = new URLSearchParams({ username: email, password })
                  const response = await fetch(`${apiBase()}/auth/token`, {
                    method: "POST",
                    headers: { "Content-Type": "application/x-www-form-urlencoded" },
                    body
                  })
                  if (!response.ok) {
                    const detail = await response.text()
                    throw new Error(detail || `Authentication failed (${response.status})`)
                  }
                  const data = await response.json()
                  if (!data.access_token) throw new Error("No access token returned")
                  setToken(data.access_token)
                  pushToast({ title: "Session established", description: "Welcome back to Quantum Hedge", tone: "success" })
                } catch (err) {
                  const message = err instanceof Error ? err.message : "Authentication failed"
                  setError(message)
                  pushToast({ title: "Authentication failed", description: message, tone: "error" })
                } finally {
                  setSubmitting(false)
                }
              }}
            >
              <div>
                <label className="mb-1.5 block text-2xs uppercase tracking-wide text-ink-faint">Email</label>
                <input name="email" type="email" defaultValue="admin@rl-hedging.local" className="control-input" />
              </div>
              <div>
                <label className="mb-1.5 block text-2xs uppercase tracking-wide text-ink-faint">Password</label>
                <input name="password" type="password" defaultValue="admin12345" className="control-input" />
              </div>
              <Button type="submit" variant="primary" className="w-full" disabled={submitting}>
                {submitting ? "Authenticating..." : "Authenticate"}
              </Button>
            </form>
            {error ? <p className="mt-3 text-sm text-negative">{error}</p> : null}
            <div className="mt-4 text-xs text-ink-faint">Token status: {token ? "active" : "offline"}</div>
          </motion.div>
        </div>
      </div>
    </div>
  )
}
