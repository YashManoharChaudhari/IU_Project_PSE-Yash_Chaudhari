import axios from "axios";

const API = axios.create({
  baseURL: "http://localhost:8000",
});

export const createPipeline = (config) =>
  API.post("/pipeline", config);

export const listPipelines = () =>
  API.get("/pipelines");

export const getPipeline = (id) =>
  API.get(`/pipeline/${id}`);

export const runPipeline = (id) =>
  API.post(`/pipeline/${id}/execute`);