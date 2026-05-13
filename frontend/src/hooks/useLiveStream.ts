import { useEffect, useState } from "react"
import { useAuthStore } from "../store/useAppStore"
import { wsBase } from "../lib/api"

export function useLiveStream() {
  const { token } = useAuthStore()
  const [messages, setMessages] = useState<{ type: string; value: number }[]>([])
  const [heatmap, setHeatmap] = useState<number[][]>([])

  useEffect(() => {
    const clientId = Math.random().toString(36).slice(2)
    const ws = new WebSocket(`${wsBase()}/ws/${clientId}?token=${token ?? ""}`)
    ws.onmessage = event => {
      const payload = JSON.parse(event.data)
      setMessages(prev => [payload, ...prev].slice(0, 12))
      if (payload.matrix) setHeatmap(payload.matrix)
    }
    return () => ws.close()
  }, [token])

  return { messages, heatmap }
}
