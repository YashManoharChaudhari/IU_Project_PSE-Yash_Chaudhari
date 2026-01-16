import { useEffect, useState } from "react";
import { listPipelines, runPipeline } from "./api";
import CreatePipeline from "./components/CreatePipeline";
import PipelineList from "./components/PipelineList";
import PipelineDetails from "./components/PipelineDetails";

export default function App() {
  const [pipelines, setPipelines] = useState([]);
  const [selected, setSelected] = useState(null);
  const [loading, setLoading] = useState(true);

  async function load() {
    try {
      setLoading(true);
      const data = await listPipelines();
      setPipelines(Array.isArray(data) ? data : []);
    } catch (err) {
      console.error("Failed to load pipelines", err);
      setPipelines([]);
    } finally {
      setLoading(false);
    }
    const data = await listPipelines();
console.log("PIPELINES RESPONSE:", data, Array.isArray(data));
setPipelines(Array.isArray(data) ? data : []);
  }

  useEffect(() => {
    load();
  }, []);

  return (
    <div className="container">
      <h1>Auto-ML Pipeline Builder</h1>

      <CreatePipeline onCreated={load} />

      <PipelineList
        pipelines={pipelines}
        loading={loading}
        onSelect={setSelected}
        onRun={async id => {
          const updated = await runPipeline(id);
          setSelected(updated);
          load();
        }}
      />

      <PipelineDetails pipeline={selected} />
    </div>
  );
}