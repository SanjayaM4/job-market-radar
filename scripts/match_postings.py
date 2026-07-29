"""
Scores every posting that doesn't yet have a match_score against your profile,
and sends a Discord notification for any posting that crosses the match
threshold set in .env (MATCH_SCORE_THRESHOLD).

Usage (run from project root, with venv active):
    python -m scripts.match_postings
"""
import os
from pathlib import Path

from dotenv import load_dotenv

from backend.app.db import SessionLocal
from backend.app.models import Posting
from backend.app.matching.matcher import compute_match_score
from backend.app.notifications.discord import send_discord_notification

load_dotenv()

PROFILE_PATH = Path(__file__).resolve().parent.parent / "profile.txt"
MATCH_SCORE_THRESHOLD = float(os.getenv("MATCH_SCORE_THRESHOLD", 0.65))


def run_matching():
    profile_text = PROFILE_PATH.read_text(encoding="utf-8")

    session = SessionLocal()
    unscored = session.query(Posting).filter(Posting.match_score.is_(None)).all()

    notified_count = 0
    for posting in unscored:
        posting_text = f"{posting.title}. {posting.description or ''}"
        score = compute_match_score(profile_text, posting_text)
        posting.match_score = score

        if score >= MATCH_SCORE_THRESHOLD:
            send_discord_notification(
                title=f"New match: {posting.title}",
                message=f"{posting.company or 'Unknown company'} — score {score:.2f}\n{posting.url}",
            )
            notified_count += 1

    session.commit()
    session.close()
    print(f"Scored {len(unscored)} posting(s), notified on {notified_count}.")


if __name__ == "__main__":
    run_matching()
