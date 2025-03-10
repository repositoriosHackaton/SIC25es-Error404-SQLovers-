"use client"

import type React from "react"

import { useState } from "react"
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs"
import { Button } from "@/components/ui/button"
import { Textarea } from "@/components/ui/textarea"
import { Input } from "@/components/ui/input"
import { Card, CardContent, CardDescription, CardFooter, CardHeader, CardTitle } from "@/components/ui/card"
import { Label } from "@/components/ui/label"
import { Loader2, Upload, LinkIcon, FileText, AlertTriangle } from "lucide-react"
import { AnalysisResults } from "@/components/analysis-results"

type InputType = "text" | "url" | "image"
type AnalysisStatus = "idle" | "loading" | "success" | "error"
type ScopeType = "international" | "national"

interface AnalysisResult {
  prediction: string
  probability: number
  explanation: string
  alternativeSources: string[]
}

interface Country {
  code: string
  name: string
}

const countries: Country[] = [
  { code: "US", name: "United States" },
  { code: "GB", name: "United Kingdom" },
  { code: "SV", name: "El Salvador" },
  { code: "CA", name: "Canada" },
  { code: "AU", name: "Australia" },
  { code: "FR", name: "France" },
  { code: "DE", name: "Germany" },
  { code: "ES", name: "Spain" },
  { code: "IT", name: "Italy" },
  { code: "JP", name: "Japan" },
  { code: "BR", name: "Brazil" },
  { code: "MX", name: "Mexico" },
  { code: "AR", name: "Argentina" },
  { code: "CL", name: "Chile" },
  { code: "CO", name: "Colombia" },
  // Add more countries as needed
]

export function NewsAnalyzer() {
  const [inputType, setInputType] = useState<InputType>("text")
  const [textInput, setTextInput] = useState("")
  const [urlInput, setUrlInput] = useState("")
  const [imageFile, setImageFile] = useState<File | null>(null)
  const [status, setStatus] = useState<AnalysisStatus>("idle")
  const [result, setResult] = useState<AnalysisResult | null>(null)
  const [error, setError] = useState<string | null>(null)
  const [scope, setScope] = useState<ScopeType>("international")
  const [selectedCountry, setSelectedCountry] = useState<string>("US")

  const handleFileChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    if (e.target.files && e.target.files[0]) {
      setImageFile(e.target.files[0])
    }
  }

  const handleAnalyze = async () => {
    setStatus("loading")
    setError(null)

    try {
      // Create form data to send to backend
      const formData = new FormData()

      switch (inputType) {
        case "text":
          if (!textInput.trim()) {
            throw new Error("Please enter some text to analyze")
          }
          formData.append("content_type", "text")
          formData.append("content", textInput)
          break
        case "url":
          if (!urlInput.trim()) {
            throw new Error("Please enter a URL to analyze")
          }
          formData.append("content_type", "url")
          formData.append("content", urlInput)
          break
        case "image":
          if (!imageFile) {
            throw new Error("Please upload an image to analyze")
          }
          formData.append("content_type", "image")
          formData.append("content", imageFile)
          break
      }

      // Add scope information to the form data
      formData.append("scope", scope)
      if (scope === "national") {
        formData.append("country", selectedCountry)
      }

      // In a real application, you would send this to your backend
      // const response = await fetch("/api/analyze-news", {
      //   method: "POST",
      //   body: formData,
      // });

      // if (!response.ok) {
      //   throw new Error("Failed to analyze content");
      // }

      // const data = await response.json();
      // setResult(data);

      // For demonstration purposes, we'll simulate a response
      setTimeout(() => {
        setResult({
          prediction: "Potentially Misleading",
          probability: 0.78,
          explanation:
            "The article contains several claims that contradict verified sources. The tone is sensationalist and lacks proper citations for key assertions.",
          alternativeSources: [
            "https://www.reuters.com/fact-check/",
            "https://www.bbc.com/news/reality_check",
            "https://www.factcheck.org/",
          ],
        })
        setStatus("success")
      }, 2000)
    } catch (err) {
      setError(err instanceof Error ? err.message : "An unknown error occurred")
      setStatus("error")
    }
  }

  const resetForm = () => {
    setTextInput("")
    setUrlInput("")
    setImageFile(null)
    setResult(null)
    setError(null)
    setStatus("idle")
  }

  return (
    <div className="w-full max-w-3xl mx-auto">
      <Card className="shadow-lg border-3">
        <CardHeader>
          <CardTitle >Analyze News Content</CardTitle>
          <CardDescription>Enter news content for verification using one of the methods below</CardDescription>
        </CardHeader>
        <CardContent>
          {result ? (
            <AnalysisResults result={result} onReset={resetForm} />
          ) : (
            <>
              <div className="mb-6 space-y-4">
                <div className="flex flex-col space-y-2">
                  <Label htmlFor="scope-selector">News Scope</Label>
                  <div className="flex items-center space-x-2">
                    <div className="flex items-center space-x-2">
                      <Button
                        variant={scope === "international" ? "default" : "outline"}
                        size="sm"
                        onClick={() => setScope("international")}
                      >
                        International
                      </Button>
                      <Button
                        variant={scope === "national" ? "default" : "outline"}
                        size="sm"
                        onClick={() => setScope("national")}
                      >
                        National
                      </Button>
                    </div>
                  </div>
                </div>

                {scope === "national" && (
                  <div className="flex flex-col space-y-2">
                    <Label htmlFor="country-selector">Select Country</Label>
                    <select
                      id="country-selector"
                      value={selectedCountry}
                      onChange={(e) => setSelectedCountry(e.target.value)}
                      className="flex h-10 w-full rounded-md border border-input bg-background px-3 py-2 text-sm ring-offset-background file:border-0 file:bg-transparent file:text-sm file:font-medium placeholder:text-muted-foreground focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring focus-visible:ring-offset-2 disabled:cursor-not-allowed disabled:opacity-50"
                    >
                      {countries.map((country) => (
                        <option key={country.code} value={country.code}>
                          {country.name}
                        </option>
                      ))}
                    </select>
                  </div>
                )}
              </div>
              <Tabs defaultValue="text" onValueChange={(value) => setInputType(value as InputType)}>
                <TabsList className="grid w-full grid-cols-3 mb-6">
                  <TabsTrigger value="text">
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
                </TabsList>

                <TabsContent value="text">
                  <div className="space-y-4">
                    <Label htmlFor="text-input">Paste news article text</Label>
                    <Textarea
                      id="text-input"
                      placeholder="Paste the full text of the news article here..."
                      className="min-h-[200px]"
                      value={textInput}
                      onChange={(e) => setTextInput(e.target.value)}
                    />
                  </div>
                </TabsContent>

                <TabsContent value="url">
                  <div className="space-y-4">
                    <Label htmlFor="url-input">Enter news article URL</Label>
                    <Input
                      id="url-input"
                      type="url"
                      placeholder="https://example.com/news-article"
                      value={urlInput}
                      onChange={(e) => setUrlInput(e.target.value)}
                    />
                  </div>
                </TabsContent>

                <TabsContent value="image">
                  <div className="space-y-4">
                    <Label htmlFor="image-input">Upload screenshot of news article</Label>
                    <div className="border-2 border-dashed border-muted-foreground/25 rounded-lg p-6 text-center">
                      <Input
                        id="image-input"
                        type="file"
                        accept="image/*"
                        className="hidden"
                        onChange={handleFileChange}
                      />
                      <Label htmlFor="image-input" className="flex flex-col items-center justify-center cursor-pointer">
                        <Upload className="h-10 w-10 text-muted-foreground mb-2" />
                        <span className="text-sm font-medium">
                          {imageFile ? imageFile.name : "Click to upload or drag and drop"}
                        </span>
                        <span className="text-xs text-muted-foreground mt-1">PNG, JPG up to 10MB</span>
                      </Label>
                    </div>
                  </div>
                </TabsContent>
              </Tabs>

              {error && (
                <div className="mt-4 p-3 bg-destructive/10 text-destructive rounded-md flex items-center">
                  <AlertTriangle className="h-4 w-4 mr-2" />
                  {error}
                </div>
              )}
            </>
          )}
        </CardContent>
        <CardFooter className="flex justify-end">
          {result ? (
            <Button onClick={resetForm} variant="outline">
              Analyze Another
            </Button>
          ) : (
            <Button onClick={handleAnalyze} disabled={status === "loading"} className="w-full sm:w-auto">
              {status === "loading" ? (
                <>
                  <Loader2 className="mr-2 h-4 w-4 animate-spin" />
                  Analyzing...
                </>
              ) : (
                "Analyze Content"
              )}
            </Button>
          )}
        </CardFooter>
      </Card>
    </div>
  )
}

