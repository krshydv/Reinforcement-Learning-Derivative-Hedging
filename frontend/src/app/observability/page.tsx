"use client"
import { PanelGrid } from "../../components/layout/PanelGrid"
import { LineChartPanel } from "../../components/charts/LineChartPanel"
import { AreaChartPanel } from "../../components/charts/AreaChartPanel"
import { Heatmap } from "../../components/charts/Heatmap"
import { MetricTile } from "../../components/ui/MetricTile"
import { useTelemetryChannel } from "../../hooks/useTelemetry"
import { PageHeader } from "../../components/ui/PageHeader"
import { Badge } from "../../components/ui/Badge"

export default function ObservabilityPage() {
  const metrics = useTelemetryChannel("training.metrics")
  const rewards = metrics.events
    .slice(0, 60)
    .map((event, index) => ({ index, value: Number(event.payload.reward_mean ?? 0) }))
    .reverse()
  const actionStd = metrics.events
    .slice(0, 60)
    .map((event, index) => ({ index, value: Number(event.payload.action_std ?? 0) }))
    .reverse()

  const latest = metrics.events[0]?.payload ?? {}
  const anomalyCount = metrics.events.filter(event => event.payload.anomaly).length
  const heatmap = Array.from({ length: 10 }, (_, i) => Array.from({ length: 10 }, (_, j) => Math.abs(Math.sin((i + 1) * (j + 1) / 6))))

  return (
    <div className="animate-fade-in space-y-6">
      <PageHeader
        title="RL Observability"
        description="Training-time diagnostics: reward tracking, action dispersion, rollout heatmaps, and anomaly detection."
        meta={<Badge tone="info">Metrics channel</Badge>}
      />

      <div className="grid grid-cols-2 gap-3 lg:grid-cols-4">
        <MetricTile label="Latest Reward" value={Number(latest.reward_mean ?? 0)} />
        <MetricTile label="Action Std" value={Number(latest.action_std ?? 0)} />
        <MetricTile label="Steps" value={Number(latest.step ?? 0)} format="compact" />
        <MetricTile label="Anomalies" value={anomalyCount} format="number" />
      </div>

      <PanelGrid
        panels={[
          { id: "reward", title: "Reward Tracking", subtitle: "Policy improvement", content: <LineChartPanel data={rewards} dataKey="value" /> },
          { id: "actions", title: "Action Distribution", subtitle: "Exploration width", content: <AreaChartPanel data={actionStd} dataKey="value" /> },
          { id: "rollout", title: "Rollout Diagnostics", subtitle: "Episode surface", content: <Heatmap matrix={heatmap} /> }
        ]}
      />
    </div>
  )
}
