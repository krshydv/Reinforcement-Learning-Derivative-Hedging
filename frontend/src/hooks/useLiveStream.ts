import { useEffect, useState } from "react"
import { useAuthStore } from "../store/useAppStore"
import { wsBase } from "../lib/api"

export function useLiveStream() {
  const { token } = useAuthStore()
  const [messages, setMessages] = useState<{ type: string; value: number }[]>([])
  const [heatmap, setHeatmap] = useState<number[][]>([])

  useEffect(() => {
    const clientId = Math.random().toString(36).slice(2)
    let socket: WebSocket | null = null
    let reconnectTimer: ReturnType<typeof setTimeout> | null = null
    let attempts = 0
    let closed = false

    const connect = () => {
      if (closed) return
      socket = new WebSocket(`${wsBase()}/ws/${clientId}?token=${token ?? ""}`)
      socket.onopen = () => {
        attempts = 0
      }
      socket.onmessage = event => {
        const payload = JSON.parse(event.data)
        if (payload?.type === "ping") {
          socket?.send(JSON.stringify({ type: "pong" }))
          return
        }
        setMessages(prev => [payload, ...prev].slice(0, 12))
        if (payload.matrix) setHeatmap(payload.matrix)
      }
      socket.onclose = () => {
        if (closed) return
        const delay = Math.min(16000, 1000 * Math.pow(2, attempts))
        attempts += 1
        reconnectTimer = setTimeout(connect, delay)
      }
      socket.onerror = () => {
        socket?.close()
      }
    }

    connect()

    return () => {
      closed = true
      if (reconnectTimer) clearTimeout(reconnectTimer)
      socket?.close()
    }
  }, [token])

  return { messages, heatmap }
}
