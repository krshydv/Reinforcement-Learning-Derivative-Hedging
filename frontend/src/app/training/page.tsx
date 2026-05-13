"use client"
import { PanelGrid } from "../../components/layout/PanelGrid"
import { LineChartPanel } from "../../components/charts/LineChartPanel"
import { AreaChartPanel } from "../../components/charts/AreaChartPanel"
import { Heatmap } from "../../components/charts/Heatmap"
import { useTrainingMetrics } from "../../lib/queries"

export default function TrainingPage() {
  const training = useTrainingMetrics()
  const rewardSeries = training.data?.rewards ?? []
  const lossSeries = training.data?.losses ?? []

  return (
    <PanelGrid
      panels={[
        {
          id: "reward",
          title: "Reward Progression",
          content: <LineChartPanel data={rewardSeries} dataKey="value" />
        },
        {
          id: "loss",
          title: "Policy Loss",
          content: <AreaChartPanel data={lossSeries} dataKey="value" />
        },
        {
          id: "heat",
          title: "Episode Heatmap",
          content: <Heatmap matrix={training.data?.heatmap ?? []} />
        },
        {
          id: "gpu",
          title: "Resource Utilization",
          content: <LineChartPanel data={training.data?.utilization ?? []} dataKey="value" />
        }
      ]}
    />
  )
}
