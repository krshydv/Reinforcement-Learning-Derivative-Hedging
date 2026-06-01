"use client"
import { PanelGrid } from "../../components/layout/PanelGrid"
import { LineChartPanel } from "../../components/charts/LineChartPanel"
import { AreaChartPanel } from "../../components/charts/AreaChartPanel"
import { Heatmap } from "../../components/charts/Heatmap"
import { useTrainingMetrics, useTrainingRuns } from "../../lib/queries"
import { PageHeader } from "../../components/ui/PageHeader"
import { DataTable } from "../../components/ui/DataTable"
import { MetricTile } from "../../components/ui/MetricTile"
import { Badge } from "../../components/ui/Badge"

export default function TrainingPage() {
  const training = useTrainingMetrics()
  const runs = useTrainingRuns()
  const rewardSeries = training.data?.rewards ?? []
  const lossSeries = training.data?.losses ?? []
  const activeRuns = (runs.data ?? []).filter(r => r.status === "running").length

  return (
    <div className="animate-fade-in space-y-6">
      <PageHeader
        title="RL Training Operations"
        description="MLOps console for experiment runs, reward curves, policy loss, and resource utilization."
        meta={
          <>
            <Badge tone="success" dot>
              {activeRuns} active runs
            </Badge>
            <Badge tone="info">SB3 · PPO/SAC/TD3</Badge>
          </>
        }
      />

      <div className="grid grid-cols-2 gap-3 lg:grid-cols-4">
        <MetricTile label="Total Runs" value={runs.data?.length ?? 0} format="number" />
        <MetricTile label="Latest Reward" value={rewardSeries[rewardSeries.length - 1]?.value ?? 0} />
        <MetricTile label="Policy Loss" value={lossSeries[lossSeries.length - 1]?.value ?? 0} />
        <MetricTile label="GPU Util %" value={training.data?.utilization?.[0]?.value ?? 0} format="pct" />
      </div>

      <PanelGrid
        panels={[
          {
            id: "runs",
            title: "Experiment Registry",
            subtitle: "Active and historical runs",
            span: "full",
            content: (
              <DataTable
                columns={[
                  { key: "exp", header: "Experiment", render: r => r.experiment_name },
                  { key: "algo", header: "Algorithm", render: r => r.algorithm },
                  { key: "steps", header: "Timesteps", align: "right", render: r => r.timesteps.toLocaleString() },
                  {
                    key: "status",
                    header: "Status",
                    render: r => (
                      <Badge tone={r.status === "completed" ? "success" : r.status === "running" ? "warning" : "neutral"}>
                        {r.status}
                      </Badge>
                    )
                  },
                  { key: "updated", header: "Updated", render: r => new Date(r.updated_at).toLocaleString() }
                ]}
                rows={runs.data ?? []}
                keyFn={r => r.run_id}
                loading={runs.isLoading}
              />
            )
          },
          { id: "reward", title: "Reward Curve", subtitle: "Episode returns", content: <LineChartPanel data={rewardSeries} dataKey="value" /> },
          { id: "loss", title: "Policy Loss", subtitle: "Optimization trajectory", content: <AreaChartPanel data={lossSeries} dataKey="value" /> },
          { id: "heat", title: "Episode Heatmap", subtitle: "Rollout diagnostics", content: <Heatmap matrix={training.data?.heatmap ?? []} /> },
          { id: "gpu", title: "Resource Utilization", subtitle: "Cluster load", content: <LineChartPanel data={training.data?.utilization ?? []} dataKey="value" /> }
        ]}
      />
    </div>
  )
}
