import { useEffect, useState } from "react";
import { listPipelines } from "../api";

export default function PipelineList({ selectedId, onSelect }) {
  const [pipelines, setPipelines] = useState([]);
  const [error, setError] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    let attempts = 0;

    const loadPipelines = async () => {
      try {
        const res = await listPipelines();
        setPipelines(Array.isArray(res.data) ? res.data : []);
        setError(null);
      } catch (err) {
        attempts += 1;

        if (attempts < 3) {
          setTimeout(loadPipelines, 1500); // retry after 1.5s
        } else {
          setError("Backend waking up. Please refresh once.");
        }
      } finally {
        setLoading(false);
      }
    };

    loadPipelines();
  }, []);

  if (loading) {
    return (
      <div className="card">
        <h3>📦 Pipelines</h3>
        <p>Loading pipelines…</p>
      </div>
    );
  }

  if (error) {
    return (
      <div className="card">
        <h3>📦 Pipelines</h3>
        <p style={{ color: "#facc15" }}>{error}</p>
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
                selectedId === p.pipeline_id
                  ? "selected pipeline-item"
                  : "pipeline-item"
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