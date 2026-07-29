"""
Prints the highest-scoring postings found so far.

Usage:
    python -m scripts.top_matches
"""
from backend.app.db import SessionLocal
from backend.app.models import Posting


def show_top_matches(limit: int = 10):
    session = SessionLocal()
    top = (
        session.query(Posting)
        .filter(Posting.match_score.isnot(None))
        .order_by(Posting.match_score.desc())
        .limit(limit)
        .all()
    )
    session.close()

    for p in top:
        print(f"{p.match_score:.3f}  |  {p.title}  @ {p.company}  ({p.source})  -> {p.url}")


if __name__ == "__main__":
    show_top_matches()
