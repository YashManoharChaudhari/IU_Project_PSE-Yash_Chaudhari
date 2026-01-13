import { useState } from "react";
import Header from "./components/Header";

import PipelineList from "./components/PipelineList";
import PipelineDetails from "./components/PipelineDetails";

function App() {
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

export default App;
