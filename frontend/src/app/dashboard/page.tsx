"use client"
import { useMemo, useState } from "react"
import { PanelGrid } from "../../components/layout/PanelGrid"
import { MetricTile } from "../../components/ui/MetricTile"
import { LineChartPanel } from "../../components/charts/LineChartPanel"
import { AreaChartPanel } from "../../components/charts/AreaChartPanel"
import { Heatmap } from "../../components/charts/Heatmap"
import { useMarketSimulation, useMetrics, usePortfolio } from "../../lib/queries"
import { useLiveStream } from "../../hooks/useLiveStream"
import { useTelemetryStore } from "../../store/useTelemetryStore"
import { PageHeader } from "../../components/ui/PageHeader"
import { Badge } from "../../components/ui/Badge"
import { FilterBar, TimeRangeSelector } from "../../components/ui/FilterBar"
import { DataTable } from "../../components/ui/DataTable"
import { fmtNumber } from "../../lib/format"

export default function DashboardPage() {
  const [range, setRange] = useState("1M")
  const market = useMarketSimulation({ model: "heston", steps: 200, dt: 0.01, spot: 100, rate: 0.02, vol: 0.2 })
  const metrics = useMetrics()
  const portfolio = usePortfolio()
  const stream = useLiveStream()
  const telemetryStatus = useTelemetryStore(s => s.status)

  const pnlSeries = useMemo(() => (market.data ?? []).map((m, index) => ({ index, value: m.price })), [market.data])
  const volSeries = useMemo(() => (market.data ?? []).map((m, index) => ({ index, value: m.volatility })), [market.data])
  const dailyPnl = pnlSeries.length > 1 ? pnlSeries[pnlSeries.length - 1].value - pnlSeries[0].value : 0
  const healthScore = Math.min(100, Math.max(0, 72 + (metrics.data?.sharpe ?? 0) * 8 - (metrics.data?.max_drawdown ?? 0) * 100))

  return (
    <div className="animate-fade-in space-y-6">
      <PageHeader
        title="Trading Command Center"
        description="Executive view of portfolio health, live market regime, greeks exposure, and streaming desk telemetry."
        meta={
          <>
            <Badge tone="accent">Live</Badge>
            <Badge tone={telemetryStatus === "connected" ? "success" : "warning"} dot>
              Telemetry {telemetryStatus}
            </Badge>
            <Badge tone="info">Regime: {volSeries[volSeries.length - 1]?.value > 0.25 ? "High Vol" : "Normal"}</Badge>
          </>
        }
      />

      <FilterBar onExport={() => undefined}>
        <TimeRangeSelector value={range} onChange={setRange} />
      </FilterBar>

      <div className="grid grid-cols-2 gap-3 md:grid-cols-3 xl:grid-cols-6">
        <MetricTile label="Portfolio Health" value={healthScore} format="number" hint="Composite score" />
        <MetricTile label="Daily PnL" value={dailyPnl} delta={dailyPnl * 0.02} />
        <MetricTile label="Net Exposure" value={portfolio.data?.netExposure ?? 0} format="compact" />
        <MetricTile label="Risk Score (CVaR)" value={metrics.data?.cvar ?? 0} />
        <MetricTile label="Sharpe" value={metrics.data?.sharpe ?? 0} />
        <MetricTile label="Active Positions" value={portfolio.data?.positions?.length ?? 0} format="number" />
      </div>

      <PanelGrid
        panels={[
          {
            id: "pnl",
            title: "Live PnL",
            subtitle: "Mark-to-market path",
            span: "full",
            content: <LineChartPanel data={pnlSeries} dataKey="value" height={320} />
          },
          {
            id: "vol",
            title: "Volatility Regime",
            subtitle: "Stochastic vol monitor",
            content: <AreaChartPanel data={volSeries} dataKey="value" />
          },
          {
            id: "greeks",
            title: "Greeks Exposure",
            subtitle: "Aggregate sensitivities",
            content: (
              <div className="grid grid-cols-2 gap-3">
                <MetricTile label="Delta" value={metrics.data?.delta ?? 0} />
                <MetricTile label="Gamma" value={metrics.data?.gamma ?? 0} />
                <MetricTile label="Vega" value={metrics.data?.vega ?? 0} />
                <MetricTile label="Theta" value={metrics.data?.theta ?? 0} />
              </div>
            )
          },
          {
            id: "positions",
            title: "Active Positions",
            subtitle: "Top book lines",
            content: (
              <DataTable
                columns={[
                  { key: "sym", header: "Symbol", render: r => r.symbol },
                  { key: "qty", header: "Qty", align: "right", render: r => fmtNumber(r.quantity, 0) },
                  { key: "delta", header: "Δ", align: "right", render: r => fmtNumber(r.delta, 3) }
                ]}
                rows={(portfolio.data?.positions ?? []).slice(0, 8)}
                keyFn={r => r.symbol}
                loading={portfolio.isLoading}
                emptyTitle="No positions"
              />
            )
          },
          {
            id: "drawdown",
            title: "Drawdown Surface",
            subtitle: "Stress visualization",
            content: <Heatmap matrix={stream.heatmap} title="PnL stress grid" />
          },
          {
            id: "stream",
            title: "Desk Stream",
            subtitle: "Live events",
            content: (
              <div className="max-h-64 space-y-2 overflow-y-auto font-mono text-2xs">
                {(stream.messages ?? []).slice(0, 10).map((m, i) => (
                  <div key={i} className="flex justify-between rounded-control border border-border-subtle bg-surface-overlay/50 px-2 py-1.5">
                    <span className="text-ink-secondary">{m.type}</span>
                    <span className="text-ink-faint">{m.value}</span>
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
