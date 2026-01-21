import axios from "axios";

/**
 * Base URL for the deployed backend.
 * IMPORTANT: Do not use localhost in production.
 */
const API_BASE_URL = "https://automlpipelinebuilder.onrender.com";

const API = axios.create({
  baseURL: API_BASE_URL,
});

/**
 * Upload a CSV dataset
 */
export const uploadDataset = async (file) => {
  const form = new FormData();
  form.append("file", file);

  const res = await API.post("/upload-dataset", form, {
    headers: {
      "Content-Type": "multipart/form-data",
    },
  });

  return res.data;
};

/**
 * Create a new ML pipeline
 */
export const createPipeline = async (datasetPath, target) => {
  const res = await API.post("/pipeline", {
    dataset_path: datasetPath,
    target_column: target,
  });
  return res.data;
};

/**
 * Fetch list of created pipelines
 */
export const listPipelines = async () => {
  const res = await API.get("/pipelines");
  return res.data;
};

/**
 * Execute an existing pipeline
 */
export const runPipeline = async (id) => {
  const res = await API.post(`/pipeline/${id}/execute`);
  return res.data;
};

/**
 * Download generated Python pipeline file
 * Uses direct browser download (no fetch/axios)
 */
export const downloadPipelinePy = (pipelineId) => {
  const downloadUrl = `${API_BASE_URL}/pipeline/${pipelineId}/download`;
  window.location.href = downloadUrl;
};

export default API;