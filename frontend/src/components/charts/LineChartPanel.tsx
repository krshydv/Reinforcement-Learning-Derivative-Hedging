"use client"
import { InstitutionalChart } from "./InstitutionalChart"

export function LineChartPanel({
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
  return <InstitutionalChart data={data} variant="line" height={height ?? 280} showBrush={showBrush} />
}
