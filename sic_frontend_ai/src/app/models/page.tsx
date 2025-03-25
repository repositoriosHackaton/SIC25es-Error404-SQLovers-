import Link from "next/link"
import { ArrowLeft, Info } from "lucide-react"
import { Button } from "@/components/ui/button"
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card"
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs"
import { Alert, AlertDescription, AlertTitle } from "@/components/ui/alert"
import { ModelCard } from "@/components/model-card"
import { ModelComparison } from "@/components/model-comparison"
import { ThemeToggle } from "@/components/theme-toggle"

export default function ModelsPage() {
  return (
    <main className="bg-gradient-to-b from-background to-muted/50 py-12">
      <div className="container mx-auto px-4 md:px-6 w-max-auto">
        <div className="flex justify-between items-center mb-8">
          <Link href="/">
            <Button variant="outline" size="sm">
              <ArrowLeft className="mr-2 h-4 w-4" />
              Back to Verification Tool
            </Button>
          </Link>
          <ThemeToggle />
        </div>

        <div className="flex flex-col items-center text-center space-y-4 mb-8">
          <h1 className="text-3xl font-bold tracking-tighter sm:text-4xl md:text-5xl">AI Models Dashboard</h1>
          <p className="max-w-[700px] text-muted-foreground md:text-xl">
            Transparency and performance metrics for the AI models powering our news verification tool.
          </p>
        </div>

        <Alert className="mb-8">
          <Info className="h-4 w-4" />
          <AlertTitle>Model Ensemble Approach</AlertTitle>
          <AlertDescription>
            Our news verification system uses an ensemble of multiple models to achieve higher accuracy and reduce bias.
            Each model contributes differently based on the type of content being analyzed.
          </AlertDescription>
        </Alert>

        <div className="grid gap-6 md:grid-cols-2 lg:grid-cols-3 mb-8">
          <Card>
            <CardHeader className="pb-2">
              <CardTitle>Overall Accuracy</CardTitle>
              <CardDescription>Combined model performance</CardDescription>
            </CardHeader>
            <CardContent>
              <div className="text-4xl font-bold">87.6%</div>
              <p className="text-sm text-muted-foreground mt-2">
                Based on our evaluation dataset of 10,000 news articles
              </p>
            </CardContent>
          </Card>
          <Card>
            <CardHeader className="pb-2">
              <CardTitle>False Positive Rate</CardTitle>
              <CardDescription>Legitimate news marked as misleading</CardDescription>
            </CardHeader>
            <CardContent>
              <div className="text-4xl font-bold">3.2%</div>
              <p className="text-sm text-muted-foreground mt-2">We prioritize minimizing false accusations</p>
            </CardContent>
          </Card>
          <Card>
            <CardHeader className="pb-2">
              <CardTitle>Detection Rate</CardTitle>
              <CardDescription>Misleading content correctly identified</CardDescription>
            </CardHeader>
            <CardContent>
              <div className="text-4xl font-bold">91.4%</div>
              <p className="text-sm text-muted-foreground mt-2">Across various types of misleading content</p>
            </CardContent>
          </Card>
        </div>

        <ModelComparison />

        <Tabs defaultValue="naive-bayes" className="mt-12">
          <TabsList className="grid w-full grid-cols-2 md:grid-cols-5">
            <TabsTrigger value="naive-bayes">Naive Bayes</TabsTrigger>
            <TabsTrigger value="neural-network">Neural Network</TabsTrigger>
            <TabsTrigger value="random-forest">Random Forest</TabsTrigger>
            <TabsTrigger value="xgboost">XGBoost</TabsTrigger>
            <TabsTrigger value="logistic">Logistic</TabsTrigger>
          </TabsList>

          <TabsContent value="naive-bayes">
            <ModelCard
              name="Naive Bayes"
              description="A probabilistic classifier based on applying Bayes' theorem with strong independence assumptions between features."
              accuracy={84.2}
              precision={82.7}
              recall={87.5}
              f1Score={85.0}
              strengths={[
                "Fast training and prediction",
                "Works well with high-dimensional data",
                "Performs well with text classification tasks",
                "Requires less training data",
              ]}
              weaknesses={[
                "Assumes feature independence (often not true)",
                "Less accurate with numerical features",
                "Can be outperformed by more complex models",
              ]}
              useCases={["Initial text classification", "Spam detection", "Sentiment analysis"]}
              featureImportance={[
                { feature: "Sensationalist language", importance: 0.28 },
                { feature: "Source credibility", importance: 0.22 },
                { feature: "Citation presence", importance: 0.18 },
                { feature: "Emotional tone", importance: 0.15 },
                { feature: "Publication context", importance: 0.12 },
                { feature: "Other factors", importance: 0.05 },
              ]}
            />
          </TabsContent>

          <TabsContent value="neural-network">
            <ModelCard
              name="Neural Network"
              description="A deep learning model with multiple layers that can capture complex patterns in text and metadata."
              accuracy={89.3}
              precision={88.1}
              recall={90.2}
              f1Score={89.1}
              strengths={[
                "Captures complex non-linear relationships",
                "Learns hierarchical feature representations",
                "Adaptable to various data types",
                "High performance ceiling with sufficient data",
              ]}
              weaknesses={[
                "Requires large amounts of training data",
                "Computationally intensive",
                "Risk of overfitting",
                "Less interpretable ('black box')",
              ]}
              useCases={[
                "Complex pattern recognition",
                "Multi-modal analysis (text + images)",
                "Contextual understanding",
              ]}
              featureImportance={[
                { feature: "Contextual inconsistencies", importance: 0.25 },
                { feature: "Source reputation", importance: 0.22 },
                { feature: "Claim verification", importance: 0.2 },
                { feature: "Writing style", importance: 0.15 },
                { feature: "Topic relevance", importance: 0.1 },
                { feature: "Other factors", importance: 0.08 },
              ]}
            />
          </TabsContent>

          <TabsContent value="random-forest">
            <ModelCard
              name="Random Forest"
              description="An ensemble learning method that operates by constructing multiple decision trees during training."
              accuracy={86.7}
              precision={85.9}
              recall={87.3}
              f1Score={86.6}
              strengths={[
                "Resistant to overfitting",
                "Handles large feature sets well",
                "Provides feature importance metrics",
                "Works well with both categorical and numerical data",
              ]}
              weaknesses={[
                "Less effective with very high-dimensional sparse data",
                "Can be computationally intensive",
                "Less interpretable than simple decision trees",
              ]}
              useCases={[
                "Balanced performance across news types",
                "Feature importance analysis",
                "Handling mixed data types",
              ]}
              featureImportance={[
                { feature: "Source credibility", importance: 0.24 },
                { feature: "Fact consistency", importance: 0.21 },
                { feature: "Citation quality", importance: 0.19 },
                { feature: "Language patterns", importance: 0.16 },
                { feature: "Publication history", importance: 0.12 },
                { feature: "Other factors", importance: 0.08 },
              ]}
            />
          </TabsContent>

          <TabsContent value="xgboost">
            <ModelCard
              name="XGBoost"
              description="An optimized gradient boosting library designed to be highly efficient, flexible and portable."
              accuracy={90.1}
              precision={89.7}
              recall={90.5}
              f1Score={90.1}
              strengths={[
                "High performance and accuracy",
                "Handles missing data well",
                "Built-in regularization",
                "Efficient implementation",
              ]}
              weaknesses={[
                "Can overfit with noisy data",
                "Requires careful tuning",
                "Less interpretable than simpler models",
              ]}
              useCases={[
                "High-stakes verification",
                "Complex feature interaction analysis",
                "When maximum accuracy is required",
              ]}
              featureImportance={[
                { feature: "Factual consistency", importance: 0.26 },
                { feature: "Source reliability", importance: 0.23 },
                { feature: "Evidence quality", importance: 0.2 },
                { feature: "Narrative bias", importance: 0.14 },
                { feature: "Historical accuracy", importance: 0.1 },
                { feature: "Other factors", importance: 0.07 },
              ]}
            />
          </TabsContent>

          <TabsContent value="logistic">
            <ModelCard
              name="Logistic Regression"
              description="A statistical model that uses a logistic function to model a binary dependent variable."
              accuracy={82.5}
              precision={81.3}
              recall={84.2}
              f1Score={82.7}
              strengths={[
                "Highly interpretable",
                "Efficient training",
                "Works well with linearly separable data",
                "Provides probability outputs",
              ]}
              weaknesses={[
                "Limited to linear decision boundaries",
                "May underperform with complex relationships",
                "Sensitive to outliers",
              ]}
              useCases={["Baseline model", "When interpretability is critical", "Initial feature selection"]}
              featureImportance={[
                { feature: "Known false claims", importance: 0.3 },
                { feature: "Source credibility", importance: 0.25 },
                { feature: "Citation presence", importance: 0.2 },
                { feature: "Emotional language", importance: 0.15 },
                { feature: "Publication context", importance: 0.07 },
                { feature: "Other factors", importance: 0.03 },
              ]}
            />
          </TabsContent>
        </Tabs>
      </div>
    </main>
  )
}

