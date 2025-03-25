"use client"

import { Bar, BarChart, ResponsiveContainer, XAxis, YAxis, Tooltip, CartesianGrid } from "recharts"

interface MetricsChartProps {
  accuracy: number
  precision: number
  recall: number
  f1Score: number
}

export function MetricsChart({ accuracy, precision, recall, f1Score }: MetricsChartProps) {
  const data = [
    { name: "Accuracy", value: accuracy },
    { name: "Precision", value: precision },
    { name: "Recall", value: recall },
    { name: "F1 Score", value: f1Score },
  ]

  return (
    <ResponsiveContainer width="100%" height="100%">
      <BarChart data={data} margin={{ top: 20, right: 30, left: 20, bottom: 20 }}>
        <CartesianGrid strokeDasharray="3 3" opacity={0.3} />
        <XAxis dataKey="name" />
        <YAxis domain={[0, 100]} tickFormatter={(value) => `${value}%`} />
        <Tooltip
          formatter={(value: number) => [`${value}%`, "Value"]}
          contentStyle={{
            backgroundColor: "var(--background)",
            borderColor: "var(--border)",
            borderRadius: "0.5rem",
            boxShadow: "var(--shadow)",
          }}
        />
        <Bar dataKey="value" fill="var(--primary)" radius={[4, 4, 0, 0]} barSize={60} />
      </BarChart>
    </ResponsiveContainer>
  )
}

