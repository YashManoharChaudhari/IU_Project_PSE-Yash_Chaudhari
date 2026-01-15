import { useEffect, useState } from "react";
import { getPipeline, executePipeline } from "../api";

export default function PipelineDetails({ pipelineId }) {
  const [pipeline, setPipeline] = useState(null);

  useEffect(() => {
    let timeout;

    async function load() {
      const data = await getPipeline(pipelineId);
      setPipeline(data);

      if (data.status === "running") {
        timeout = setTimeout(load, 3000);
      }
    }

    load();
    return () => clearTimeout(timeout);
  }, [pipelineId]);

  if (!pipeline) return null;

  return (
    <div className="card">
      <h2>📊 Pipeline Details</h2>
      <p>Status: {pipeline.status}</p>
      <p>Model: {pipeline.model || "-"}</p>
      <p>Metric: {JSON.stringify(pipeline.metric)}</p>

      {pipeline.status === "created" && (
        <button onClick={() => executePipeline(pipelineId)}>
          ▶ Run Pipeline
        </button>
      )}

      {pipeline.status === "completed" && (
        <a
          href={`${import.meta.env.VITE_API_BASE_URL}/pipeline/${pipelineId}/download-script`}
          download
        >
          ⬇ Download Script
        </a>
      )}
    </div>
  );
}