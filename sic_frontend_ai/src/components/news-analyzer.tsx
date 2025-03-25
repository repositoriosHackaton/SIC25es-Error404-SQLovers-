"use client";

import { motion, AnimatePresence } from "framer-motion"
import { useState, useEffect } from "react";
import { analyzeNews, analyzeNewsByImage, analyzeNewsByUrl } from "@/lib/api";
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
  Terminal,
} from "lucide-react";
import { AnalysisResults } from "@/components/analysis-results";

type InputType = "text" | "url" | "image" | "devs";
type AnalysisStatus = "idle" | "loading" | "success" | "error";
type PredictionMode = "default" | "all" | "single";

interface AnalysisResult {
  final_prediction: string;
  explanation: string;
  predictions?: Record<
    string,
    { accuracy: number; prediction: string; prediction_time?: number }
  >;
  confidence?: number;
  extracted_text?: string;
  article_data?: {
    title: string;
    publish_date: string | null;
    text: string;
    top_image: string | null;
  };
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
  const [loadingMessage, setLoadingMessage] = useState<string>("");
  const [tab, setTab] = useState<"general" | "devs" | "url" | "images">(
    "general"
  );
  const [predictionMode, setPredictionMode] =
    useState<PredictionMode>("default");
  const [selectedModel, setSelectedModel] = useState<string>("naive_bayes");
  const [currentMessageIndex, setCurrentMessageIndex] = useState(0)
  const [progress, setProgress] = useState(0)

  const handleFileChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    if (e.target.files && e.target.files[0]) {
      setImageFile(e.target.files[0]);
    }
  };

  const handleAnalyze = async () => {
    setStatus("loading");
    setError(null);

    try {
      let data;
      console.log("Input type:", inputType); 
  
      const effectiveInputType = inputType === "devs" ? "text" : inputType;
  
      if (effectiveInputType === "text") {
        if (!textInput.trim()) throw new Error("Please enter some text to analyze");
  
        if (predictionMode === "all") {
          data = await analyzeNews(textInput, "all");
        } else if (predictionMode === "single") {
          if (!selectedModel) throw new Error("Please select a model");
          data = await analyzeNews(textInput, "single", selectedModel);
        } else {
          data = await analyzeNews(textInput, "default", "logistic");
        }
      } else if (effectiveInputType === "url") {
        if (!urlInput.trim()) throw new Error("Please enter a valid URL");
        console.log("Analyzing URL:", urlInput); 
        data = await analyzeNewsByUrl(urlInput);
      } else if (effectiveInputType === "image") {
        if (!imageFile) throw new Error("Please upload an image");
        data = await analyzeNewsByImage(imageFile);
      }

      console.log("API Response:", data);
      setResult(data);
      setStatus("success");
    } catch (err) {
      console.error("Error:", err); 
      setError(
        err instanceof Error ? err.message : "An unknown error occurred"
      );
      setStatus("error");
    }
  };

  const messages = [
    "Extrayendo el contenido...",
    "Procesando datos...",
    "Procesando con Machine learning...",
    "Analizando resultados...",
    "Verificando autenticidad...",
    "Generando respuesta..",
    "Ya casi terminamos...",
    "Casi listo...",
  ];

  useEffect(() => {
    // Message rotation
    const messageInterval = setInterval(() => {
      setCurrentMessageIndex((prev) => (prev + 1) % messages.length)
    }, 3000)

    // Progress animation
    const progressInterval = setInterval(() => {
      setProgress((prev) => {
        if (prev >= 100) {
          return 0
        }
        return prev + 1
      })
    }, 30)

    return () => {
      clearInterval(messageInterval)
      clearInterval(progressInterval)
    }
  }, [messages.length])

  const resetForm = () => {
    setTextInput("");
    setUrlInput("");
    setImageFile(null);
    setResult(null);
    setError(null);
    setStatus("idle");
  };

  useEffect(() => {
    if (status === "loading") {
      const messages = [
        "Extrayendo el contenido...",
        "Procesando datos...",
        "Procesando con Machine learning...",
        "Analizando resultados...",
        "Verificando autenticidad...",
        "Generando respuesta..",
        "Ya casi terminamos...",
        "Casi listo...",
        "¡Listo!",
      ];
      let index = 0;

      const interval = setInterval(() => {
        setLoadingMessage(messages[index]);
        index = (index + 1) % messages.length;
      }, 2500);

      return () => clearInterval(interval);
    }
  }, [status]);

  return (
    <div className="w-full max-w-4xl mx-auto">
      <Card className="shadow-lg border-3">
        <CardHeader>
          <CardTitle>Analyze News Content</CardTitle>
          <CardDescription>
            Enter news content for verification using one of the methods below
          </CardDescription>
        </CardHeader>
        <CardContent>
          {status === "loading" ? (
            <div className="flex flex-col items-center justify-cente p-4">
            <div className="w-full max-w-md rounded-xl shadow-lg overflow-hidden">
      
              <div className="p-6">
                <div className="flex justify-center mb-6">
                  <motion.div
                    className="w-10 h-10 border-4 border-yellow-100 border-t-yellow-500 rounded-full"
                    animate={{ rotate: 360 }}
                    transition={{
                      duration: 1,
                      repeat: Number.POSITIVE_INFINITY,
                      ease: "linear",
                    }}
                  />
                </div>
      
                <div className="h-16 flex items-center justify-center">
                  <AnimatePresence mode="wait">
                    <motion.div
                      key={currentMessageIndex}
                      initial={{ opacity: 0, y: 10 }}
                      animate={{ opacity: 1, y: 0 }}
                      exit={{ opacity: 0, y: -10 }}
                      transition={{
                        duration: 0.5,
                        ease: "easeInOut",
                      }}
                      className="text-center text-gray-700 font-medium"
                    >
                      {messages[currentMessageIndex]}
                    </motion.div>
                  </AnimatePresence>
                </div>
      
                <div className="flex justify-center mt-4 space-x-2">
                  {[0, 1, 2].map((i) => (
                    <motion.div
                      key={i}
                      className="w-2 h-2 bg-yellow-500 rounded-full"
                      animate={{
                        opacity: [0.3, 1, 0.3],
                        scale: [0.8, 1.2, 0.8],
                      }}
                      transition={{
                        duration: 1.5,
                        repeat: Number.POSITIVE_INFINITY,
                        delay: i * 0.2,
                        ease: "easeInOut",
                      }}
                    />
                  ))}
                </div>
              </div>
            </div>
          </div>
          ) : result ? (
            <AnalysisResults result={result} onReset={resetForm} />
          ) : (
            <>
              <Tabs
                defaultValue="general"
                onValueChange={(value) => setInputType(value as InputType)}
              >
                <TabsList className="grid w-full grid-cols-4 mb-6">
                  <TabsTrigger value="general">
                    <FileText className="mr-2 h-4 w-4" />
                    Text
                  </TabsTrigger>
                  <TabsTrigger value="url">
                    <LinkIcon className="mr-2 h-4 w-4" />
                    URL
                  </TabsTrigger>
                  <TabsTrigger value="image">
                    <Upload className="mr-2 h-4 w-4" />
                    Image
                  </TabsTrigger>
                  <TabsTrigger value="devs">
                    <Terminal className="mr-2 h-4 w-4" />
                    For Devs
                  </TabsTrigger>
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
                    <Label className="my-3" htmlFor="text-input">
                      Prediction Mode
                    </Label>
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

                <TabsContent value="url">
                  <div className="space-y-4">
                    <Label htmlFor="url-input">Enter news article URL</Label>
                    <Input
                      id="url-input"
                      type="url"
                      placeholder="https://noticias.com/nota"
                      value={urlInput}
                      onChange={(e) => setUrlInput(e.target.value)}
                    />
                  </div>
                </TabsContent>

                <TabsContent value="image">
                  <div className="space-y-4">
                    <Label htmlFor="image-input">
                      Upload screenshot of news article
                    </Label>
                    <div className="border-2 border-dashed border-muted-foreground/25 rounded-lg p-6 text-center">
                      <Input
                        id="image-input"
                        type="file"
                        accept="image/*"
                        className="hidden"
                        onChange={(e) => {
                          if (e.target.files && e.target.files[0]) {
                            console.log("Selected file:", e.target.files[0]); // Depuración
                            setImageFile(e.target.files[0]);
                          }
                        }}
                      />
                      <Label
                        htmlFor="image-input"
                        className="flex flex-col items-center justify-center cursor-pointer"
                      >
                        <Upload className="h-10 w-10 text-muted-foreground mb-2" />
                        <span className="text-sm font-medium">
                          {imageFile
                            ? imageFile.name
                            : "Click to upload or drag and drop"}
                        </span>
                        <span className="text-xs text-muted-foreground mt-1">
                          PNG, JPG up to 10MB
                        </span>
                      </Label>
                    </div>
                  </div>
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
