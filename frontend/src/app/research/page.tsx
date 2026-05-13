"use client"
import { PanelGrid } from "../../components/layout/PanelGrid"
import { LineChartPanel } from "../../components/charts/LineChartPanel"
import { Heatmap } from "../../components/charts/Heatmap"
import { useResearchAnalytics } from "../../lib/queries"

export default function ResearchPage() {
  const research = useResearchAnalytics()
  return (
    <PanelGrid
      panels={[
        {
          id: "bench",
          title: "Strategy Benchmarking",
          content: <LineChartPanel data={research.data?.benchmarkSeries ?? []} dataKey="value" />
        },
        {
          id: "surface",
          title: "Volatility Surface",
          content: <Heatmap matrix={research.data?.volSurface ?? []} />
        },
        {
          id: "greeks",
          title: "Greeks Surface",
          content: <Heatmap matrix={research.data?.greeksSurface ?? []} />
        },
        {
          id: "mc",
          title: "Monte Carlo Paths",
          content: <LineChartPanel data={research.data?.paths ?? []} dataKey="value" />
        }
      ]}
    />
  )
}
