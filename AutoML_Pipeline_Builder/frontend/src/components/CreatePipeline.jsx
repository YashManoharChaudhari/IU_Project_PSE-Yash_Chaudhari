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
      const pipeline = await createPipeline(upload.dataset_path, target);

      alert("Pipeline created successfully!");

      // ✅ reset UI state
      setFile(null);
      setTarget("");

      // ✅ refresh pipelines (important: await so state updates correctly)
      if (onCreated) {
        await onCreated();
      }
    } catch (err) {
      console.error("Pipeline creation failed:", err);
      alert(
        err?.response?.data?.detail ||
        err.message ||
        "Pipeline creation failed"
      );
    } finally {
      // ✅ ALWAYS reset loading
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
          onChange={(e) => setFile(e.target.files[0])}
          disabled={loading}
        />

        <input
          type="text"
          placeholder="Target column (e.g. label)"
          value={target}
          onChange={(e) => setTarget(e.target.value)}
          disabled={loading}
        />

        <button
          type="submit"
          disabled={loading}
          className="primary-btn"
        >
  {loading ? "Creating..." : "Create Pipeline"}
</button>
      </form>
    </div>
  );
}