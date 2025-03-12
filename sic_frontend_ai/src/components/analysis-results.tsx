import { AlertTriangle, CheckCircle, Info, ExternalLink } from "lucide-react"
import { Progress } from "@/components/ui/progress"

interface AnalysisResultProps {
  result: {
    prediction: string
    probability: number
    explanation: string
    alternativeSources: string[]
  }
  onReset: () => void
}

export function AnalysisResults({ result, onReset }: AnalysisResultProps) {
  const { prediction, probability, explanation, alternativeSources } = result
  console.log(prediction)

  const getResultColor = () => {
    if (prediction.toLowerCase().includes("reliable") || prediction.toLowerCase().includes("true")) {
      return "text-green-500"
    }
    if (prediction.toLowerCase().includes("misleading") || prediction.toLowerCase().includes("misleading")) {
      return "text-amber-500"
    }
    if (prediction.toLowerCase().includes("fake") || prediction.toLowerCase().includes("false")) {
      return "text-red-500"
    }

    console.log(prediction)
    return "text-blue-500"
  }

  const getResultIcon = () => {
    if (prediction.toLowerCase().includes("reliable") || prediction.toLowerCase().includes("true")) {
      return <CheckCircle className="h-8 w-8 text-green-500" />
    }
    if (prediction.toLowerCase().includes("misleading") || prediction.toLowerCase().includes("misleading")) {
      return <AlertTriangle className="h-8 w-8 text-amber-500" />
    }
    if (prediction.toLowerCase().includes("fake") || prediction.toLowerCase().includes("false")) {
      return <AlertTriangle className="h-8 w-8 text-red-500" />
    }
    return <Info className="h-8 w-8 text-blue-500" />
  }

  return (
    <div className="space-y-6">
      <div className="flex items-center space-x-4">
        {getResultIcon()}
        <div>
          <h3 className={`text-xl font-bold ${getResultColor()}`}>{prediction}</h3>
          <div className="flex items-center mt-1">
            <span className="text-sm text-muted-foreground mr-2">Confidence:</span>
            <Progress value={probability * 100} className="h-2 w-24" />
            <span className="ml-2 text-sm">{Math.round(probability * 100)}%</span>
          </div>
        </div>
      </div>

      <div>
        <h4 className="font-medium mb-2">Analysis Explanation:</h4>
        <p className="text-muted-foreground">{explanation}</p>
      </div>

      {alternativeSources.length > 0 && (
        <div>
          <h4 className="font-medium mb-2">Verified Sources:</h4>
          <ul className="space-y-2">
            {alternativeSources.map((source, index) => (
              <li key={index} className="flex items-center">
                <ExternalLink className="h-4 w-4 mr-2 text-primary" />
                <a href={source} target="_blank" rel="noopener noreferrer" className="text-primary hover:underline">
                  {source}
                </a>
              </li>
            ))}
          </ul>
        </div>
      )}

      <div className="mt-8 p-4 bg-muted rounded-lg">
        <div className="flex items-start space-x-2">
          <AlertTriangle className="h-5 w-5 text-yellow-500 mt-0.5" />
          <div>
            <h4 className="font-medium">AI Analysis Disclaimer</h4>
            <p className="text-sm text-muted-foreground">
              This analysis is provided by an AI system and may not be 100% accurate. The results should be used as a
              starting point for your own research. Always verify information through multiple trusted sources before
              making decisions based on this analysis.
            </p>
          </div>
        </div>
      </div>
    </div>
  )
}

