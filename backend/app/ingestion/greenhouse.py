import requests
from dateutil import parser as date_parser

BASE_URL = "https://boards-api.greenhouse.io/v1/boards/{board_token}/jobs"


def fetch_and_normalize(board_token: str):
    """
    board_token is the company's Greenhouse slug. If a company's careers
    page is boards.greenhouse.io/stripe, the token is "stripe".
    """
    response = requests.get(BASE_URL.format(board_token=board_token), timeout=15)
    response.raise_for_status()
    raw_jobs = response.json().get("jobs", [])

    normalized = []
    for job in raw_jobs:
        normalized.append({
            "external_id": str(job["id"]),
            "title": job.get("title"),
            "company": board_token,
            "location": (job.get("location") or {}).get("name"),
            "description": job.get("content"),  # this is HTML, fine to store raw for now
            "url": job.get("absolute_url"),
            "posted_date": date_parser.parse(job["updated_at"]) if job.get("updated_at") else None,
        })
    return normalized
