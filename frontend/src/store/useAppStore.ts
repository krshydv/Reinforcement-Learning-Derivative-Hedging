import { create } from "zustand"

type AuthState = {
  token: string | null
  setToken: (token: string) => void
  clearToken: () => void
}

const readStoredToken = (): string | null => {
  if (typeof window === "undefined") return null
  return localStorage.getItem("token")
}

export const useAuthStore = create<AuthState>(set => ({
  token: readStoredToken(),
  setToken: token => {
    if (typeof window !== "undefined") localStorage.setItem("token", token)
    set({ token })
  },
  clearToken: () => {
    if (typeof window !== "undefined") localStorage.removeItem("token")
    set({ token: null })
  }
}))
