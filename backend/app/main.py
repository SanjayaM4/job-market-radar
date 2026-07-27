from fastapi import FastAPI

app = FastAPI(title="Smart Job Market Radar", version="0.1.0")


@app.get("/health")
def health_check():
    """Basic liveness check - confirms the API process is up and reachable."""
    return {"status": "ok"}
