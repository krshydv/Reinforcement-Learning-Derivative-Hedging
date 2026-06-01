import { create } from "zustand"
import { TelemetryEvent } from "../types/telemetry"

type TelemetryState = {
  events: Record<string, TelemetryEvent[]>
  status: "connected" | "disconnected" | "connecting"
  pushEvent: (event: TelemetryEvent) => void
  setStatus: (status: TelemetryState["status"]) => void
}

export const useTelemetryStore = create<TelemetryState>(set => ({
  events: {},
  status: "disconnected",
  pushEvent: event =>
    set(state => {
      const existing = state.events[event.channel] ?? []
      const next = [event, ...existing].slice(0, 200)
      return { events: { ...state.events, [event.channel]: next } }
    }),
  setStatus: status => set({ status })
}))
