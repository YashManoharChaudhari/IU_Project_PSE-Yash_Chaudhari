export default function PipelineDetails({ pipeline }) {
  if (!pipeline) {
    return (
      <div className="card">
        <p className="muted">Select a pipeline to see details.</p>
      </div>
    );
  }

  const handleDownload = async () => {
    try {
      const response = await fetch(
        `${API_BASE}/pipeline/${pipeline.id}/download`
      );

      if (!response.ok) {
        throw new Error("Download failed");
      }

      const contentType = response.headers.get("content-type") || "";
      if (!contentType.includes("python")) {
        throw new Error("Invalid file type received");
      }

      const blob = await response.blob();
      const url = window.URL.createObjectURL(blob);

      const a = document.createElement("a");
      a.href = url;
      a.download = `pipeline_${pipeline.id}.py`;
      document.body.appendChild(a);
      a.click();
      
      window.URL.revokeObjectURL(url);
    } catch (err) {
      alert("Failed to download ML pipeline. Please try again.");
    }
  };

  return (
    <div className="card">
      <h3>📊 Pipeline Details</h3>

      <button
        className="primary-btn"
        onClick={handleDownload}
        disabled={pipeline.status !== "completed"}
      >
        ⬇️ Download ML Pipeline (.py)
      </button>

      <p className="muted" style={{ marginTop: "6px" }}>
        Includes preprocessing, training, evaluation, and model selection logic.
      </p>

      <p><strong>ID:</strong> {pipeline.id}</p>
      <p><strong>Status:</strong> {pipeline.status}</p>
      <p><strong>Dataset:</strong> {pipeline.dataset_path}</p>
      <p><strong>Target:</strong> {pipeline.target_column}</p>
      <p><strong>Model:</strong> {pipeline.model}</p>

      {pipeline.metric !== null && (
        <p>
          <strong>
            {pipeline.problem_type === "classification"
              ? "Accuracy"
              : "R² Score"}
            :
          </strong>{" "}
          {pipeline.problem_type === "classification"
            ? `${(pipeline.metric * 100).toFixed(2)}%`
            : pipeline.metric.toFixed(3)}
        </p>
      )}
    </div>
  );
}