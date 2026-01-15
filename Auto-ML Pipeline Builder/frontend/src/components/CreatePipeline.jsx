import { useState } from "react";
import { createPipeline } from "../api";

export default function CreatePipeline({ onCreated }) {
  const [file, setFile] = useState(null);
  const [target, setTarget] = useState("");
  const [loading, setLoading] = useState(false);

  async function handleSubmit(e) {
    e.preventDefault();
    if (!file || !target) return;

    setLoading(true);
    await createPipeline(file, target);
    setLoading(false);

    setFile(null);
    setTarget("");
    onCreated();
  }

  return (
    <div className="card">
      <h2>🚀 Create Pipeline</h2>

      <form onSubmit={handleSubmit} className="form">
        <div className="form-group">
          <label>Upload CSV dataset</label>
          <input
            type="file"
            accept=".csv"
            onChange={(e) => setFile(e.target.files[0])}
          />
        </div>

        <div className="form-group">
          <label>Target column</label>
          <input
            type="text"
            placeholder="e.g. default, pass, price"
            value={target}
            onChange={(e) => setTarget(e.target.value)}
          />
        </div>

        <button className="primary-btn" disabled={loading}>
          {loading ? "Creating..." : "Create Pipeline"}
        </button>
      </form>
    </div>
  );
}