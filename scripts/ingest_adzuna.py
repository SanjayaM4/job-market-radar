"""
Run this to pull postings from Adzuna and insert any new ones into the database.

Usage:
    python scripts/ingest_adzuna.py
"""
from dateutil import parser as date_parser

from backend.app.db import SessionLocal
from backend.app.models import Posting
from backend.app.ingestion.adzuna import fetch_adzuna_postings


def run_adzuna_ingestion(query: str = "software developer"):
    session = SessionLocal()
    raw_postings = fetch_adzuna_postings(query=query)
    new_count = 0

    for job in raw_postings:
        external_id = str(job["id"])

        # skip it if we already have this exact posting from Adzuna
        existing = (
            session.query(Posting)
            .filter_by(source="adzuna", external_id=external_id)
            .first()
        )
        if existing:
            continue

        posting = Posting(
            source="adzuna",
            external_id=external_id,
            title=job.get("title"),
            company=(job.get("company") or {}).get("display_name"),
            location=(job.get("location") or {}).get("display_name"),
            description=job.get("description"),
            url=job.get("redirect_url"),
            posted_date=date_parser.parse(job["created"]) if job.get("created") else None,
        )
        session.add(posting)
        new_count += 1

    session.commit()
    session.close()
    print(f"Inserted {new_count} new posting(s) out of {len(raw_postings)} fetched.")


if __name__ == "__main__":
    run_adzuna_ingestion()
