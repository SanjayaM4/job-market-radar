import { useEffect, useState } from "react";
import { fetchApplications, updateApplicationStatus } from "../api";

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
                <div key={app.id} className="bg-white border rounded p-2 text-sm">
                  <p className="font-medium">{app.posting.title}</p>
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
