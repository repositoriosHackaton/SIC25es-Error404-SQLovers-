"use client"

interface ConfusionMatrixProps {
  data: {
    truePositives: number
    falsePositives: number
    falseNegatives: number
    trueNegatives: number
  }
}

export function ConfusionMatrix({ data }: ConfusionMatrixProps) {
  const { truePositives, falsePositives, falseNegatives, trueNegatives } = data
  const total = truePositives + falsePositives + falseNegatives + trueNegatives

  // Calculate percentages for display
  const tpPercent = Math.round((truePositives / total) * 100)
  const fpPercent = Math.round((falsePositives / total) * 100)
  const fnPercent = Math.round((falseNegatives / total) * 100)
  const tnPercent = Math.round((trueNegatives / total) * 100)

  return (
    <div className="w-full max-w-md">
      <div className="grid grid-cols-[1fr_2fr_2fr] text-center">
        <div className="border p-2"></div>
        <div className="border p-2 font-medium bg-muted/50">Predicted Positive</div>
        <div className="border p-2 font-medium bg-muted/50">Predicted Negative</div>

        <div className="border p-2 font-medium bg-muted/50">Actual Positive</div>
        <div className="border p-4 bg-green-500/20 dark:bg-green-500/10">
          <div className="font-bold">True Positive</div>
          <div className="text-2xl font-bold">{truePositives}</div>
          <div className="text-sm text-muted-foreground">{tpPercent}% of total</div>
        </div>
        <div className="border p-4 bg-red-500/20 dark:bg-red-500/10">
          <div className="font-bold">False Negative</div>
          <div className="text-2xl font-bold">{falseNegatives}</div>
          <div className="text-sm text-muted-foreground">{fnPercent}% of total</div>
        </div>

        <div className="border p-2 font-medium bg-muted/50">Actual Negative</div>
        <div className="border p-4 bg-red-500/20 dark:bg-red-500/10">
          <div className="font-bold">False Positive</div>
          <div className="text-2xl font-bold">{falsePositives}</div>
          <div className="text-sm text-muted-foreground">{fpPercent}% of total</div>
        </div>
        <div className="border p-4 bg-green-500/20 dark:bg-green-500/10">
          <div className="font-bold">True Negative</div>
          <div className="text-2xl font-bold">{trueNegatives}</div>
          <div className="text-sm text-muted-foreground">{tnPercent}% of total</div>
        </div>
      </div>
    </div>
  )
}