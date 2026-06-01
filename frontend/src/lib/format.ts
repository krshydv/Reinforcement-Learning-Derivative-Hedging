export function fmtNumber(value: number, digits = 2): string {
  if (!Number.isFinite(value)) return "—"
  return new Intl.NumberFormat("en-US", { maximumFractionDigits: digits, minimumFractionDigits: digits }).format(value)
}

export function fmtCompact(value: number): string {
  if (!Number.isFinite(value)) return "—"
  return new Intl.NumberFormat("en-US", { notation: "compact", maximumFractionDigits: 2 }).format(value)
}

export function fmtCurrency(value: number): string {
  if (!Number.isFinite(value)) return "—"
  return new Intl.NumberFormat("en-US", { style: "currency", currency: "USD", maximumFractionDigits: 0 }).format(value)
}

export function fmtPct(value: number, digits = 2): string {
  if (!Number.isFinite(value)) return "—"
  return `${(value * 100).toFixed(digits)}%`
}

export function fmtDelta(value: number): { text: string; positive: boolean } {
  const positive = value >= 0
  return { text: `${positive ? "+" : ""}${fmtNumber(value)}`, positive }
}
