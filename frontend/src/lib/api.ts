import { useAuthStore } from "../store/useAppStore"

const trimTrailingSlash = (value: string) => (value.endsWith("/") ? value.slice(0, -1) : value)

export const apiBase = () => {
  const env = process.env.NEXT_PUBLIC_API_URL
  if (env) return trimTrailingSlash(env)
  if (typeof window !== "undefined") return `${window.location.protocol}//${window.location.host}/api/v1`
  return "/api/v1"
}

export const wsBase = () => {
  const env = process.env.NEXT_PUBLIC_WS_URL
  if (env) return trimTrailingSlash(env)
  if (typeof window !== "undefined") {
    const protocol = window.location.protocol === "https:" ? "wss" : "ws"
    return `${protocol}://${window.location.host}`
  }
  return "ws://localhost:8080"
}

export async function fetchJson<T>(path: string, options: { method?: string; body?: unknown } = {}): Promise<T> {
  const token = useAuthStore.getState().token
  const response = await fetch(`${apiBase()}${path}`, {
    method: options.method ?? "GET",
    headers: {
      "Content-Type": "application/json",
      ...(token ? { Authorization: `Bearer ${token}` } : {})
    },
    body: options.body ? JSON.stringify(options.body) : undefined
  })
  if (!response.ok) {
    const text = await response.text()
    throw new Error(text)
  }
  return response.json()
}
