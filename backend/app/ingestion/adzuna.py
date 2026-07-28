import os

import requests
from dateutil import parser as date_parser
from dotenv import load_dotenv

load_dotenv()

APP_ID = os.getenv("ADZUNA_APP_ID")
APP_KEY = os.getenv("ADZUNA_APP_KEY")

# "ca" = Canada. Swap for "us", "gb" etc if you ever want to widen the search.
BASE_URL = "https://api.adzuna.com/v1/api/jobs/ca/search/1"


def fetch_and_normalize(query: str = "software developer", results_per_page: int = 20):
    params = {
        "app_id": APP_ID,
        "app_key": APP_KEY,
        "what": query,
        "results_per_page": results_per_page,
        "content-type": "application/json",
    }
    response = requests.get(BASE_URL, params=params, timeout=15)
    response.raise_for_status()
    raw_jobs = response.json()["results"]

    normalized = []
    for job in raw_jobs:
        normalized.append({
            "external_id": str(job["id"]),
            "title": job.get("title"),
            "company": (job.get("company") or {}).get("display_name"),
            "location": (job.get("location") or {}).get("display_name"),
            "description": job.get("description"),
            "url": job.get("redirect_url"),
            "posted_date": date_parser.parse(job["created"]) if job.get("created") else None,
        })
    return normalized
