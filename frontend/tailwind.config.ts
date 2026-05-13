import type { Config } from "tailwindcss"

export default {
  content: ["./src/**/*.{ts,tsx}"],
  theme: {
    extend: {
      colors: {
        background: "#0b0f1a",
        panel: "rgba(17, 25, 40, 0.7)",
        border: "rgba(148, 163, 184, 0.2)",
        accent: "#3b82f6",
        success: "#22c55e",
        danger: "#ef4444",
        warning: "#f59e0b"
      },
      boxShadow: {
        glass: "0 4px 30px rgba(0, 0, 0, 0.3)"
      },
      backdropBlur: {
        glass: "20px"
      }
    }
  },
  plugins: []
} satisfies Config
