"use client"
import { LineChart, Line, ResponsiveContainer, XAxis, YAxis, Tooltip } from "recharts"

export function LineChartPanel({ data, dataKey }: { data: { index: number; value: number }[]; dataKey: "value" }) {
  return (
    <div className="h-56">
      <ResponsiveContainer width="100%" height="100%">
        <LineChart data={data}>
          <XAxis dataKey="index" stroke="#64748b" />
          <YAxis stroke="#64748b" />
          <Tooltip contentStyle={{ background: "#0f172a", border: "none" }} />
          <Line type="monotone" dataKey={dataKey} stroke="#3b82f6" strokeWidth={2} dot={false} />
        </LineChart>
      </ResponsiveContainer>
    </div>
  )
}
