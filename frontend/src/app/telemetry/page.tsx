"use client"
import { useMemo, useState } from "react"
import { useTelemetryStream, useTelemetryChannel } from "../../hooks/useTelemetry"
import type { ApiLatencyPayload } from "../../types/telemetry"
import { MetricTile } from "../../components/ui/MetricTile"
import { PageHeader } from "../../components/ui/PageHeader"
import { Panel } from "../../components/ui/Panel"
import { Badge } from "../../components/ui/Badge"
import { Button } from "../../components/ui/Button"
import { FilterBar } from "../../components/ui/FilterBar"
const severityTone = (type: string) => {
  if (type.includes("fail") || type.includes("error")) return "danger"
  if (type.includes("checkpoint") || type.includes("metrics")) return "info"
  return "neutral"
}

export default function TelemetryPage() {
  const [filter, setFilter] = useState("")
  const [paused, setPaused] = useState(false)
  useTelemetryStream(paused ? [] : ["training", "risk", "portfolio", "api.latency"], 80, false)
  const training = useTelemetryChannel("training")
  const latency = useTelemetryChannel<ApiLatencyPayload>("api.latency")
  const status = training.status

  const events = useMemo(() => {
    const merged = [...training.events, ...latency.events].sort(
      (a, b) => new Date(b.timestamp).getTime() - new Date(a.timestamp).getTime()
    )
    if (!filter.trim()) return merged
    const q = filter.toLowerCase()
    return merged.filter(e => e.event_type.toLowerCase().includes(q) || e.channel.toLowerCase().includes(q))
  }, [training.events, latency.events, filter])

  const avgLatency = latency.events.length
    ? latency.events.reduce((acc, e) => acc + Number(e.payload.duration_ms ?? 0), 0) / latency.events.length
    : 0

  return (
    <div className="animate-fade-in space-y-6">
      <PageHeader
        title="Telemetry Console"
        description="Live observability stream with channel filtering, severity tagging, and API latency profiling."
        meta={
          <Badge tone={status === "connected" ? "success" : status === "connecting" ? "warning" : "danger"} dot>
            {status}
          </Badge>
        }
        actions={
          <Button variant="secondary" size="sm" onClick={() => setPaused(p => !p)}>
            {paused ? "Resume Stream" : "Pause Stream"}
          </Button>
        }
      />

      <FilterBar>
        <input
          className="control-input w-64"
          placeholder="Filter events..."
          value={filter}
          onChange={e => setFilter(e.target.value)}
        />
      </FilterBar>

      <div className="grid grid-cols-2 gap-3 lg:grid-cols-4">
        <MetricTile label="Events Buffered" value={events.length} format="number" />
        <MetricTile label="Avg Latency (ms)" value={avgLatency} />
        <MetricTile label="Training Events" value={training.events.length} format="number" />
        <MetricTile label="API Samples" value={latency.events.length} format="number" />
      </div>

      <Panel title="Live Event Feed" subtitle="Newest first · auto-reconnect enabled">
        <div className="max-h-[480px] overflow-y-auto font-mono text-2xs">
          {events.slice(0, 40).map(event => (
            <div
              key={event.id}
              className="grid grid-cols-[100px_1fr_120px_80px] gap-2 border-b border-border-subtle px-2 py-2 hover:bg-surface-overlay/50"
            >
              <span className="text-ink-faint">{new Date(event.timestamp).toLocaleTimeString()}</span>
              <span className="truncate text-ink-secondary">{event.channel}</span>
              <span className="text-ink-primary">{event.event_type}</span>
              <Badge tone={severityTone(event.event_type)} className="justify-self-end">
                {event.source}
              </Badge>
            </div>
          ))}
          {!events.length ? <div className="py-12 text-center text-ink-muted">Waiting for telemetry events...</div> : null}
        </div>
      </Panel>
    </div>
  )
}
