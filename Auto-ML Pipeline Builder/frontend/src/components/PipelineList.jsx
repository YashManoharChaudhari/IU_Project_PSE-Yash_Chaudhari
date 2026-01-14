import { useEffect, useState } from "react";
import { listPipelines } from "../api";

export default function PipelineList({ selectedId, onSelect }) {
  const [pipelines, setPipelines] = useState([]);
  const [error, setError] = useState(null);

  useEffect(() => {
    const loadPipelines = async () => {
      try {
        const res = await listPipelines();
        setPipelines(Array.isArray(res.data) ? res.data : []);
      } catch (err) {
        console.error("Failed to load pipelines", err);
        setError("Failed to load pipelines");
      }
    };

    loadPipelines();
  }, []);

  if (error) {
    return (
      <div className="card">
        <h3>📦 Pipelines</h3>
        <p style={{ color: "#ef4444" }}>{error}</p>
      </div>
    );
  }

  return (
    <div className="card">
      <h3>📦 Pipelines</h3>

      {pipelines.length === 0 ? (
        <p>No pipelines created yet.</p>
      ) : (
        <ul className="pipeline-list">
          {pipelines.map((p) => (
            <li
              key={p.pipeline_id}
              onClick={() => onSelect(p.pipeline_id)}
              className={
                selectedId === p.pipeline_id ? "selected pipeline-item" : "pipeline-item"
              }
            >
              <strong>Pipeline #{p.pipeline_id}</strong>
              <span style={{ marginLeft: "8px", opacity: 0.7 }}>
                ({p.status})
              </span>
            </li>
          ))}
        </ul>
      )}
    </div>
  );
}