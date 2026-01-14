import { useState } from "react";
import axios from "axios";

export default function CreatePipeline({ onCreated }) {
  const [file, setFile] = useState(null);
  const [target, setTarget] = useState("");
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const [success, setSuccess] = useState(false);

  const API_BASE = import.meta.env.VITE_API_BASE_URL;

  const handleSubmit = async () => {
    if (!file || !target) {
      setError("Please upload a CSV file and specify a target column.");
      return;
    }

    try {
      setLoading(true);
      setError(null);
      setSuccess(false);

      // -----------------------------
      // 1. Upload dataset
      // -----------------------------
      const formData = new FormData();
      formData.append("file", file);

      const uploadRes = await axios.post(
        `${API_BASE}/upload-dataset`,
        formData,
        {
          headers: {
            "Content-Type": "multipart/form-data",
          },
        }
      );

      const datasetName = uploadRes.data.dataset_name;

      // -----------------------------
      // 2. Create pipeline
      // -----------------------------
      const pipelineRes = await axios.post(`${API_BASE}/pipeline`, {
        dataset_name: datasetName,
        target_column: target,
      });

      setSuccess(true);

      // Notify parent to refresh pipeline list
      if (onCreated) {
        onCreated(pipelineRes.data.pipeline_id);
      }

      // Reset form
      setFile(null);
      setTarget("");
    } catch (err) {
      console.error(err);
      setError("Failed to create pipeline. Please check your dataset and try again.");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="card">
      <h3>🚀 Create Pipeline</h3>

      {/* File upload */}
      <label style={{ display: "block", marginBottom: "8px" }}>
        Upload CSV dataset
      </label>
      <input
        type="file"
        accept=".csv"
        onChange={(e) => setFile(e.target.files[0])}
      />

      {/* Target column */}
      <label style={{ display: "block", marginTop: "16px", marginBottom: "8px" }}>
        Target column
      </label>
      <input
        type="text"
        placeholder="e.g. default, pass, price"
        value={target}
        onChange={(e) => setTarget(e.target.value)}
      />

      {/* Action button */}
      <button
        onClick={handleSubmit}
        disabled={loading}
        style={{ marginTop: "16px" }}
      >
        {loading ? "Creating..." : "Create Pipeline"}
      </button>

      {/* Feedback */}
      {error && (
        <p style={{ color: "#ef4444", marginTop: "12px" }}>{error}</p>
      )}
      {success && (
        <p style={{ color: "#22c55e", marginTop: "12px" }}>
          Pipeline created successfully.
        </p>
      )}
    </div>
  );
}