"use client"
import { useMemo } from "react"
import { useTelemetryStream } from "../../hooks/useTelemetry"

const TELEMETRY_CHANNELS = ["training", "training.metrics", "risk", "portfolio", "api.latency"] as const

export function TelemetryBootstrap() {
  const channels = useMemo(() => [...TELEMETRY_CHANNELS], [])
  useTelemetryStream(channels, 20, false)
  return null
}
