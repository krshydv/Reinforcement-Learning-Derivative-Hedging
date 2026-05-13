import { useQuery } from "@tanstack/react-query"
import { fetchJson } from "./api"
import { MarketPoint, MetricSeries } from "../types"

export function useMarketSimulation(payload: { model: string; steps: number; dt: number; spot: number; rate: number; vol: number }) {
  return useQuery({
    queryKey: ["market", payload],
    queryFn: () => fetchJson<MarketPoint[]>("/market/simulate", { method: "POST", body: payload }),
    staleTime: 5000
  })
}

export function useMetrics() {
  return useQuery({
    queryKey: ["metrics"],
    queryFn: () => fetchJson<Record<string, number>>("/metrics/latest"),
    staleTime: 3000,
    refetchInterval: 3000
  })
}

export function useTrainingMetrics() {
  return useQuery({
    queryKey: ["training-metrics"],
    queryFn: async () => {
      const series = await fetchJson<MarketPoint[]>("/market/simulate", { method: "POST", body: { model: "gbm", steps: 120, dt: 0.01, spot: 100, rate: 0.02, vol: 0.25 } })
      const rewards: MetricSeries[] = series.map((p, index) => ({ index, value: Math.tanh(p.price / 120) }))
      const losses: MetricSeries[] = series.map((p, index) => ({ index, value: Math.abs(p.volatility - 0.2) }))
      const utilization: MetricSeries[] = series.map((p, index) => ({ index, value: 40 + (p.volatility * 100) % 60 }))
      const heatmap = Array.from({ length: 8 }, (_, i) => Array.from({ length: 8 }, (_, j) => Math.abs(Math.sin((i + 1) * (j + 1) / 10))))
      return { rewards, losses, utilization, heatmap }
    },
    refetchInterval: 4000
  })
}

export function useRiskAnalytics() {
  return useQuery({
    queryKey: ["risk-analytics"],
    queryFn: async () => {
      const series = await fetchJson<MarketPoint[]>("/market/simulate", { method: "POST", body: { model: "jump", steps: 160, dt: 0.01, spot: 100, rate: 0.03, vol: 0.35 } })
      const returns = series.map((p, i) => (i === 0 ? 0 : Math.log(p.price / series[i - 1].price)))
      const sorted = [...returns].sort((a, b) => a - b)
      const varValue = sorted[Math.floor(0.05 * sorted.length)] ?? 0
      const cvarValue = sorted.slice(0, Math.floor(0.05 * sorted.length)).reduce((a, b) => a + b, 0) / Math.max(1, Math.floor(0.05 * sorted.length))
      const varSeries = returns.map((r, index) => ({ index, value: r }))
      const tailMatrix = Array.from({ length: 8 }, (_, i) => Array.from({ length: 8 }, (_, j) => Math.abs(Math.sin(radians(i + j)))))
      const corrMatrix = Array.from({ length: 8 }, (_, i) => Array.from({ length: 8 }, (_, j) => Math.cos((i - j) / 4)))
      const liquiditySeries = returns.map((r, index) => ({ index, value: Math.abs(r) * 100 }))
      return { varValue, cvarValue, varSeries, tailMatrix, corrMatrix, liquiditySeries }
    },
    refetchInterval: 5000
  })
}

export function useResearchAnalytics() {
  return useQuery({
    queryKey: ["research"],
    queryFn: async () => {
      const series = await fetchJson<MarketPoint[]>("/market/simulate", { method: "POST", body: { model: "heston", steps: 140, dt: 0.01, spot: 120, rate: 0.015, vol: 0.2 } })
      const benchmarkSeries = series.map((p, index) => ({ index, value: p.price }))
      const volSurface = Array.from({ length: 8 }, (_, i) => Array.from({ length: 8 }, (_, j) => Math.abs(Math.sin((i + 1) * (j + 1) / 8))))
      const greeksSurface = Array.from({ length: 8 }, (_, i) => Array.from({ length: 8 }, (_, j) => Math.abs(Math.cos((i + 1) * (j + 1) / 8))))
      const paths = series.map((p, index) => ({ index, value: p.price }))
      return { benchmarkSeries, volSurface, greeksSurface, paths }
    },
    refetchInterval: 6000
  })
}

export function usePortfolio() {
  return useQuery({
    queryKey: ["portfolio"],
    queryFn: () => fetchJson<{ netExposure: number; grossExposure: number; hedgeRatio: number; positions: { symbol: string; quantity: number; avgPrice: number; delta: number; gamma: number }[] }>("/portfolios/overview"),
    refetchInterval: 4000
  })
}

function radians(x: number) {
  return (x * Math.PI) / 180
}
