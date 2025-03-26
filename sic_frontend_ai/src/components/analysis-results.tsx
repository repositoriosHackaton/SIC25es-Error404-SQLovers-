import { AlertTriangle, CheckCircle, Info } from "lucide-react";
import { Progress } from "@/components/ui/progress";

interface PredictionDetails {
  accuracy?: number;
  prediction: string;
  prediction_time?: number;
}

interface AnalysisResultProps {
  result: {
    final_prediction: string;
    explanation: string;
    predictions?: Record<string, PredictionDetails>;
    confidence?: number;
  };
  onReset: () => void;
}

export function AnalysisResults({ result, onReset }: AnalysisResultProps) {
  const { final_prediction, explanation, predictions, confidence } = result;

  const getResultColor = () => {
    const pred = final_prediction.toLowerCase();
    if (pred.includes("real") || pred.includes("true")) return "text-green-500";
    if (pred.includes("misleading")) return "text-amber-500";
    if (pred.includes("fake") || pred.includes("false")) return "text-red-500";
    return "text-blue-500";
  };

  const getResultIcon = () => {
    const pred = final_prediction.toLowerCase();
    if (pred.includes("real") || pred.includes("true")) return <CheckCircle className="h-8 w-8 text-green-500" />;
    if (pred.includes("misleading")) return <AlertTriangle className="h-8 w-8 text-amber-500" />;
    if (pred.includes("fake") || pred.includes("false")) return <AlertTriangle className="h-8 w-8 text-red-500" />;
    return <Info className="h-8 w-8 text-blue-500" />;
  };

  const parseExplanation = (explanation: string) => {
    const sections = explanation.split(/\d+\.\s+/).filter(Boolean);
    return sections.map((section, index) => (
      <div key={index} className="space-y-2">
        <h4 className="font-medium">{['Análisis del Texto', 'Razones del Resultado', 'Factores Relevantes'][index]}</h4>
        <p className="text-sm text-muted-foreground">{section.trim()}</p>
      </div>
    ));
  };

  return (
    <div className="space-y-6">
      {/* Header - Resultado Final */}
      <div className="flex items-center space-x-4">
        {getResultIcon()}
        <div>
          <h3 className={`text-xl font-bold ${getResultColor()}`}>Potentially {final_prediction}</h3>
          <div className="flex items-center mt-1">
            <span className="text-sm text-muted-foreground mr-2">Confidence:</span>
            <Progress value={(confidence ?? 0) * 100} className="h-2 w-24" />
            <span className="ml-2 text-sm">{Math.round((confidence ?? 0) * 100)}%</span>
          </div>
        </div>
      </div>

      {/* Modelos Evaluados */}
      <div>
        <h4 className="font-medium mb-2">Model Evaluations:</h4>
        <div className="space-y-4">
          {predictions && Object.entries(predictions).map(([model, details]) => (
            <div key={model} className="flex items-center justify-between p-3 bg-muted rounded-lg">
              <div>
                <h4 className="font-medium capitalize">{model.replace(/_/g, ' ')}</h4>
                <p className="text-sm text-muted-foreground">Accuracy: {(details.accuracy ?? 0).toFixed(2)}</p>
                <p className="text-sm text-muted-foreground">Time: {details.prediction_time}s</p>
              </div>
              <div className="flex items-center">
                <Progress value={(details.accuracy ?? 0) * 100} className="h-2 w-24" />
                <span className="ml-2 text-sm">{details.prediction}</span>
              </div>
            </div>
          ))}
        </div>
      </div>

      {/* Explicación del Análisis */}
      <div className="space-y-4">
        <h4 className="font-medium">Analysis Explanation:</h4>
        {parseExplanation(explanation)}
      </div>

      {/* Disclaimer */}
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
  );
}
