import axios from "axios";

// Setup axios instance pointing to FastAPI
const apiClient = axios.create({
  baseURL: import.meta.env.VITE_API_BASE_URL || "/api",
  headers: {
    "Content-Type": "application/json",
  },
});

export const getLiveNews = async (query = "technology AI jobs") => {
  const response = await apiClient.get("/news/live", { params: { query } });
  return response.data.articles || [];
};

export const analyzeProfile = async (formData: FormData) => {
  // Use multipart/form-data for file upload
  const response = await axios.post((import.meta.env.VITE_API_BASE_URL || "/api") + "/orchestrator/analyze", formData, {
    headers: {
      "Content-Type": "multipart/form-data",
    },
  });
  return response.data;
};
