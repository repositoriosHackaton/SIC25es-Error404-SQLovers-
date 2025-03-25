const BASE_URL = process.env.NEXT_PUBLIC_BACKEND_URL;
import axios from "axios";

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

export async function analyzeNewsByUrl(url: string) {
  const response = await axios.post("/api/analyze-url/", { url });
  return response.data;
}

export async function analyzeNewsByImage(imageFile: File) {
  const formData = new FormData();
  formData.append("image", imageFile);

  const response = await axios.post("/api/predict/v1/api/ai/image", formData, {
    headers: { "Content-Type": "multipart/form-data" },
  });
  return response.data;
}