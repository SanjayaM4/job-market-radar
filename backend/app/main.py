from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from backend.app.routers import postings, applications

app = FastAPI(title="Smart Job Market Radar", version="0.1.0")

# Allows the React dev server (Vite, port 5173) to call this API from the browser.
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(postings.router)
app.include_router(applications.router)


@app.get("/health")
def health_check():
    """Basic liveness check - confirms the API process is up and reachable."""
    return {"status": "ok"}
