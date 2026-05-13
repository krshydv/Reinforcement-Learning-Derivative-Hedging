"use client"
import { motion } from "framer-motion"
import { useAuthStore } from "../../store/useAppStore"

export function TopBar() {
  const { token } = useAuthStore()
  return (
    <motion.div initial={{ opacity: 0, y: -10 }} animate={{ opacity: 1, y: 0 }} className="flex items-center justify-between px-6 py-4 border-b border-slate-800 bg-black/60">
      <div className="text-sm text-slate-400">Live Market Hedging Desk</div>
      <div className="text-xs text-slate-300">Session {token ? "secured" : "offline"}</div>
    </motion.div>
  )
}
