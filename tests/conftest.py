import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from backend.app.models import Base, Posting
from backend.app.db import get_db
from backend.app.main import app

# In-memory SQLite for tests - fast, no Docker/Postgres required to run the
# suite. StaticPool keeps it as a single shared connection, since a plain
# in-memory SQLite DB otherwise resets between connections.
TEST_DATABASE_URL = "sqlite:///:memory:"

engine = create_engine(
    TEST_DATABASE_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)
TestingSessionLocal = sessionmaker(bind=engine, autocommit=False, autoflush=False)


def override_get_db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()


app.dependency_overrides[get_db] = override_get_db


@pytest.fixture(autouse=True)
def setup_db():
    """Fresh tables before every test, dropped after - tests never see each other's data."""
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)


@pytest.fixture
def client():
    return TestClient(app)


@pytest.fixture
def sample_posting():
    db = TestingSessionLocal()
    posting = Posting(
        source="adzuna",
        external_id="abc123",
        title="Backend Developer",
        company="Acme Corp",
        location="Toronto, ON",
        match_score=0.8,
    )
    db.add(posting)
    db.commit()
    db.refresh(posting)
    db.close()
    return posting
