import { useEffect, useState } from "react";
import { getPipelines } from "../api";

export default function PipelineList({ onSelect }) {
  const [pipelines, setPipelines] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    async function fetchPipelines() {
      try {
        const data = await getPipelines();
        setPipelines(data || []);
      } catch (err) {
        setError("Failed to load pipelines");
      } finally {
        setLoading(false);
      }
    }

    fetchPipelines();
  }, []);

  return (
    <div className="card">
      <h2>📦 Pipelines</h2>

      {loading && <p>Loading pipelines…</p>}

      {!loading && pipelines.length === 0 && (
        <p className="muted">No pipelines created yet.</p>
      )}

      {!loading && pipelines.length > 0 && (
        <ul className="pipeline-list">
          {pipelines.map((p) => (
            <li key={p.id} onClick={() => onSelect(p)}>
              {p.name}
            </li>
          ))}
        </ul>
      )}

      {error && <p className="error">{error}</p>}
    </div>
  );
}