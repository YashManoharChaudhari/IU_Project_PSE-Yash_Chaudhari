import { useState } from "react";
import { uploadDataset, createPipeline } from "../api";

export default function CreatePipeline({ onCreated }) {
  const [file, setFile] = useState(null);
  const [target, setTarget] = useState("");
  const [loading, setLoading] = useState(false);

  async function handleSubmit(e) {
    e.preventDefault();

    if (!file || !target) {
      alert("Please upload a CSV file and enter a target column.");
      return;
    }

    setLoading(true);

    try {
      // Step 1: Upload dataset
      const uploadResult = await uploadDataset(file);

      // Step 2: Create pipeline
      await createPipeline(uploadResult.dataset_name, target);

      // Reset form
      setFile(null);
      setTarget("");

      // Refresh pipelines list
      onCreated();
    } catch (err) {
      console.error(err);
      alert(
        "Failed to create pipeline. Backend may be waking up, please try again."
      );
    } finally {
      setLoading(false);
    }
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
            placeholder="e.g. label, default, price"
            value={target}
            onChange={(e) => setTarget(e.target.value)}
          />
        </div>

        <button className="primary-btn" disabled={loading}>
          {loading ? "Creating pipeline..." : "Create Pipeline"}
        </button>
      </form>
    </div>
  );
}