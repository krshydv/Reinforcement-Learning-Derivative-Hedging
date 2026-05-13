"use client"
import { AreaChart, Area, ResponsiveContainer, XAxis, YAxis, Tooltip } from "recharts"

export function AreaChartPanel({ data, dataKey }: { data: { index: number; value: number }[]; dataKey: "value" }) {
  return (
    <div className="h-56">
      <ResponsiveContainer width="100%" height="100%">
        <AreaChart data={data}>
          <XAxis dataKey="index" stroke="#64748b" />
          <YAxis stroke="#64748b" />
          <Tooltip contentStyle={{ background: "#0f172a", border: "none" }} />
          <Area type="monotone" dataKey={dataKey} stroke="#22c55e" fill="rgba(34,197,94,0.2)" />
        </AreaChart>
      </ResponsiveContainer>
    </div>
  )
}
