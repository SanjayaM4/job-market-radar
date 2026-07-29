from datetime import datetime
from typing import Optional

from pydantic import BaseModel

from backend.app.models import ApplicationStatus


class PostingOut(BaseModel):
    id: int
    source: str
    title: str
    company: Optional[str] = None
    location: Optional[str] = None
    url: Optional[str] = None
    posted_date: Optional[datetime] = None
    match_score: Optional[float] = None

    class Config:
        from_attributes = True


class ApplicationCreate(BaseModel):
    posting_id: int
    status: ApplicationStatus = ApplicationStatus.SAVED
    notes: Optional[str] = None


class ApplicationUpdate(BaseModel):
    status: Optional[ApplicationStatus] = None
    notes: Optional[str] = None


class ApplicationOut(BaseModel):
    id: int
    posting_id: int
    status: ApplicationStatus
    notes: Optional[str] = None
    created_at: datetime
    updated_at: datetime
    posting: PostingOut

    class Config:
        from_attributes = True
