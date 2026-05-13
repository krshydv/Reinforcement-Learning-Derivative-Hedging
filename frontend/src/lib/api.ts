import { useAuthStore } from "../store/useAppStore"

export async function fetchJson<T>(path: string, options: { method?: string; body?: unknown } = {}): Promise<T> {
  const token = useAuthStore.getState().token
  const response = await fetch(`${process.env.NEXT_PUBLIC_API_URL}${path}`, {
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
