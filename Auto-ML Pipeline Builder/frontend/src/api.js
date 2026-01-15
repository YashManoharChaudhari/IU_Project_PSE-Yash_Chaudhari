import axios from "axios";

const API = axios.create({
  baseURL: import.meta.env.VITE_API_BASE_URL,
});

export const createPipeline = (config) => API.post("/pipeline", config);
export const listPipelines = () => API.get("/pipelines");
export const getPipeline = (id) => API.get(`/pipeline/${id}`);
export const runPipeline = (id) => API.post(`/pipeline/${id}/execute`);

export async function createPipeline(file, target) {
  const formData = new FormData();
  formData.append("file", file);
  formData.append("target", target);

  const res = await fetch(`${API_BASE}/pipeline`, {
    method: "POST",
    body: formData,
  });

  if (!res.ok) {
    throw new Error("Pipeline creation failed");
  }

  return res.json();
}