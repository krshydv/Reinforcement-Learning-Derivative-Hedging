"use client"
import { motion } from "framer-motion"
import Link from "next/link"
import { useAuthStore } from "../store/useAppStore"

export default function Page() {
  const { token, setToken } = useAuthStore()
  return (
    <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
      <div className="glass rounded-2xl p-10">
        <h1 className="text-4xl font-semibold text-white">Reinforcement Learning Derivative Hedging</h1>
        <p className="text-slate-300 mt-4 text-lg">Institutional-grade RL hedging, risk analytics, and multi-strategy benchmarking platform.</p>
        <div className="mt-8 flex gap-4">
          <Link href="/dashboard" className="px-6 py-3 rounded-xl bg-accent text-white">Launch Dashboard</Link>
          <Link href="/training" className="px-6 py-3 rounded-xl border border-slate-700 text-slate-200">View Training</Link>
        </div>
      </div>
      <motion.div initial={{ opacity: 0, y: 20 }} animate={{ opacity: 1, y: 0 }} className="glass rounded-2xl p-10">
        <h2 className="text-2xl font-semibold">Secure Access</h2>
        <p className="text-slate-300 mt-2">Authenticate to connect dashboards to live analytics and training streams.</p>
        <form
          className="mt-6 space-y-4"
          onSubmit={async e => {
            e.preventDefault()
            const form = e.currentTarget as HTMLFormElement
            const email = (form.elements.namedItem("email") as HTMLInputElement).value
            const password = (form.elements.namedItem("password") as HTMLInputElement).value
            const body = new URLSearchParams({ username: email, password })
            const response = await fetch(`${process.env.NEXT_PUBLIC_API_URL}/auth/token`, {
              method: "POST",
              headers: { "Content-Type": "application/x-www-form-urlencoded" },
              body
            })
            const data = await response.json()
            if (data.access_token) setToken(data.access_token)
          }}
        >
          <input name="email" placeholder="email" className="w-full bg-transparent border border-slate-700 rounded-lg px-4 py-3" />
          <input name="password" type="password" placeholder="password" className="w-full bg-transparent border border-slate-700 rounded-lg px-4 py-3" />
          <button className="w-full px-6 py-3 rounded-xl bg-accent text-white">Authenticate</button>
        </form>
        <div className="mt-4 text-sm text-slate-400">Token status: {token ? "active" : "offline"}</div>
      </motion.div>
    </div>
  )
}
