from datetime import datetime, timezone

import requests


def fetch_and_normalize(company_slug: str):
    """
    company_slug is the company's Lever slug. If a company's careers
    page is jobs.lever.co/netflix, the slug is "netflix".
    """
    url = f"https://api.lever.co/v0/postings/{company_slug}?mode=json"
    response = requests.get(url, timeout=15)
    response.raise_for_status()
    raw_jobs = response.json()

    normalized = []
    for job in raw_jobs:
        posted_date = None
        if job.get("createdAt"):
            # Lever gives createdAt as a unix timestamp in milliseconds
            posted_date = datetime.fromtimestamp(job["createdAt"] / 1000, tz=timezone.utc)

        normalized.append({
            "external_id": str(job["id"]),
            "title": job.get("text"),
            "company": company_slug,
            "location": (job.get("categories") or {}).get("location"),
            "description": job.get("descriptionPlain") or job.get("description"),
            "url": job.get("hostedUrl"),
            "posted_date": posted_date,
        })
    return normalized
