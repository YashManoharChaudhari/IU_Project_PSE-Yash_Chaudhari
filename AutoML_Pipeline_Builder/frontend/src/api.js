import axios from "axios";

const API_BASE = import.meta.env.VITE_API_BASE_URL;

export async function uploadDataset(file) {
  const formData = new FormData();
  formData.append("file", file);

  const res = await axios.post(`${BASE_URL}/upload-dataset`, formData);
  return res.data; 
}

export async function createPipeline(dataset_path, target_column) {
  const res = await axios.post(`${API_BASE}/pipeline`, {
    dataset_path,
    target_column,
  });

  return res.data;
}

export async function getPipelines() {
  const res = await axios.get(`${API_BASE}/pipelines`);
  return res.data;
}

export async function getPipeline(id) {
  const res = await axios.get(`${API_BASE}/pipeline/${id}`);
  return res.data;
}

export async function executePipeline(id) {
  const res = await axios.post(`${API_BASE}/pipeline/${id}/execute`);
  return res.data;
}