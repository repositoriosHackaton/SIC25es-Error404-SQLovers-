"use client"

import { Bar, BarChart, ResponsiveContainer, XAxis, YAxis, Tooltip } from "recharts"

interface FeatureImportance {
  feature: string
  importance: number
}

interface FeatureImportanceChartProps {
  data: FeatureImportance[]
}

export function FeatureImportanceChart({ data }: FeatureImportanceChartProps) {
  // Sort data by importance in descending order
  const sortedData = [...data].sort((a, b) => b.importance - a.importance)

  // Format data for the chart
  const chartData = sortedData.map((item) => ({
    name: item.feature,
    value: Math.round(item.importance * 100),
  }))

  return (
    <ResponsiveContainer width="100%" height="100%">
      <BarChart data={chartData} layout="vertical" margin={{ top: 10, right: 30, left: 120, bottom: 10 }}>
        <XAxis type="number" domain={[0, 100]} tickFormatter={(value) => `${value}%`} />
        <YAxis type="category" dataKey="name" width={120} />
        <Tooltip
          formatter={(value: number) => [`${value}%`, "Importance"]}
          contentStyle={{
            backgroundColor: "var(--background)",
            borderColor: "var(--border)",
            borderRadius: "0.5rem",
            boxShadow: "var(--shadow)",
          }}
        />
        <Bar dataKey="value" fill="var(--primary)" radius={[0, 4, 4, 0]} barSize={20} />
      </BarChart>
    </ResponsiveContainer>
  )
}

