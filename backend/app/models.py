import datetime

from sqlalchemy import Column, Integer, String, Text, DateTime, Float, UniqueConstraint
from sqlalchemy.orm import declarative_base

Base = declarative_base()


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
    match_score = Column(Float, nullable=True)        # filled in by the matcher service later
    fetched_at = Column(DateTime, default=datetime.datetime.utcnow)

    __table_args__ = (
        # one row per posting per source - reruns won't create duplicates
        UniqueConstraint("source", "external_id", name="uq_source_external_id"),
    )
