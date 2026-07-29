from backend.app.celery_app import celery_app
from scripts.ingest import run as run_ingest
from scripts.match_postings import run_matching


@celery_app.task(name="backend.app.tasks.ingest_all_task")
def ingest_all_task():
    run_ingest("all")


@celery_app.task(name="backend.app.tasks.match_postings_task")
def match_postings_task():
    run_matching()
