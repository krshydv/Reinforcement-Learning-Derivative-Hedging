"use client"
import { PanelGrid } from "../../components/layout/PanelGrid"
import { LineChartPanel } from "../../components/charts/LineChartPanel"
import { Heatmap } from "../../components/charts/Heatmap"
import { useResearchAnalytics } from "../../lib/queries"
import { PageHeader } from "../../components/ui/PageHeader"
import { Badge } from "../../components/ui/Badge"

export default function ResearchPage() {
  const research = useResearchAnalytics()
  return (
    <div className="animate-fade-in space-y-6">
      <PageHeader
        title="Research Lab"
        description="Volatility surfaces, greeks tensors, Monte Carlo paths, and strategy benchmarking for quant research."
        meta={<Badge tone="accent">Heston calibration</Badge>}
      />
      <PanelGrid
        panels={[
          { id: "bench", title: "Strategy Benchmarking", content: <LineChartPanel data={research.data?.benchmarkSeries ?? []} dataKey="value" /> },
          { id: "surface", title: "Volatility Surface", content: <Heatmap matrix={research.data?.volSurface ?? []} /> },
          { id: "greeks", title: "Greeks Surface", content: <Heatmap matrix={research.data?.greeksSurface ?? []} /> },
          { id: "mc", title: "Monte Carlo Paths", content: <LineChartPanel data={research.data?.paths ?? []} dataKey="value" /> }
        ]}
      />
    </div>
  )
}
