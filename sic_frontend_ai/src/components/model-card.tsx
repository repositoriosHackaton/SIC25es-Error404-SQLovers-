import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card"
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs"
import { FeatureImportanceChart } from "@/components/feature-importance-chart"
import { ConfusionMatrix } from "@/components/confusion-matrix"
import { MetricsChart } from "@/components/metrics-chart"

interface FeatureImportance {
  feature: string
  importance: number
}

interface ModelCardProps {
  name: string
  description: string
  accuracy: number
  precision: number
  recall: number
  f1Score: number
  strengths: string[]
  weaknesses: string[]
  useCases: string[]
  featureImportance: FeatureImportance[]
}

export function ModelCard({
  name,
  description,
  accuracy,
  precision,
  recall,
  f1Score,
  strengths,
  weaknesses,
  useCases,
  featureImportance,
}: ModelCardProps) {
  // Calculate confusion matrix values based on provided metrics
  // These are approximations for visualization purposes
  const total = 1000
  const truePositives = Math.round((recall * precision * total) / 100)
  const falseNegatives = Math.round(truePositives * (1 / recall - 1))
  const falsePositives = Math.round(truePositives * (1 / precision - 1))
  const trueNegatives = total - truePositives - falsePositives - falseNegatives

  const confusionMatrixData = {
    truePositives,
    falsePositives,
    falseNegatives,
    trueNegatives,
  }

  return (
    <div className="grid gap-6 md:grid-cols-2 lg:grid-cols-3 mt-6">
      <Card className="md:col-span-2 lg:col-span-1">
        <CardHeader>
          <CardTitle>{name} Model</CardTitle>
          <CardDescription>{description}</CardDescription>
        </CardHeader>
        <CardContent>
          <div className="space-y-6">
            <div>
              <h3 className="font-medium mb-2">Performance Metrics</h3>
              <div className="grid grid-cols-2 gap-4">
                <div className="flex flex-col">
                  <span className="text-sm text-muted-foreground">Accuracy</span>
                  <span className="text-2xl font-bold">{accuracy}%</span>
                </div>
                <div className="flex flex-col">
                  <span className="text-sm text-muted-foreground">Precision</span>
                  <span className="text-2xl font-bold">{precision}%</span>
                </div>
                <div className="flex flex-col">
                  <span className="text-sm text-muted-foreground">Recall</span>
                  <span className="text-2xl font-bold">{recall}%</span>
                </div>
                <div className="flex flex-col">
                  <span className="text-sm text-muted-foreground">F1 Score</span>
                  <span className="text-2xl font-bold">{f1Score}%</span>
                </div>
              </div>
            </div>

            <div>
              <h3 className="font-medium mb-2">Strengths</h3>
              <ul className="list-disc pl-5 space-y-1">
                {strengths.map((strength, index) => (
                  <li key={index} className="text-sm">
                    {strength}
                  </li>
                ))}
              </ul>
            </div>

            <div>
              <h3 className="font-medium mb-2">Limitations</h3>
              <ul className="list-disc pl-5 space-y-1">
                {weaknesses.map((weakness, index) => (
                  <li key={index} className="text-sm">
                    {weakness}
                  </li>
                ))}
              </ul>
            </div>

            <div>
              <h3 className="font-medium mb-2">Primary Use Cases</h3>
              <ul className="list-disc pl-5 space-y-1">
                {useCases.map((useCase, index) => (
                  <li key={index} className="text-sm">
                    {useCase}
                  </li>
                ))}
              </ul>
            </div>
          </div>
        </CardContent>
      </Card>

      <Card className="lg:col-span-2">
        <CardHeader>
          <CardTitle>Model Visualizations</CardTitle>
          <CardDescription>Performance metrics and feature importance</CardDescription>
        </CardHeader>
        <CardContent>
          <Tabs defaultValue="metrics">
            <TabsList className="grid w-full grid-cols-3">
              <TabsTrigger value="metrics">Performance Metrics</TabsTrigger>
              <TabsTrigger value="confusion">Confusion Matrix</TabsTrigger>
              <TabsTrigger value="features">Feature Importance</TabsTrigger>
            </TabsList>
            <TabsContent value="metrics" className="pt-4">
              <div className="h-[350px]">
                <MetricsChart accuracy={accuracy} precision={precision} recall={recall} f1Score={f1Score} />
              </div>
            </TabsContent>
            <TabsContent value="confusion" className="pt-4">
              <div className="h-[350px] flex items-center justify-center">
                <ConfusionMatrix data={confusionMatrixData} />
              </div>
            </TabsContent>
            <TabsContent value="features" className="pt-4">
              <div className="h-[350px]">
                <FeatureImportanceChart data={featureImportance} />
              </div>
            </TabsContent>
          </Tabs>
        </CardContent>
      </Card>
    </div>
  )
}

