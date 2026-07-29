"""
Scores every posting that doesn't yet have a match_score against your profile.

Usage (run from project root, with venv active):
    python -m scripts.match_postings
"""
from pathlib import Path

from backend.app.db import SessionLocal
from backend.app.models import Posting
from backend.app.matching.matcher import compute_match_score

PROFILE_PATH = Path(__file__).resolve().parent.parent / "profile.txt"


def run_matching():
    profile_text = PROFILE_PATH.read_text(encoding="utf-8")

    session = SessionLocal()
    unscored = session.query(Posting).filter(Posting.match_score.is_(None)).all()

    for posting in unscored:
        posting_text = f"{posting.title}. {posting.description or ''}"
        posting.match_score = compute_match_score(profile_text, posting_text)

    session.commit()
    session.close()
    print(f"Scored {len(unscored)} posting(s).")


if __name__ == "__main__":
    run_matching()
