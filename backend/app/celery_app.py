import os

from celery import Celery
from celery.schedules import crontab
from dotenv import load_dotenv

load_dotenv()

REDIS_URL = os.getenv("REDIS_URL", "redis://localhost:6379/0")

celery_app = Celery(
    "job_radar",
    broker=REDIS_URL,
    backend=REDIS_URL,
    include=["backend.app.tasks"],  # makes sure Celery finds the task definitions
)

celery_app.conf.timezone = "America/Toronto"

# Runs ingestion, then matching 15 minutes later so new postings get scored.
# crontab(minute=0, hour="*/3") = at minute 0, every 3rd hour (00:00, 03:00, 06:00...)
celery_app.conf.beat_schedule = {
    "ingest-all-every-3-hours": {
        "task": "backend.app.tasks.ingest_all_task",
        "schedule": crontab(minute=0, hour="*/3"),
    },
    "match-postings-every-3-hours": {
        "task": "backend.app.tasks.match_postings_task",
        "schedule": crontab(minute=15, hour="*/3"),
    },
}
