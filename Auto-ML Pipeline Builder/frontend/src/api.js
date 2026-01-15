import axios from "axios";

const API_BASE = import.meta.env.VITE_API_BASE_URL;

export async function uploadDataset(file) {
  const formData = new FormData();
  formData.append("file", file);

  const response = await axios.post(
    `${API_BASE}/upload-dataset`,
    formData,
    {
      headers: {
        "Content-Type": "multipart/form-data",
      },
    }
  );

  return response.data; 
}

export async function createPipeline(datasetName, target) {
  const response = await axios.post(
    `${API_BASE}/pipeline`,
    {
      dataset_name: datasetName,
      target: target,
    },
    {
      headers: {
        "Content-Type": "application/json",
      },
    }
  );

  return response.data;
}

export async function getPipelines() {
  const response = await axios.get(`${API_BASE}/pipelines`);
  return response.data;
}

export async function getPipeline(pipelineId) {
  const response = await axios.get(`${API_BASE}/pipeline/${pipelineId}`);
  return response.data;
}

export async function executePipeline(pipelineId) {
  const response = await axios.post(
    `${API_BASE}/pipeline/${pipelineId}/execute`
  );
  return response.data;
}