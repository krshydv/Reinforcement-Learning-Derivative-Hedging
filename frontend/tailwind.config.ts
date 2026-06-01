import type { Config } from "tailwindcss"

export default {
  content: ["./src/**/*.{ts,tsx}"],
  theme: {
    extend: {
      colors: {
        canvas: "var(--color-canvas)",
        surface: {
          DEFAULT: "var(--color-surface)",
          raised: "var(--color-surface-raised)",
          overlay: "var(--color-surface-overlay)"
        },
        border: {
          DEFAULT: "var(--color-border)",
          subtle: "var(--color-border-subtle)",
          strong: "var(--color-border-strong)"
        },
        ink: {
          primary: "var(--color-ink-primary)",
          secondary: "var(--color-ink-secondary)",
          muted: "var(--color-ink-muted)",
          faint: "var(--color-ink-faint)"
        },
        accent: {
          DEFAULT: "var(--color-accent)",
          muted: "var(--color-accent-muted)",
          glow: "var(--color-accent-glow)"
        },
        positive: "var(--color-positive)",
        negative: "var(--color-negative)",
        warning: "var(--color-warning)",
        info: "var(--color-info)"
      },
      fontFamily: {
        sans: ["var(--font-sans)", "system-ui", "sans-serif"],
        mono: ["var(--font-mono)", "ui-monospace", "monospace"]
      },
      fontSize: {
        "2xs": ["0.625rem", { lineHeight: "0.875rem" }],
        display: ["2rem", { lineHeight: "2.25rem", letterSpacing: "-0.02em" }],
        "display-sm": ["1.5rem", { lineHeight: "1.75rem", letterSpacing: "-0.02em" }]
      },
      spacing: {
        18: "4.5rem",
        22: "5.5rem"
      },
      borderRadius: {
        panel: "var(--radius-panel)",
        control: "var(--radius-control)"
      },
      boxShadow: {
        panel: "var(--shadow-panel)",
        elevated: "var(--shadow-elevated)",
        glow: "var(--shadow-glow)"
      },
      backgroundImage: {
        "grid-fade": "radial-gradient(circle at 50% 0%, rgba(56, 189, 248, 0.08), transparent 55%)",
        "panel-gradient": "linear-gradient(180deg, var(--color-surface-raised) 0%, var(--color-surface) 100%)"
      },
      animation: {
        "fade-in": "fadeIn 0.35s ease-out",
        "slide-up": "slideUp 0.4s ease-out"
      },
      keyframes: {
        fadeIn: { from: { opacity: "0" }, to: { opacity: "1" } },
        slideUp: { from: { opacity: "0", transform: "translateY(8px)" }, to: { opacity: "1", transform: "translateY(0)" } }
      }
    }
  },
  plugins: []
} satisfies Config
