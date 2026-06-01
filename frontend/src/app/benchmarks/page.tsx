"use client"
import { PanelGrid } from "../../components/layout/PanelGrid"
import { MetricTile } from "../../components/ui/MetricTile"
import { AreaChartPanel } from "../../components/charts/AreaChartPanel"
import { LineChartPanel } from "../../components/charts/LineChartPanel"
import { useBenchmarks } from "../../lib/queries"
import { PageHeader } from "../../components/ui/PageHeader"
import { Badge } from "../../components/ui/Badge"

export default function BenchmarksPage() {
  const benchmarks = useBenchmarks()
  const pricing = benchmarks.data?.pricing
  const backtests = benchmarks.data?.backtests
  const timingSeries = Object.entries(benchmarks.data?.timings ?? {}).map(([key, value], index) => ({ index, value }))
  const backtestSeries = Object.entries(backtests ?? {}).map(([key, value], index) => ({ index, value: value.pnl ?? 0 }))

  return (
    <div className="animate-fade-in space-y-6">
      <PageHeader
        title="Quant Benchmarks"
        description="Pricing engine accuracy, runtime profiling, strategy backtests, and risk snapshots."
        meta={<Badge tone="info">Engine v2 · Heston · Merton</Badge>}
      />
      <PanelGrid
        panels={[
          {
            id: "pricing",
            title: "Pricing Accuracy",
            subtitle: "Model fair values",
            content: (
              <div className="grid grid-cols-2 gap-3">
                <MetricTile label="Black-Scholes" value={pricing?.black_scholes ?? 0} />
                <MetricTile label="Monte Carlo" value={pricing?.monte_carlo ?? 0} />
                <MetricTile label="Heston MC" value={pricing?.heston_monte_carlo ?? 0} />
                <MetricTile label="Merton MC" value={pricing?.merton_jump_monte_carlo ?? 0} />
              </div>
            )
          },
          { id: "timings", title: "Benchmark Runtime", subtitle: "Latency (ms)", content: <AreaChartPanel data={timingSeries} dataKey="value" /> },
          { id: "backtests", title: "Strategy PnL", content: <LineChartPanel data={backtestSeries} dataKey="value" /> },
          {
            id: "risk",
            title: "Risk Snapshot",
            content: (
              <div className="grid grid-cols-2 gap-3">
                <MetricTile label="Sharpe" value={benchmarks.data?.risk?.sharpe ?? 0} />
                <MetricTile label="CVaR" value={benchmarks.data?.risk?.cvar ?? 0} />
              </div>
            )
          }
        ]}
      />
    </div>
  )
}
