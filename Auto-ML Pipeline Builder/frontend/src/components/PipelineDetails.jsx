import { useEffect, useState } from "react";
import { getPipeline, runPipeline } from "../api";

export default function PipelineDetails({ pipelineId }) {
  const [pipeline, setPipeline] = useState(null);

  useEffect(() => {
    if (!pipelineId) return;

    const load = async () => {
      const res = await getPipeline(pipelineId);
      setPipeline(res.data);
    };

    load();
    const interval = setInterval(load, 2000);
    return () => clearInterval(interval);
  }, [pipelineId]);

  if (!pipelineId) {
    return (
      <div className="card empty">
        <h2>🚀 AutoML Results</h2>
        <p>Select a pipeline to see details.</p>
      </div>
    );
  }

  if (!pipeline) {
    return <div className="card">Loading...</div>;
  }

  const statusColor = {
    created: "#9CA3AF",
    running: "#F59E0B",
    completed: "#10B981",
    failed: "#EF4444",
  }[pipeline.status];

  return (
    <div className="card bold-card">
      <div className="header-row">
        <h2>Pipeline #{pipelineId}</h2>
        <span
          className="status-pill"
          style={{ backgroundColor: statusColor }}
        >
          {pipeline.status.toUpperCase()}
        </span>
      </div>

      {pipeline.task_type && (
        <p className="muted">
          Task type: <strong>{pipeline.task_type}</strong>
        </p>
      )}

      {pipeline.status === "running" && (
        <div className="thinking">
          ⏳ Training multiple models and selecting the best one…
        </div>
      )}

      {pipeline.model_name && (
        <div className="result-card">
          <h3>Best Model</h3>
          <p className="big-text">{pipeline.model_name}</p>
        </div>
      )}

      {pipeline.metric !== null && pipeline.metric_name && (
        <div className="metric-card">
          <h3>
            {pipeline.metric_name === "accuracy" ? "Accuracy" : "RMSE"}
          </h3>
          <p className="metric-value">{pipeline.metric}</p>
        </div>
      )}

      {pipeline.status === "created" && (
        <button className="primary-btn" onClick={() => runPipeline(pipelineId)}>
          ▶ Run Pipeline
        </button>
      )}

      {pipeline.artifacts && (
        <div className="download-row">
          <a href={pipeline.artifacts.model} className="link-btn" download>
            ⬇ Download Model Info
          </a>
          <a href={pipeline.artifacts.script} className="link-btn" download>
            ⬇ Download Pipeline Script
          </a>
        </div>
      )}
    </div>
  );
}