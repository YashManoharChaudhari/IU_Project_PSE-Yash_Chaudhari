import { useState } from "react";
import Header from "./components/Header";
import CreatePipeline from "./components/CreatePipeline";
import PipelineList from "./components/PipelineList";
import PipelineDetails from "./components/PipelineDetails";

export default function App() {
  const [selectedPipeline, setSelectedPipeline] = useState(null);

  return (
    <div className="app-container">
      <Header />
      <CreatePipeline onCreated={setSelectedPipeline} />
      <PipelineList
        selectedId={selectedPipeline}
        onSelect={setSelectedPipeline}
      />
      <PipelineDetails pipelineId={selectedPipeline} />
    </div>
  );
}