"use client"
import { InstitutionalChart } from "./InstitutionalChart"

export function AreaChartPanel({
  data,
  dataKey: _dataKey,
  height,
  showBrush = true
}: {
  data: { index: number; value: number }[]
  dataKey: "value"
  height?: number
  showBrush?: boolean
}) {
  return <InstitutionalChart data={data} variant="area" height={height ?? 280} color="#34d399" showBrush={showBrush} />
}
