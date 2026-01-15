import { useState } from "react";
import { uploadDataset, createPipeline } from "../api";

export default function CreatePipeline({ onCreated }) {
  const [file, setFile] = useState(null);
  const [target, setTarget] = useState("");
  const [loading, setLoading] = useState(false);

  async function handleSubmit(e) {
    e.preventDefault();

    if (!file || !target) {
      alert("Upload a CSV file and enter target column");
      return;
    }

    setLoading(true);
    try {
      const upload = await uploadDataset(file);
      await createPipeline(upload.dataset_path, target);

      setFile(null);
      setTarget("");
      onCreated();
    } catch (err) {
      console.error(err);
      alert("Pipeline creation failed");
    } finally {
      setLoading(false);
    }
  }

  return (
    <div className="card">
      <h2>🚀 Create Pipeline</h2>

      <form onSubmit={handleSubmit} className="form">
        <input
          type="file"
          accept=".csv"
          onChange={e => setFile(e.target.files[0])}
        />

        <input
          type="text"
          placeholder="Target column (e.g. label)"
          value={target}
          onChange={e => setTarget(e.target.value)}
        />

        <button type="submit" disabled={loading}>
          {loading ? "Creating..." : "Create Pipeline"}
        </button>
      </form>
    </div>
  );
}