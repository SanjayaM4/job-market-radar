"""
Manually queues the two Celery tasks once, without waiting for the schedule.
Useful for confirming everything is wired up correctly. Requires the Celery
worker (Phase 5 step 3) to already be running in another terminal.

Usage:
    python -m scripts.trigger_tasks
"""
from backend.app.tasks import ingest_all_task, match_postings_task

if __name__ == "__main__":
    print("Queuing ingest_all_task...")
    ingest_all_task.delay()
    print("Queuing match_postings_task...")
    match_postings_task.delay()
    print("Tasks queued - check the celery worker terminal window for output.")
