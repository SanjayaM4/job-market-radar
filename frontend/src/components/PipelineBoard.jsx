import { useEffect, useState } from "react";
import { fetchApplications, updateApplicationStatus, deleteApplication } from "../api";

const STATUSES = ["saved", "applied", "interview", "offer", "rejected"];

export default function PipelineBoard() {
  const [applications, setApplications] = useState([]);
  const [loading, setLoading] = useState(true);

  function loadApplications() {
    setLoading(true);
    fetchApplications()
      .then(setApplications)
      .finally(() => setLoading(false));
  }

  useEffect(() => {
    loadApplications();
  }, []);

  async function handleStatusChange(applicationId, newStatus) {
    await updateApplicationStatus(applicationId, newStatus);
    loadApplications();
  }

  async function handleRemove(applicationId, title) {
    if (!window.confirm(`Remove "${title}" from your pipeline?`)) return;
    await deleteApplication(applicationId);
    loadApplications();
  }

  if (loading) return <p className="p-4 text-gray-500">Loading pipeline...</p>;

  return (
    <div className="p-4 grid grid-cols-1 md:grid-cols-5 gap-3">
      {STATUSES.map((status) => (
        <div key={status} className="bg-gray-50 rounded-lg p-3">
          <h3 className="font-semibold capitalize mb-2 text-sm text-gray-700">{status}</h3>
          <div className="space-y-2">
            {applications
              .filter((app) => app.status === status)
              .map((app) => (
                <div key={app.id} className="bg-white border rounded p-2 text-sm relative">
                  <button
                    onClick={() => handleRemove(app.id, app.posting.title)}
                    title="Remove from pipeline"
                    className="absolute top-1 right-1 text-gray-400 hover:text-red-600 text-xs leading-none w-4 h-4 flex items-center justify-center"
                  >
                    ×
                  </button>
                  <p className="font-medium pr-4">{app.posting.title}</p>
                  <p className="text-gray-500 text-xs mb-2">{app.posting.company}</p>
                  <select
                    value={app.status}
                    onChange={(e) => handleStatusChange(app.id, e.target.value)}
                    className="text-xs border rounded px-1 py-0.5 w-full"
                  >
                    {STATUSES.map((s) => (
                      <option key={s} value={s}>{s}</option>
                    ))}
                  </select>
                </div>
              ))}
          </div>
        </div>
      ))}
    </div>
  );
}
