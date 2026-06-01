"use client"
import { memo } from "react"
import {
  Area,
  AreaChart,
  Brush,
  CartesianGrid,
  Legend,
  Line,
  LineChart,
  ReferenceLine,
  ResponsiveContainer,
  Tooltip,
  XAxis,
  YAxis
} from "recharts"
import { ChartTooltip } from "./ChartTooltip"

export type ChartPoint = { index: number; value: number; label?: string }

function InstitutionalChartInner({
  data,
  variant = "line",
  height = 280,
  color = "#38bdf8",
  yLabel,
  showBrush = true,
  showLegend = false
}: {
  data: ChartPoint[]
  variant?: "line" | "area"
  height?: number
  color?: string
  yLabel?: string
  showBrush?: boolean
  showLegend?: boolean
}) {
  const chartProps = {
    data,
    margin: { top: 8, right: 8, left: 0, bottom: showBrush ? 24 : 0 }
  }
  const seriesProps = {
    type: "monotone" as const,
    dataKey: "value",
    name: "Value",
    stroke: color,
    strokeWidth: 2,
    dot: false,
    activeDot: { r: 4, strokeWidth: 0, fill: color },
    isAnimationActive: true,
    animationDuration: 450
  }
  const chartChildren = (
    <>
      <defs>
        <linearGradient id="chartFill" x1="0" y1="0" x2="0" y2="1">
          <stop offset="0%" stopColor={color} stopOpacity={0.35} />
          <stop offset="100%" stopColor={color} stopOpacity={0} />
        </linearGradient>
      </defs>
      <CartesianGrid strokeDasharray="3 3" vertical={false} />
      <XAxis dataKey="index" tick={{ fill: "#64748b", fontSize: 10 }} axisLine={false} tickLine={false} />
      <YAxis
        tick={{ fill: "#64748b", fontSize: 10 }}
        axisLine={false}
        tickLine={false}
        width={48}
        label={yLabel ? { value: yLabel, angle: -90, position: "insideLeft", fill: "#64748b", fontSize: 10 } : undefined}
      />
      <Tooltip content={<ChartTooltip />} cursor={{ stroke: "rgba(148,163,184,0.35)", strokeWidth: 1 }} />
      {showLegend ? <Legend wrapperStyle={{ fontSize: 11, color: "#94a3b8" }} /> : null}
      <ReferenceLine y={0} stroke="rgba(148,163,184,0.2)" />
      {variant === "area" ? (
        <Area {...seriesProps} fill="url(#chartFill)" />
      ) : (
        <Line {...seriesProps} />
      )}
      {showBrush && data.length > 20 ? (
        <Brush dataKey="index" height={22} stroke="#334155" fill="#0f172a" travellerWidth={8} />
      ) : null}
    </>
  )

  return (
    <div style={{ height }} className="w-full">
      <ResponsiveContainer width="100%" height="100%">
        {variant === "area" ? (
          <AreaChart {...chartProps}>{chartChildren}</AreaChart>
        ) : (
          <LineChart {...chartProps}>{chartChildren}</LineChart>
        )}
      </ResponsiveContainer>
    </div>
  )
}

export const InstitutionalChart = memo(InstitutionalChartInner)
