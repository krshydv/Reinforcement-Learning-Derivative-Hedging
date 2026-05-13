import type { Metadata } from "next"
import { Inter } from "next/font/google"
import "./globals.css"
import { QueryProvider } from "../providers/QueryProvider"
import { Sidebar } from "../components/layout/Sidebar"
import { TopBar } from "../components/layout/TopBar"

const inter = Inter({ subsets: ["latin"] })

export const metadata: Metadata = {
  title: "RL Derivative Hedging",
  description: "Institutional RL hedging platform"
}

export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <html lang="en">
      <body className={inter.className}>
        <QueryProvider>
          <div className="flex min-h-screen">
            <Sidebar />
            <div className="flex-1">
              <TopBar />
              <main className="p-6 space-y-6">{children}</main>
            </div>
          </div>
        </QueryProvider>
      </body>
    </html>
  )
}
