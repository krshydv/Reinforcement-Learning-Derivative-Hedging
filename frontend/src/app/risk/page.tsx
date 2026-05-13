"use client"
import { PanelGrid } from "../../components/layout/PanelGrid"
import { Heatmap } from "../../components/charts/Heatmap"
import { AreaChartPanel } from "../../components/charts/AreaChartPanel"
import { useRiskAnalytics } from "../../lib/queries"

export default function RiskPage() {
  const risk = useRiskAnalytics()
  return (
    <PanelGrid
      panels={[
        {
          id: "var",
          title: "VaR / CVaR",
          content: <AreaChartPanel data={risk.data?.varSeries ?? []} dataKey="value" />
        },
        {
          id: "tail",
          title: "Tail Risk Surface",
          content: <Heatmap matrix={risk.data?.tailMatrix ?? []} />
        },
        {
          id: "corr",
          title: "Correlation Matrix",
          content: <Heatmap matrix={risk.data?.corrMatrix ?? []} />
        },
        {
          id: "liquidity",
          title: "Liquidity Stress",
          content: <AreaChartPanel data={risk.data?.liquiditySeries ?? []} dataKey="value" />
        }
      ]}
    />
  )
}
