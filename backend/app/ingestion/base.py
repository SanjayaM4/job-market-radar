from backend.app.db import SessionLocal
from backend.app.models import Posting


def save_postings(source: str, normalized_postings: list) -> int:
    """
    Takes a list of already-normalized posting dicts and inserts any new ones.
    Every ingestion source funnels through this same function - this is the
    shared interface that keeps sources interchangeable. A source module's
    only job is to return dicts shaped like:
        {external_id, title, company, location, description, url, posted_date}
    """
    session = SessionLocal()
    new_count = 0

    for job in normalized_postings:
        existing = (
            session.query(Posting)
            .filter_by(source=source, external_id=job["external_id"])
            .first()
        )
        if existing:
            continue

        posting = Posting(source=source, **job)
        session.add(posting)
        new_count += 1

    session.commit()
    session.close()
    return new_count
