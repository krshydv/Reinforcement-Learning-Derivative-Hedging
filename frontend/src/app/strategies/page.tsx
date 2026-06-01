"use client"
import { PanelGrid } from "../../components/layout/PanelGrid"
import { LineChartPanel } from "../../components/charts/LineChartPanel"
import { useStrategyBenchmarks } from "../../lib/queries"
import { PageHeader } from "../../components/ui/PageHeader"
import { fmtNumber } from "../../lib/format"

export default function StrategiesPage() {
  const benchmarks = useStrategyBenchmarks()
  const pnlSeries = Object.entries(benchmarks.data ?? {}).map(([key, value], index) => ({ index, value: value.pnl ?? 0, label: key }))

  return (
    <div className="animate-fade-in space-y-6">
      <PageHeader title="Strategy Library" description="Performance attribution and cross-strategy benchmarking for hedging programs." />
      <PanelGrid
        panels={[
          { id: "performance", title: "Strategy Performance", subtitle: "Cumulative PnL", content: <LineChartPanel data={pnlSeries} dataKey="value" /> },
          {
            id: "attribution",
            title: "Performance Attribution",
            content: (
              <div className="space-y-2">
                {pnlSeries.map(item => (
                  <div key={item.index} className="flex items-center justify-between rounded-control border border-border-subtle px-3 py-2 text-sm">
                    <span className="text-ink-secondary">Strategy {item.index + 1}</span>
                    <span className="font-mono text-ink-primary">{fmtNumber(item.value, 2)}</span>
                  </div>
                ))}
              </div>
            )
          }
        ]}
      />
    </div>
  )
}
