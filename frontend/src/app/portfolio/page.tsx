"use client"
import { useMemo } from "react"
import { usePortfolio } from "../../lib/queries"
import { MetricTile } from "../../components/ui/MetricTile"
import { PageHeader } from "../../components/ui/PageHeader"
import { DataTable } from "../../components/ui/DataTable"
import { Panel } from "../../components/ui/Panel"
import { InstitutionalChart } from "../../components/charts/InstitutionalChart"
import { fmtNumber } from "../../lib/format"
import { Badge } from "../../components/ui/Badge"

export default function PortfolioPage() {
  const portfolio = usePortfolio()
  const allocation = useMemo(
    () =>
      (portfolio.data?.positions ?? []).map((p, i) => ({
        index: i,
        value: Math.abs(p.quantity * p.avgPrice)
      })),
    [portfolio.data?.positions]
  )

  return (
    <div className="animate-fade-in space-y-6">
      <PageHeader
        title="Portfolio Explorer"
        description="Institutional book view with exposure breakdown, greeks ladder, and allocation profile."
        meta={<Badge tone="accent">Book: Hedging Master</Badge>}
      />

      <div className="grid grid-cols-2 gap-3 lg:grid-cols-4">
        <MetricTile label="Net Exposure" value={portfolio.data?.netExposure ?? 0} format="compact" loading={portfolio.isLoading} />
        <MetricTile label="Gross Exposure" value={portfolio.data?.grossExposure ?? 0} format="compact" loading={portfolio.isLoading} />
        <MetricTile label="Hedge Ratio" value={portfolio.data?.hedgeRatio ?? 0} format="pct" loading={portfolio.isLoading} />
        <MetricTile label="Positions" value={portfolio.data?.positions?.length ?? 0} format="number" loading={portfolio.isLoading} />
      </div>

      <div className="grid grid-cols-1 gap-4 xl:grid-cols-3">
        <Panel title="Allocation Profile" subtitle="Exposure by line" className="xl:col-span-1">
          <InstitutionalChart data={allocation} variant="area" height={240} showBrush={false} />
        </Panel>
        <Panel title="Position Explorer" subtitle="Greeks-aware holdings" className="xl:col-span-2">
          <DataTable
            columns={[
              { key: "symbol", header: "Symbol", render: r => <span className="font-semibold text-ink-primary">{r.symbol}</span> },
              { key: "qty", header: "Quantity", align: "right", render: r => fmtNumber(r.quantity, 0) },
              { key: "avg", header: "Avg Price", align: "right", render: r => fmtNumber(r.avgPrice, 2) },
              { key: "delta", header: "Delta", align: "right", render: r => fmtNumber(r.delta, 4) },
              { key: "gamma", header: "Gamma", align: "right", render: r => fmtNumber(r.gamma, 6) }
            ]}
            rows={portfolio.data?.positions ?? []}
            keyFn={r => r.symbol}
            loading={portfolio.isLoading}
            emptyTitle="No positions in book"
            emptyDescription="Seed data appears after admin authentication."
          />
        </Panel>
      </div>
    </div>
  )
}
