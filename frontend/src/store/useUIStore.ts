import { create } from "zustand"

type UIState = {
  commandOpen: boolean
  mobileNavOpen: boolean
  searchQuery: string
  setCommandOpen: (open: boolean) => void
  setMobileNavOpen: (open: boolean) => void
  setSearchQuery: (value: string) => void
}

export const useUIStore = create<UIState>(set => ({
  commandOpen: false,
  mobileNavOpen: false,
  searchQuery: "",
  setCommandOpen: open => set({ commandOpen: open }),
  setMobileNavOpen: open => set({ mobileNavOpen: open }),
  setSearchQuery: value => set({ searchQuery: value })
}))
