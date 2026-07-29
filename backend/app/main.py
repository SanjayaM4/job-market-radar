from fastapi import FastAPI

from backend.app.routers import postings, applications

app = FastAPI(title="Smart Job Market Radar", version="0.1.0")

app.include_router(postings.router)
app.include_router(applications.router)


@app.get("/health")
def health_check():
    """Basic liveness check - confirms the API process is up and reachable."""
    return {"status": "ok"}
