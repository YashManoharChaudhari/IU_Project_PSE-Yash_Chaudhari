import { useEffect, useState } from "react";
import { getPipelines } from "../api";

export default function PipelineList({ onSelect }) {
  const [pipelines, setPipelines] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    async function load() {
      try {
        const data = await getPipelines();
        setPipelines(data || []);
      } finally {
        setLoading(false);
      }
    }
    load();
  }, []);

  return (
    <div className="card">
      <h2>📦 Pipelines</h2>

      {loading && <p>Loading pipelines...</p>}

      {!loading && pipelines.length === 0 && (
        <p>No pipelines created yet.</p>
      )}

      <ul>
        {pipelines.map(p => (
          <li key={p.id} onClick={() => onSelect(p)}>
            Pipeline #{p.id} — {p.status}
          </li>
        ))}
      </ul>
    </div>
  );
}