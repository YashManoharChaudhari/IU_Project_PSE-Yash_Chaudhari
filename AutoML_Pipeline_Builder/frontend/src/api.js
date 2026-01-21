import axios from "axios";


const API = axios.create({
  baseURL: "https://automlpipelinebuilder.onrender.com",
});

export const uploadDataset = async (file) => {
  const form = new FormData();
  form.append("file", file);
  const res = await API.post("/upload-dataset", form);
  return res.data;
};

export const createPipeline = async (datasetPath, target) => {
  const res = await API.post("/pipeline", {
    dataset_path: datasetPath,
    target_column: target,
  });
  return res.data;
};

export const listPipelines = async () => {
  const res = await API.get("/pipelines");
  return res.data;
};

export const runPipeline = async (id) => {
  const res = await API.post(`/pipeline/${id}/execute`);
  return res.data;
};

export const downloadPipelinePy = (pipelineId) => {
  const baseUrl =
    import.meta.env.VITE_API_URL || "http://127.0.0.1:8000";

  window.open(
    `${baseUrl}/pipeline/${pipelineId}/download-py`,
    "_blank"
  );
};

export default API;