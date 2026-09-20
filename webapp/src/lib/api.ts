import axios from "axios";

// Backend deployed on Render
const API_BASE = import.meta.env.VITE_API_BASE_URL || "https://margdarshak-api-1j94.onrender.com/api";

// Setup axios instance pointing to FastAPI
const apiClient = axios.create({
  baseURL: API_BASE,
  headers: {
    "Content-Type": "application/json",
  },
});

export const getLiveNews = async (query = "technology AI jobs India") => {
  const response = await apiClient.get("/news/live", { params: { query } });
  return response.data.articles || [];
};

export const analyzeProfile = async (formData: FormData) => {
  // Use multipart/form-data for file upload
  const response = await axios.post(API_BASE + "/orchestrator/analyze", formData, {
    headers: {
      "Content-Type": "multipart/form-data",
    },
    timeout: 120000, // 2 min timeout for AI analysis
  });
  return response.data;
};
