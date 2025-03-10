import { NewsAnalyzer } from "@/components/news-analyzer"
import { Alert, AlertDescription, AlertTitle } from "@/components/ui/alert"
import { AlertTriangle } from "lucide-react"
import { ThemeToggle } from "@/components/theme-toggle"

export default function Home() {
  return (
    <main className="min-h-screen relative">
      <div className="relative py-2">
        <div className="container px-4 md:px-6">
          <div className="flex justify-end mb-4">
            <ThemeToggle />
          </div>
          <div className="flex flex-col items-center text-center space-y-4 mb-8">
            <h1 className="text-5xl md:text-6xl font-extrabold mb-4 dark:text-transparent dark:bg-clip-text dark:bg-gradient-to-r dark:from-neutral-700 dark:via-white dark:to-neutral-700 dark:animate-text-shimmer text-center">News Verification Tool</h1>
            <p className="max-w-[700px] text-muted-foreground md:text-xl">
              Verify the authenticity of news articles by pasting text, URLs, or uploading screenshots.
            </p>
          </div>

          <Alert className="mb-8 max-w-3xl mx-auto border-yellow-500">
            <AlertTriangle className="h-4 w-4" />
            <AlertTitle>Disclaimer</AlertTitle>
            <AlertDescription>
              This tool uses artificial intelligence to analyze news content. Results may not be 100% accurate and should
              be used as a supplementary resource, not as the sole basis for determining authenticity. Always verify
              information through multiple trusted sources.
            </AlertDescription>
          </Alert>
          <NewsAnalyzer />
        </div>
      </div>
    </main>
  )
}

