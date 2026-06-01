"use client"
import { PanelGrid } from "../../components/layout/PanelGrid"
import { MetricTile } from "../../components/ui/MetricTile"
import { Heatmap } from "../../components/charts/Heatmap"
import { PageHeader } from "../../components/ui/PageHeader"
import { Badge } from "../../components/ui/Badge"
import { useTelemetryStore } from "../../store/useTelemetryStore"

export default function InfraPage() {
  const telemetryStatus = useTelemetryStore(s => s.status)
  const resourceHeatmap = Array.from({ length: 10 }, (_, i) => Array.from({ length: 10 }, (_, j) => Math.abs(Math.cos((i + 2) * (j + 1) / 5))))

  return (
    <div className="animate-fade-in space-y-6">
      <PageHeader
        title="Infrastructure"
        description="Service mesh health, resource utilization heatmaps, and platform reliability indicators."
        meta={<Badge tone={telemetryStatus === "connected" ? "success" : "warning"} dot>WebSocket {telemetryStatus}</Badge>}
      />
      <div className="grid grid-cols-2 gap-3 md:grid-cols-4 lg:grid-cols-6">
        <MetricTile label="API" value={1} hint="Healthy" />
        <MetricTile label="PostgreSQL" value={1} hint="Healthy" />
        <MetricTile label="Redis" value={1} hint="Healthy" />
        <MetricTile label="Worker" value={1} hint="Celery ready" />
        <MetricTile label="MLflow" value={1} hint="Tracking" />
        <MetricTile label="Error Rate" value={0.02} format="pct" />
      </div>
      <PanelGrid
        panels={[
          {
            id: "latency",
            title: "Resource Utilization Grid",
            subtitle: "Cluster load surface",
            span: "full",
            content: <Heatmap matrix={resourceHeatmap} title="CPU/Memory pressure" />
          }
        ]}
      />
    </div>
  )
}
