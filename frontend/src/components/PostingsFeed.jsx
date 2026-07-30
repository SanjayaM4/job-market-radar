import { useEffect, useState } from "react";
import { fetchPostings, createApplication } from "../api";

export default function PostingsFeed() {
  const [postings, setPostings] = useState([]);
  const [minScore, setMinScore] = useState(0.5);
  const [loading, setLoading] = useState(true);
  const [trackedIds, setTrackedIds] = useState(new Set());

  useEffect(() => {
    setLoading(true);
    fetchPostings(minScore)
      .then(setPostings)
      .finally(() => setLoading(false));
  }, [minScore]);

  async function handleTrack(postingId) {
    try {
      await createApplication(postingId);
      setTrackedIds((prev) => new Set(prev).add(postingId));
    } catch (err) {
      alert("Could not track this posting - it may already be tracked.");
    }
  }

  return (
    <div className="p-4">
      <div className="flex items-center gap-2 mb-4">
        <label className="text-sm text-gray-600">Minimum match score:</label>
        <input
          type="range"
          min="0"
          max="1"
          step="0.05"
          value={minScore}
          onChange={(e) => setMinScore(parseFloat(e.target.value))}
        />
        <span className="text-sm font-mono">{minScore.toFixed(2)}</span>
      </div>

      {loading ? (
        <p className="text-gray-500">Loading postings...</p>
      ) : (
        <div className="space-y-3">
          {postings.map((posting) => (
            <div key={posting.id} className="border rounded-lg p-4 flex justify-between items-start">
              <div>
                <h3 className="font-semibold">{posting.title}</h3>
                <p className="text-sm text-gray-600">
                  {posting.company} · {posting.location} · {posting.source}
                </p>
                <a
                  href={posting.url}
                  target="_blank"
                  rel="noreferrer"
                  className="text-blue-600 text-sm hover:underline"
                >
                  View posting
                </a>
              </div>
              <div className="text-right">
                <div className="text-sm font-mono mb-2">
                  {posting.match_score != null ? posting.match_score.toFixed(2) : "—"}
                </div>
                <button
                  onClick={() => handleTrack(posting.id)}
                  disabled={trackedIds.has(posting.id)}
                  className="text-xs px-3 py-1 rounded bg-blue-600 text-white disabled:bg-gray-300"
                >
                  {trackedIds.has(posting.id) ? "Tracked" : "Track"}
                </button>
              </div>
            </div>
          ))}
        </div>
      )}
    </div>
  );
}
