import os

import requests
from dotenv import load_dotenv

load_dotenv()

APP_ID = os.getenv("ADZUNA_APP_ID")
APP_KEY = os.getenv("ADZUNA_APP_KEY")

# "ca" = Canada. Adzuna also supports "us", "gb", etc if you ever want to widen the search.
BASE_URL = "https://api.adzuna.com/v1/api/jobs/ca/search/1"


def fetch_adzuna_postings(query: str = "software developer", results_per_page: int = 20):
    """Hits the Adzuna search endpoint and returns the raw list of job dicts."""
    params = {
        "app_id": APP_ID,
        "app_key": APP_KEY,
        "what": query,
        "results_per_page": results_per_page,
        "content-type": "application/json",
    }
    response = requests.get(BASE_URL, params=params, timeout=15)
    response.raise_for_status()
    return response.json()["results"]
