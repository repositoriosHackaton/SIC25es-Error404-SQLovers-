const BASE_URL = process.env.BACKEND_URL || "http://127.0.0.1:8000";

export async function analyzeNews(content: string, mode: "default" | "all" | "single", modelType?: string) {
  let endpoint = `${BASE_URL}/api/predict/v1/api/ai/default`; 

  if (mode === "all") {
    endpoint = `${BASE_URL}/api/predict/advanced/v1/ai/full-featured`;
  } else if (mode === "single" && modelType) {
    endpoint = `${BASE_URL}/api/predict/v1/api/ai/custom-type/${modelType}/`;
  }

  const response = await fetch(endpoint, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ text: content }),
  });

  if (!response.ok) {
    throw new Error("Failed to analyze news content");
  }

  return response.json();
}
