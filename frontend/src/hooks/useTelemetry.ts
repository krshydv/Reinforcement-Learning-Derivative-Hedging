import { useEffect, useMemo, useRef } from "react"
import { wsBase } from "../lib/api"
import { useAuthStore } from "../store/useAppStore"
import { useTelemetryStore } from "../store/useTelemetryStore"
import { TelemetryEvent } from "../types/telemetry"

const decodeEvent = async (payload: Record<string, unknown>): Promise<TelemetryEvent> => {
  if (payload.compressed) {
    if (typeof DecompressionStream === "undefined") {
      return payload as unknown as TelemetryEvent
    }
    const data = atob(String(payload.data))
    const bytes = new Uint8Array(data.length)
    for (let i = 0; i < data.length; i += 1) bytes[i] = data.charCodeAt(i)
    const stream = new Response(bytes).body!.pipeThrough(new DecompressionStream("deflate"))
    const decompressed = await new Response(stream).text()
    return JSON.parse(decompressed)
  }
  return payload as unknown as TelemetryEvent
}

export function useTelemetryStream(channels: string[], replay = 50, compress = false) {
  const { token } = useAuthStore()
  const pushEvent = useTelemetryStore(state => state.pushEvent)
  const setStatus = useTelemetryStore(state => state.setStatus)
  const buffer = useRef<TelemetryEvent[]>([])
  const scheduled = useRef<number | null>(null)

  const channelParam = useMemo(() => channels.join(","), [channels])

  useEffect(() => {
    if (!channels.length) return
    let socket: WebSocket | null = null
    let reconnectTimer: ReturnType<typeof setTimeout> | null = null
    let attempts = 0
    let closed = false

    const flush = () => {
      scheduled.current = null
      if (buffer.current.length) {
        buffer.current.forEach(event => pushEvent(event))
        buffer.current = []
      }
    }

    const scheduleFlush = () => {
      if (scheduled.current === null) {
        scheduled.current = window.setTimeout(flush, 200)
      }
    }

    const connect = () => {
      if (closed) return
      setStatus("connecting")
      socket = new WebSocket(`${wsBase()}/ws/telemetry?token=${token ?? ""}&channels=${channelParam}&replay=${replay}&compress=${compress ? 1 : 0}`)
      socket.onopen = () => {
        attempts = 0
        setStatus("connected")
      }
      socket.onmessage = event => {
        const payload = JSON.parse(event.data)
        if (payload.type === "ping") {
          socket?.send(JSON.stringify({ type: "pong" }))
          return
        }
        decodeEvent(payload).then(parsed => {
          buffer.current.push(parsed)
          scheduleFlush()
        })
      }
      socket.onclose = () => {
        if (closed) return
        setStatus("disconnected")
        const delay = Math.min(16000, 1000 * Math.pow(2, attempts))
        attempts += 1
        reconnectTimer = setTimeout(connect, delay)
      }
      socket.onerror = () => socket?.close()
    }

    connect()

    return () => {
      closed = true
      if (reconnectTimer) clearTimeout(reconnectTimer)
      if (scheduled.current) clearTimeout(scheduled.current)
      socket?.close()
    }
  }, [token, channelParam, replay, compress, pushEvent, setStatus])
}

export function useTelemetryChannel<TPayload = Record<string, unknown>>(channel: string) {
  const events = useTelemetryStore(state => (state.events[channel] ?? []) as TelemetryEvent<TPayload>[])
  const status = useTelemetryStore(state => state.status)
  return { events, status }
}
