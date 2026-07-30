FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY backend/ ./backend/
COPY scripts/ ./scripts/
COPY tests/ ./tests/
COPY profile.txt .
COPY alembic.ini .
COPY alembic/ ./alembic/

EXPOSE 8000

# Default command runs the API. The worker/beat services override this
# with their own `command:` in docker-compose.yml, reusing this same image.
CMD ["uvicorn", "backend.app.main:app", "--host", "0.0.0.0", "--port", "8000"]
