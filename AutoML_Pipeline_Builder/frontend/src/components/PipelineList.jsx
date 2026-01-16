export default function PipelineList({ pipelines, loading, onRun, onSelect }) {
  // ✅ Guard: pipelines must be an array
  if (!Array.isArray(pipelines)) {
    return (
      <div className="card">
        <h2>📦 Pipelines</h2>
        <p className="muted">No pipelines available.</p>
      </div>
    );
  }

  return (
    <div className="card">
      <h2>📦 Pipelines</h2>

      {loading ? (
        <p className="muted">Loading pipelines...</p>
      ) : pipelines.length === 0 ? (
        <p className="muted">No pipelines created yet.</p>
      ) : null}

      <div className="column">
        {pipelines.filter(Boolean).map((p) => (
          <div key={p.id} className="card">
            <strong>Pipeline #{p.id}</strong>
            <p className="muted">Status: {p.status}</p>

            <div className="row">
              <button disabled={loading} onClick={() => onSelect(p)}>
                View
              </button>

              <button
                disabled={p.status === "running"}
                onClick={() => onRun(p.id)}
              >
                {p.status === "running" ? "Running..." : "Run"}
              </button>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
}