import { NewsAnalyzer } from "@/components/news-analyzer"
import { Alert, AlertDescription, AlertTitle } from "@/components/ui/alert"
import { AlertTriangle } from "lucide-react"
import { ThemeToggle } from "@/components/theme-toggle"
import { Button } from "@/components/ui/button"

export default function Home() {
  return (
    <main className="min-h-screen relative max-w-full">
      <div className="relative">
        <div className="container px-4 md:px-3 mx-auto flex flex-col justify-center min-h-screen">
            <div className="flex justify-between items-center mb-4">
            <div>
              <Button variant="link" asChild>
              <a href="https://github.com/Ezzz-Lui/SamsungInnovationCampus-FinalProject" target="_blank" rel="noopener noreferrer">
                View on GitHub
              </a>
              </Button>
            </div>
            <div className="flex items-center gap-4">
              <Button variant="ghost" asChild>
              <a href="/team" className="flex items-center gap-2">
                Our Team
              </a>
              </Button>
              <ThemeToggle />
            </div>
            </div>
          <div className="flex flex-col items-center text-center space-y-4 mb-8">
            <h1 className="text-5xl md:text-7xl font-extrabold mb-4 dark:text-transparent dark:bg-clip-text dark:bg-gradient-to-r dark:from-neutral-700 dark:via-white dark:to-neutral-700 dark:animate-text-shimmer text-center">News Verification Tool</h1>
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
        <footer className="w-full py-4">
          <div className="container mx-auto px-4 text-center">
            <p className="text-sm text-muted-foreground dark:text-neutral-400">
              &copy; {new Date().getFullYear()} News Verification Tool. All rights reserved. - A project for Samsung Innovation Campus
            </p>
          </div>
        </footer>
      </div>
    </main>
  )
}

