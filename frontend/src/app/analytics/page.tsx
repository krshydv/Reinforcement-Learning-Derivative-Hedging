"use client"
import { useMemo, useState } from "react"
import { PanelGrid } from "../../components/layout/PanelGrid"
import { AreaChartPanel } from "../../components/charts/AreaChartPanel"
import { LineChartPanel } from "../../components/charts/LineChartPanel"
import { Heatmap } from "../../components/charts/Heatmap"
import { useMarketSimulation, useMetrics } from "../../lib/queries"
import { MetricTile } from "../../components/ui/MetricTile"
import { PageHeader } from "../../components/ui/PageHeader"
import { FilterBar, TimeRangeSelector } from "../../components/ui/FilterBar"
import { Badge } from "../../components/ui/Badge"
import { Button } from "../../components/ui/Button"

export default function AnalyticsPage() {
  const [range, setRange] = useState("1M")
  const [compare, setCompare] = useState(false)
  const market = useMarketSimulation({ model: "heston", steps: 180, dt: 0.01, spot: 100, rate: 0.02, vol: 0.2 })
  const metrics = useMetrics()

  const pnlSeries = useMemo(() => (market.data ?? []).map((m, index) => ({ index, value: m.price })), [market.data])
  const volSeries = useMemo(() => (market.data ?? []).map((m, index) => ({ index, value: m.volatility })), [market.data])
  const heatmap = useMemo(
    () => Array.from({ length: 12 }, (_, i) => Array.from({ length: 12 }, (_, j) => Math.abs(Math.sin((i + 2) * (j + 1) / 6)))),
    []
  )

  return (
    <div className="animate-fade-in space-y-6">
      <PageHeader
        title="Analytics Workspace"
        description="Multi-factor macro regime analysis, volatility drift, and cross-asset correlation intelligence."
        meta={<Badge tone="info">Saved view: Institutional Default</Badge>}
        actions={
          <Button variant={compare ? "primary" : "secondary"} size="sm" onClick={() => setCompare(v => !v)}>
            {compare ? "Comparison On" : "Compare Mode"}
          </Button>
        }
      />
      <FilterBar onExport={() => undefined}>
        <TimeRangeSelector value={range} onChange={setRange} />
      </FilterBar>

      <div className="grid grid-cols-2 gap-3 lg:grid-cols-4">
        <MetricTile label="Sharpe" value={metrics.data?.sharpe ?? 0} loading={metrics.isLoading} />
        <MetricTile label="Sortino" value={metrics.data?.sortino ?? 0} loading={metrics.isLoading} />
        <MetricTile label="Max Drawdown" value={metrics.data?.max_drawdown ?? 0} loading={metrics.isLoading} />
        <MetricTile label="VaR" value={metrics.data?.var ?? 0} loading={metrics.isLoading} />
      </div>

      <PanelGrid
        panels={[
          { id: "macro", title: "Macro Regime", subtitle: "Cross-asset drift", content: <LineChartPanel data={pnlSeries} dataKey="value" /> },
          { id: "vol", title: "Volatility Drift", subtitle: "Surface dynamics", content: <AreaChartPanel data={volSeries} dataKey="value" /> },
          {
            id: "heat",
            title: "Correlation Matrix",
            subtitle: "Factor co-movement",
            span: "full",
            content: <Heatmap matrix={heatmap} title="12x12 correlation grid" />
          }
        ]}
      />
    </div>
  )
}
