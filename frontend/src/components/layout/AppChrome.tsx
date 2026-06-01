"use client"
import { usePathname } from "next/navigation"
import { Sidebar } from "./Sidebar"
import { TopBar } from "./TopBar"

export function AppChrome({ children }: { children: React.ReactNode }) {
  const pathname = usePathname()
  const isLanding = pathname === "/"

  if (isLanding) {
    return <div className="min-h-screen">{children}</div>
  }

  return (
    <div className="flex min-h-screen">
      <Sidebar />
      <div className="flex min-w-0 flex-1 flex-col">
        <TopBar />
        <main className="flex-1 overflow-auto p-4 md:p-6 lg:p-8">{children}</main>
      </div>
    </div>
  )
}
