const API_BASE = import.meta.env.VITE_API_BASE || "http://localhost:8000";

export async function fetchPostings(minScore = 0) {
  const res = await fetch(`${API_BASE}/postings/?min_score=${minScore}&limit=100`);
  if (!res.ok) throw new Error("Failed to fetch postings");
  return res.json();
}

export async function fetchApplications() {
  const res = await fetch(`${API_BASE}/applications/`);
  if (!res.ok) throw new Error("Failed to fetch applications");
  return res.json();
}

export async function createApplication(postingId) {
  const res = await fetch(`${API_BASE}/applications/`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ posting_id: postingId }),
  });
  if (!res.ok) throw new Error("Failed to create application");
  return res.json();
}

export async function updateApplicationStatus(applicationId, status) {
  const res = await fetch(`${API_BASE}/applications/${applicationId}`, {
    method: "PATCH",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ status }),
  });
  if (!res.ok) throw new Error("Failed to update application");
  return res.json();
}
