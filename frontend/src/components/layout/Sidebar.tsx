"use client"
import Link from "next/link"
import { usePathname } from "next/navigation"
import { Activity, ChartArea, FlaskConical, Gauge, Layers, ShieldCheck } from "lucide-react"

const links = [
  { href: "/dashboard", label: "Trading", icon: Activity },
  { href: "/training", label: "RL Training", icon: Gauge },
  { href: "/risk", label: "Risk", icon: ShieldCheck },
  { href: "/research", label: "Research", icon: FlaskConical },
  { href: "/portfolio", label: "Portfolio", icon: Layers }
]

export function Sidebar() {
  const pathname = usePathname()
  return (
    <aside className="w-64 border-r border-slate-800 min-h-screen p-6 bg-black">
      <div className="text-xl font-semibold text-white">Quantum Hedge</div>
      <nav className="mt-10 space-y-2">
        {links.map(link => {
          const Icon = link.icon
          const active = pathname === link.href
          return (
            <Link
              key={link.href}
              href={link.href}
              className={`flex items-center gap-3 px-4 py-3 rounded-xl ${active ? "bg-slate-800 text-white" : "text-slate-400 hover:text-white"}`}
            >
              <Icon size={18} />
              <span>{link.label}</span>
            </Link>
          )
        })}
      </nav>
    </aside>
  )
}
