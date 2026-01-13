import { useState } from "react";
import { createPipeline } from "../api";

export default function CreatePipeline({ onCreated }) {
  const [dataset, setDataset] = useState("");
  const [target, setTarget] = useState("");
  const [loading, setLoading] = useState(false);

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (!dataset || !target) return;

    setLoading(true);
    const res = await createPipeline({
      dataset_path: dataset,
      target_column: target,
    });
    setLoading(false);

    setDataset("");
    setTarget("");
    onCreated(res.data.pipeline_id);
  };

  return (
    <div className="card bold-card">
      <h2>⚙️ Create AutoML Pipeline</h2>
      <p className="muted">
        Provide a dataset and target column. The system will automatically
        detect the task type and select the best model.
      </p>

      <form onSubmit={handleSubmit} className="form">
        <div className="form-group">
          <label>Dataset name</label>
          <input
            type="text"
            placeholder="e.g. student_performance.csv"
            value={dataset}
            onChange={(e) => setDataset(e.target.value)}
          />
        </div>

        <div className="form-group">
          <label>Target column</label>
          <input
            type="text"
            placeholder="e.g. pass"
            value={target}
            onChange={(e) => setTarget(e.target.value)}
          />
        </div>

        <button type="submit" className="primary-btn" disabled={loading}>
          {loading ? "⏳ Creating pipeline..." : "🚀 Create Pipeline"}
        </button>
      </form>
    </div>
  );
}
