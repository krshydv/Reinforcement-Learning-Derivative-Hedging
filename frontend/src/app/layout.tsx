import type { Metadata } from "next"
import { Inter, JetBrains_Mono } from "next/font/google"
import "./globals.css"
import { QueryProvider } from "../providers/QueryProvider"
import { AppChrome } from "../components/layout/AppChrome"
import { CommandPalette } from "../components/ui/CommandPalette"
import { TelemetryBootstrap } from "../components/telemetry/TelemetryBootstrap"
import { ToastStack } from "../components/ui/ToastStack"

const inter = Inter({ subsets: ["latin"], variable: "--font-sans" })
const jetbrains = JetBrains_Mono({ subsets: ["latin"], variable: "--font-mono" })

export const metadata: Metadata = {
  title: "Quantum Hedge | RL Derivative Hedging",
  description: "Institutional reinforcement learning derivative hedging platform"
}

export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <html lang="en" className={`${inter.variable} ${jetbrains.variable}`}>
      <body>
        <QueryProvider>
          <AppChrome>{children}</AppChrome>
          <CommandPalette />
          <TelemetryBootstrap />
          <ToastStack />
        </QueryProvider>
      </body>
    </html>
  )
}
