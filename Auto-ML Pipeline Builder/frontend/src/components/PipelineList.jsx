import { useEffect, useState } from "react";
import { listPipelines, getPipeline } from "../api";

export default function PipelineList({ selectedId, onSelect }) {
  const [pipelines, setPipelines] = useState([]);

  useEffect(() => {
    const load = async () => {
      const res = await listPipelines();
      setPipelines(res.data);
    };

    load();
    const interval = setInterval(load, 3000);
    return () => clearInterval(interval);
  }, []);

  const statusColor = {
    created: "#9CA3AF",
    running: "#F59E0B",
    completed: "#10B981",
    failed: "#EF4444",
  };

  if (pipelines.length === 0) {
    return (
      <div className="card empty">
        <h3>📦 Pipelines</h3>
        <p>Create your first pipeline to begin automated ML.</p>
      </div>
    );
  }

  return (
    <div className="card">
      <h3 style={{ marginBottom: "16px" }}>📦 Pipelines</h3>

      <div className="pipeline-list">
        {pipelines.map((p) => (
          <div
            key={p.pipeline_id}
            className={`pipeline-item ${
              selectedId === p.pipeline_id ? "selected" : ""
            }`}
            onClick={() => onSelect(p.pipeline_id)}
          >
            <div className="pipeline-left">
              <strong>Pipeline #{p.pipeline_id}</strong>
              <span
                className="status-pill"
                style={{ backgroundColor: statusColor[p.status] }}
              >
                {p.status.toUpperCase()}
              </span>
            </div>

            <div className="pipeline-right">
              {p.status === "completed" && (
                <span className="done">✔ Ready</span>
              )}
              {p.status === "running" && <span className="run">⏳ Running</span>}
              {p.status === "failed" && <span className="fail">✖ Failed</span>}
            </div>
          </div>
        ))}
      </div>
    </div>
  );
}