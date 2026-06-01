"use client"
import { PanelGrid } from "../../components/layout/PanelGrid"
import { MetricTile } from "../../components/ui/MetricTile"
import { useTelemetryChannel, useTelemetryStream } from "../../hooks/useTelemetry"
import type { ApiLatencyPayload } from "../../types/telemetry"
import { PageHeader } from "../../components/ui/PageHeader"
import { Badge } from "../../components/ui/Badge"
import { fmtNumber } from "../../lib/format"

export default function HealthPage() {
  useTelemetryStream(["api.latency"], 30, false)
  const latency = useTelemetryChannel<ApiLatencyPayload>("api.latency")
  const avgLatency = latency.events.length
    ? latency.events.reduce((acc, event) => acc + Number(event.payload.duration_ms ?? 0), 0) / latency.events.length
    : 0

  return (
    <div className="animate-fade-in space-y-6">
      <PageHeader
        title="System Health"
        description="Operational health dashboard with API latency traces and telemetry connectivity."
        meta={<Badge tone={latency.status === "connected" ? "success" : "warning"} dot>{latency.status}</Badge>}
      />
      <div className="grid grid-cols-2 gap-3 lg:grid-cols-4">
        <MetricTile label="API Gateway" value={1} />
        <MetricTile label="Telemetry" value={latency.events.length > 0 ? 1 : 0} />
        <MetricTile label="Avg Latency (ms)" value={avgLatency} />
        <MetricTile label="Samples" value={latency.events.length} format="number" />
      </div>
      <PanelGrid
        panels={[
          {
            id: "activity",
            title: "Request Timeline",
            subtitle: "Recent API calls",
            span: "full",
            content: (
              <div className="max-h-80 overflow-y-auto font-mono text-2xs">
                {latency.events.slice(0, 20).map(event => (
                  <div key={event.id} className="grid grid-cols-[80px_1fr_80px] gap-2 border-b border-border-subtle py-2">
                    <span className="text-ink-faint">{event.payload.method}</span>
                    <span className="truncate text-ink-secondary">{event.payload.path}</span>
                    <span className="text-right text-ink-primary">{fmtNumber(Number(event.payload.duration_ms ?? 0), 2)} ms</span>
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
