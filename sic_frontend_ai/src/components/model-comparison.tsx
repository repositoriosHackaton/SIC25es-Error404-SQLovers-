"use client"

import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card"
import {
  ResponsiveContainer,
  RadarChart,
  PolarGrid,
  PolarAngleAxis,
  PolarRadiusAxis,
  Radar,
  Legend,
  Tooltip,
} from "recharts"

const modelComparisonData = [
  { metric: "Text Analysis", "Naive Bayes": 80, "Neural Network": 95, "Random Forest": 85, XGBoost: 90, Logistic: 75 },
  { metric: "URL Analysis", "Naive Bayes": 70, "Neural Network": 85, "Random Forest": 90, XGBoost: 95, Logistic: 65 },
  { metric: "Image Analysis", "Naive Bayes": 60, "Neural Network": 90, "Random Forest": 75, XGBoost: 80, Logistic: 55 },
  { metric: "Speed", "Naive Bayes": 95, "Neural Network": 70, "Random Forest": 80, XGBoost: 75, Logistic: 90 },
  { metric: "Explainability", "Naive Bayes": 85, "Neural Network": 60, "Random Forest": 80, XGBoost: 75, Logistic: 90 },
  { metric: "Adaptability", "Naive Bayes": 65, "Neural Network": 90, "Random Forest": 80, XGBoost: 85, Logistic: 60 },
]

export function ModelComparison() {
  return (
    <Card>
      <CardHeader>
        <CardTitle>Model Comparison</CardTitle>
        <CardDescription>Performance across different metrics</CardDescription>
      </CardHeader>
      <CardContent>
        <div className="h-[500px] w-full">
          <ResponsiveContainer width="100%" height="100%">
            <RadarChart outerRadius="80%" data={modelComparisonData}>
              <PolarGrid />
              <PolarAngleAxis dataKey="metric" />
              <PolarRadiusAxis angle={30} domain={[0, 100]} />
              <Tooltip
                contentStyle={{
                  backgroundColor: "var(--background)",
                  borderColor: "var(--border)",
                  borderRadius: "0.5rem",
                  boxShadow: "var(--shadow)",
                }}
              />
              <Radar name="Naive Bayes" dataKey="Naive Bayes" stroke="#8884d8" fill="#8884d8" fillOpacity={0.2} />
              <Radar name="Neural Network" dataKey="Neural Network" stroke="#82ca9d" fill="#82ca9d" fillOpacity={0.2} />
              <Radar name="Random Forest" dataKey="Random Forest" stroke="#ffc658" fill="#ffc658" fillOpacity={0.2} />
              <Radar name="XGBoost" dataKey="XGBoost" stroke="#ff8042" fill="#ff8042" fillOpacity={0.2} />
              <Radar name="Logistic" dataKey="Logistic" stroke="#0088fe" fill="#0088fe" fillOpacity={0.2} />
              <Legend />
            </RadarChart>
          </ResponsiveContainer>
        </div>
      </CardContent>
    </Card>
  )
}

