"use client"
import { PanelGrid } from "../../components/layout/PanelGrid"
import { StatCard } from "../../components/ui/Stat"
import { LineChartPanel } from "../../components/charts/LineChartPanel"
import { AreaChartPanel } from "../../components/charts/AreaChartPanel"
import { Heatmap } from "../../components/charts/Heatmap"
import { useMarketSimulation, useMetrics } from "../../lib/queries"
import { useLiveStream } from "../../hooks/useLiveStream"

export default function DashboardPage() {
  const market = useMarketSimulation({ model: "heston", steps: 200, dt: 0.01, spot: 100, rate: 0.02, vol: 0.2 })
  const metrics = useMetrics()
  const stream = useLiveStream()

  const pnlSeries = (market.data ?? []).map((m, index) => ({ index, value: m.price }))
  const volSeries = (market.data ?? []).map((m, index) => ({ index, value: m.volatility }))

  return (
    <PanelGrid
      panels={[
        {
          id: "pnl",
          title: "Live PnL",
          content: <LineChartPanel data={pnlSeries} dataKey="value" />
        },
        {
          id: "vol",
          title: "Volatility Regime",
          content: <AreaChartPanel data={volSeries} dataKey="value" />
        },
        {
          id: "metrics",
          title: "Risk Metrics",
          content: (
            <div className="grid grid-cols-2 gap-4">
              <StatCard label="Sharpe" value={metrics.data?.sharpe ?? 0} />
              <StatCard label="Drawdown" value={metrics.data?.drawdown ?? 0} />
              <StatCard label="CVaR" value={metrics.data?.cvar ?? 0} />
              <StatCard label="Hedge Cost" value={metrics.data?.hedge_cost ?? 0} />
            </div>
          )
        },
        {
          id: "greeks",
          title: "Greeks Exposure",
          content: (
            <div className="grid grid-cols-2 gap-4">
              <StatCard label="Delta" value={metrics.data?.delta ?? 0} />
              <StatCard label="Gamma" value={metrics.data?.gamma ?? 0} />
              <StatCard label="Vega" value={metrics.data?.vega ?? 0} />
              <StatCard label="Theta" value={metrics.data?.theta ?? 0} />
            </div>
          )
        },
        {
          id: "drawdown",
          title: "Drawdown Matrix",
          content: <Heatmap matrix={stream.heatmap} />
        },
        {
          id: "stream",
          title: "Live Stream",
          content: (
            <div className="space-y-2 text-sm text-slate-300">
              {(stream.messages ?? []).slice(0, 6).map((m, i) => (
                <div key={i} className="flex justify-between">
                  <span>{m.type}</span>
                  <span className="text-slate-400">{m.value}</span>
                </div>
              ))}
            </div>
          )
        }
      ]}
    />
  )
}
