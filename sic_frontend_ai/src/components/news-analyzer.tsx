"use client";

import { useState } from "react";
import { analyzeNews } from "@/lib/api";
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs";
import { Button } from "@/components/ui/button";
import { Textarea } from "@/components/ui/textarea";
import { Input } from "@/components/ui/input";
import {
  Card,
  CardContent,
  CardDescription,
  CardFooter,
  CardHeader,
  CardTitle,
} from "@/components/ui/card";
import { Label } from "@/components/ui/label";
import {
  Loader2,
  Upload,
  LinkIcon,
  FileText,
  AlertTriangle,
} from "lucide-react";
import { AnalysisResults } from "@/components/analysis-results";

type InputType = "text" | "url" | "image";
type AnalysisStatus = "idle" | "loading" | "success" | "error";
type PredictionMode = "default" | "all" | "single";

interface AnalysisResult {
  final_prediction: string;
  explanation: string;
  predictions: Record<
    string,
    { accuracy: number; prediction: string; prediction_time: number }
  >;
  confidence: number;
}

const MODELS = [
  { code: "logistic", name: "Logistic" },
  { code: "random_forest", name: "Random Forest" },
  { code: "xgboost", name: "XG Boost" },
  { code: "naive_bayes", name: "Naive Bayes" },
  { code: "neural_network", name: "Neural Network" },
];

export function NewsAnalyzer() {
  const [inputType, setInputType] = useState<InputType>("text");
  const [textInput, setTextInput] = useState("");
  const [urlInput, setUrlInput] = useState("");
  const [imageFile, setImageFile] = useState<File | null>(null);
  const [status, setStatus] = useState<AnalysisStatus>("idle");
  const [result, setResult] = useState<AnalysisResult | null>(null);
  const [error, setError] = useState<string | null>(null);
  const [tab, setTab] = useState<"general" | "devs">("general");
  const [predictionMode, setPredictionMode] =
    useState<PredictionMode>("default");
  const [selectedModel, setSelectedModel] = useState<string>("naive_bayes");

  const handleFileChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    if (e.target.files && e.target.files[0]) {
      setImageFile(e.target.files[0]);
    }
  };

  const handleAnalyze = async () => {
    setStatus("loading");
    setError(null);

    try {
      if (!textInput.trim()) {
        throw new Error("Please enter some text to analyze");
      }

      const data = await analyzeNews(textInput, predictionMode, selectedModel);
      setResult(data);
      setStatus("success");
    } catch (err) {
      setError(
        err instanceof Error ? err.message : "An unknown error occurred"
      );
      setStatus("error");
    }
  };

  const resetForm = () => {
    setTextInput("");
    setUrlInput("");
    setImageFile(null);
    setResult(null);
    setError(null);
    setStatus("idle");
  };

  return (
    <div className="w-full max-w-3xl mx-auto">
      <Card className="shadow-lg border-3">
        <CardHeader>
          <CardTitle>Analyze News Content</CardTitle>
          <CardDescription>
            Enter news content for verification using one of the methods below
          </CardDescription>
        </CardHeader>
        <CardContent>
          {result ? (
            <AnalysisResults result={result} onReset={resetForm} />
          ) : (
            <>
              <Tabs
                defaultValue="general"
                onValueChange={(value) => setTab(value as "general" | "devs")}
              >
                <TabsList className="grid w-full grid-cols-2 mb-6">
                  <TabsTrigger value="general">General</TabsTrigger>
                  <TabsTrigger value="devs">For Devs</TabsTrigger>
                </TabsList>

                {/* General Mode */}
                <TabsContent value="general">
                  <Label className="my-3" htmlFor="text-input">
                    Paste news article text
                  </Label>
                  <Textarea
                    id="text-input"
                    placeholder="Paste the full text of the news article here..."
                    className="min-h-[200px]"
                    value={textInput}
                    onChange={(e) => setTextInput(e.target.value)}
                  />
                </TabsContent>

                {/* For Devs Mode */}
                <TabsContent value="devs">
                  <div>
                    <Label>Prediction Mode</Label>
                    <div className="flex space-x-2 mt-2">
                      <Button
                        variant={
                          predictionMode === "all" ? "default" : "outline"
                        }
                        size="sm"
                        onClick={() => setPredictionMode("all")}
                      >
                        All Models
                      </Button>
                      <Button
                        variant={
                          predictionMode === "single" ? "default" : "outline"
                        }
                        size="sm"
                        onClick={() => setPredictionMode("single")}
                      >
                        Custom Model
                      </Button>
                    </div>
                  </div>

                  {predictionMode === "single" && (
                    <div className="mt-4">
                      <Label className="mb-3">Select Model</Label>
                      <select
                        value={selectedModel}
                        onChange={(e) => setSelectedModel(e.target.value)}
                        className="flex h-10 w-full rounded-md border border-input bg-background px-3 py-2 text-sm"
                      >
                        {MODELS.map((model) => (
                          <option key={model.code} value={model.code}>
                            {model.name}
                          </option>
                        ))}
                      </select>
                    </div>
                  )}

                  <Label className="my-3" htmlFor="text-input">
                    Paste news article text
                  </Label>
                  <Textarea
                    id="text-input"
                    placeholder="Paste the full text of the news article here..."
                    className="min-h-[200px]"
                    value={textInput}
                    onChange={(e) => setTextInput(e.target.value)}
                  />
                </TabsContent>
              </Tabs>
            </>
          )}
        </CardContent>
        <CardFooter className="flex justify-end space-x-3">
          {result ? (
            <Button
              onClick={resetForm}
              variant="outline"
              className="w-full sm:w-auto"
            >
              Analyze Other
            </Button>
          ) : (
            <Button
              onClick={handleAnalyze}
              disabled={status === "loading"}
              className="w-full sm:w-auto"
            >
              {status === "loading" ? (
                <Loader2 className="mr-2 h-4 w-4 animate-spin" />
              ) : (
                "Analyze Content"
              )}
            </Button>
          )}
        </CardFooter>
      </Card>
    </div>
  );
}
