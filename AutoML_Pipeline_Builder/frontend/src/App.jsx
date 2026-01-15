import { useState } from "react";
import Header from "./components/Header";
import CreatePipeline from "./components/CreatePipeline";
import PipelineList from "./components/PipelineList";
import PipelineDetails from "./components/PipelineDetails";

export default function App() {
  const [selectedPipeline, setSelectedPipeline] = useState(null);
  const [refreshKey, setRefreshKey] = useState(0);

  return (
    <div className="app">
      <Header />

      <div className="container">
        <CreatePipeline onCreated={() => setRefreshKey(k => k + 1)} />

        <PipelineList
          key={refreshKey}
          onSelect={setSelectedPipeline}
        />

        {selectedPipeline && (
          <PipelineDetails pipelineId={selectedPipeline.id} />
        )}
      </div>
    </div>
  );
}