"use client"
import { useExperiments } from "../../lib/queries"
import { PanelGrid } from "../../components/layout/PanelGrid"
import { MetricTile } from "../../components/ui/MetricTile"
import { PageHeader } from "../../components/ui/PageHeader"
import { DataTable } from "../../components/ui/DataTable"
import { Badge } from "../../components/ui/Badge"

export default function ExperimentsPage() {
  const experiments = useExperiments()
  const running = experiments.data?.filter(exp => exp.status === "running").length ?? 0

  return (
    <div className="animate-fade-in space-y-6">
      <PageHeader title="Experiment Registry" description="Track RL experiments, algorithms, and lifecycle status across the research organization." />
      <div className="grid grid-cols-2 gap-3 lg:grid-cols-4">
        <MetricTile label="Total Experiments" value={experiments.data?.length ?? 0} format="number" />
        <MetricTile label="Running" value={running} format="number" />
      </div>
      <PanelGrid
        panels={[
          {
            id: "table",
            title: "Experiments",
            span: "full",
            content: (
              <DataTable
                columns={[
                  { key: "name", header: "Name", render: r => r.name },
                  { key: "algo", header: "Algorithm", render: r => r.algorithm },
                  {
                    key: "status",
                    header: "Status",
                    render: r => <Badge tone={r.status === "running" ? "warning" : "neutral"}>{r.status}</Badge>
                  }
                ]}
                rows={experiments.data ?? []}
                keyFn={r => r.id}
                loading={experiments.isLoading}
              />
            )
          }
        ]}
      />
    </div>
  )
}
