from datetime import datetime

import requests


def fetch_and_normalize():
    # RemoteOK asks for a descriptive User-Agent - a generic one can get blocked
    headers = {"User-Agent": "job-market-radar (personal project - github.com/SanjayaM4)"}
    response = requests.get("https://remoteok.com/api", headers=headers, timeout=15)
    response.raise_for_status()
    raw_jobs = response.json()

    # RemoteOK's first array element is a legal/metadata notice, not a job - drop it
    raw_jobs = [job for job in raw_jobs if "id" in job]

    normalized = []
    for job in raw_jobs:
        posted_date = None
        if job.get("date"):
            try:
                posted_date = datetime.fromisoformat(job["date"].replace("Z", "+00:00"))
            except ValueError:
                posted_date = None

        normalized.append({
            "external_id": str(job["id"]),
            "title": job.get("position"),
            "company": job.get("company"),
            "location": job.get("location") or "Remote",
            "description": job.get("description"),
            "url": job.get("url"),
            "posted_date": posted_date,
        })
    return normalized
