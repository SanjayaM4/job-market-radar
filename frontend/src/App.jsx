import { useState } from "react";
import PostingsFeed from "./components/PostingsFeed";
import PipelineBoard from "./components/PipelineBoard";
import FunnelChart from "./components/FunnelChart";

export default function App() {
  const [tab, setTab] = useState("feed");

  return (
    <div className="min-h-screen bg-white">
      <header className="border-b p-4 flex gap-4">
        <h1 className="font-bold text-lg mr-4">Job Market Radar</h1>
        <button onClick={() => setTab("feed")} className={tab === "feed" ? "font-semibold" : "text-gray-500"}>
          Feed
        </button>
        <button onClick={() => setTab("pipeline")} className={tab === "pipeline" ? "font-semibold" : "text-gray-500"}>
          Pipeline
        </button>
        <button onClick={() => setTab("stats")} className={tab === "stats" ? "font-semibold" : "text-gray-500"}>
          Stats
        </button>
      </header>

      {tab === "feed" && <PostingsFeed />}
      {tab === "pipeline" && <PipelineBoard />}
      {tab === "stats" && <FunnelChart />}
    </div>
  );
}
