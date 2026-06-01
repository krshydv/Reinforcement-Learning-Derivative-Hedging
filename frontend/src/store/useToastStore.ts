import { create } from "zustand"

export type ToastTone = "success" | "error" | "info" | "warning"

export type ToastItem = {
  id: string
  title: string
  description?: string
  tone: ToastTone
}

type ToastState = {
  items: ToastItem[]
  push: (toast: Omit<ToastItem, "id">) => void
  dismiss: (id: string) => void
}

export const useToastStore = create<ToastState>(set => ({
  items: [],
  push: toast =>
    set(state => {
      const id = crypto.randomUUID()
      setTimeout(() => {
        useToastStore.getState().dismiss(id)
      }, 4200)
      return { items: [{ ...toast, id }, ...state.items].slice(0, 5) }
    }),
  dismiss: id => set(state => ({ items: state.items.filter(item => item.id !== id) }))
}))
