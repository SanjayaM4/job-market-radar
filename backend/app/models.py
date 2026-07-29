import datetime
import enum

from sqlalchemy import (
    Column, Integer, String, Text, DateTime, Float,
    ForeignKey, UniqueConstraint, Enum as SAEnum,
)
from sqlalchemy.orm import declarative_base, relationship

Base = declarative_base()


class ApplicationStatus(str, enum.Enum):
    SAVED = "saved"
    APPLIED = "applied"
    INTERVIEW = "interview"
    OFFER = "offer"
    REJECTED = "rejected"


class Posting(Base):
    __tablename__ = "postings"

    id = Column(Integer, primary_key=True)
    source = Column(String, nullable=False)          # e.g. "adzuna", "greenhouse"
    external_id = Column(String, nullable=False)      # the source's own ID for this posting
    title = Column(String, nullable=False)
    company = Column(String)
    location = Column(String)
    description = Column(Text)
    url = Column(String)
    posted_date = Column(DateTime, nullable=True)
    match_score = Column(Float, nullable=True)        # filled in by the matcher service
    fetched_at = Column(DateTime, default=datetime.datetime.utcnow)

    applications = relationship("Application", back_populates="posting")

    __table_args__ = (
        # one row per posting per source - reruns won't create duplicates
        UniqueConstraint("source", "external_id", name="uq_source_external_id"),
    )


class Application(Base):
    __tablename__ = "applications"

    id = Column(Integer, primary_key=True)
    posting_id = Column(Integer, ForeignKey("postings.id"), nullable=False, unique=True)
    status = Column(SAEnum(ApplicationStatus), nullable=False, default=ApplicationStatus.SAVED)
    notes = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.datetime.utcnow, onupdate=datetime.datetime.utcnow)

    posting = relationship("Posting", back_populates="applications")
