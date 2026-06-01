"use client"
import { useState } from "react"
import { PanelGrid } from "../../components/layout/PanelGrid"
import { Heatmap } from "../../components/charts/Heatmap"
import { AreaChartPanel } from "../../components/charts/AreaChartPanel"
import { useRiskAnalytics } from "../../lib/queries"
import { PageHeader } from "../../components/ui/PageHeader"
import { MetricTile } from "../../components/ui/MetricTile"
import { FilterBar, TimeRangeSelector } from "../../components/ui/FilterBar"
import { Badge } from "../../components/ui/Badge"
export default function RiskPage() {
  const [range, setRange] = useState("1M")
  const risk = useRiskAnalytics()

  return (
    <div className="animate-fade-in space-y-6">
      <PageHeader
        title="Risk Management Desk"
        description="VaR/CVaR surveillance, tail risk surfaces, correlation structure, and liquidity stress monitors."
        meta={<Badge tone="warning">Stress testing enabled</Badge>}
      />
      <FilterBar>
        <TimeRangeSelector value={range} onChange={setRange} />
      </FilterBar>

      <div className="grid grid-cols-2 gap-3 lg:grid-cols-3">
        <MetricTile label="VaR (5%)" value={risk.data?.varValue ?? 0} loading={risk.isLoading} />
        <MetricTile label="CVaR" value={risk.data?.cvarValue ?? 0} loading={risk.isLoading} />
        <MetricTile label="Liquidity Stress" value={risk.data?.liquiditySeries?.[0]?.value ?? 0} loading={risk.isLoading} />
      </div>

      <PanelGrid
        panels={[
          { id: "var", title: "VaR / CVaR Path", subtitle: "Return distribution tail", content: <AreaChartPanel data={risk.data?.varSeries ?? []} dataKey="value" /> },
          { id: "tail", title: "Tail Risk Surface", content: <Heatmap matrix={risk.data?.tailMatrix ?? []} title="Tail loss grid" /> },
          { id: "corr", title: "Correlation Matrix", content: <Heatmap matrix={risk.data?.corrMatrix ?? []} title="Asset correlations" /> },
          { id: "liquidity", title: "Liquidity Stress", content: <AreaChartPanel data={risk.data?.liquiditySeries ?? []} dataKey="value" /> }
        ]}
      />
    </div>
  )
}
