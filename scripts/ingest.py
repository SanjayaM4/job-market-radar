"""
Runs ingestion for one or more sources. Each source module only needs to
expose fetch_and_normalize() - this runner and save_postings() don't care
which source it is, that's the whole point of the shared interface.

Usage (run from project root, with venv active):
    python -m scripts.ingest --source adzuna
    python -m scripts.ingest --source remoteok
    python -m scripts.ingest --source greenhouse --company stripe
    python -m scripts.ingest --source lever --company netflix
    python -m scripts.ingest --source all
"""
import argparse

from backend.app.ingestion.base import save_postings
from backend.app.ingestion import adzuna, remoteok, greenhouse, lever

# Companies to track on Greenhouse/Lever when no --company flag is given.
# Edit these to whichever companies you actually want to watch - see the
# instructions for how to find a company's board token/slug.
GREENHOUSE_COMPANIES = ["stripe"]
LEVER_COMPANIES = ["netflix", "testname"]


def run(source: str, company: str = None):
    if source == "adzuna":
        postings = adzuna.fetch_and_normalize()
        count = save_postings("adzuna", postings)
        print(f"[adzuna] inserted {count} new posting(s)")

    elif source == "remoteok":
        postings = remoteok.fetch_and_normalize()
        count = save_postings("remoteok", postings)
        print(f"[remoteok] inserted {count} new posting(s)")

    elif source == "greenhouse":
        companies = [company] if company else GREENHOUSE_COMPANIES
        for c in companies:
            try:
                postings = greenhouse.fetch_and_normalize(c)
                count = save_postings("greenhouse", postings)
                print(f"[greenhouse:{c}] inserted {count} new posting(s)")
            except Exception as e:
                print(f"[greenhouse:{c}] failed: {e}")

    elif source == "lever":
        companies = [company] if company else LEVER_COMPANIES
        for c in companies:
            try:
                postings = lever.fetch_and_normalize(c)
                count = save_postings("lever", postings)
                print(f"[lever:{c}] inserted {count} new posting(s)")
            except Exception as e:
                print(f"[lever:{c}] failed: {e}")

    elif source == "all":
        run("adzuna")
        run("remoteok")
        run("greenhouse")
        run("lever")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--source", required=True,
        choices=["adzuna", "remoteok", "greenhouse", "lever", "all"],
    )
    parser.add_argument("--company", required=False, help="override for a single greenhouse/lever company")
    args = parser.parse_args()
    run(args.source, args.company)
