from typing import List, Optional

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from backend.app.db import get_db
from backend.app.models import Posting
from backend.app.schemas import PostingOut

router = APIRouter(prefix="/postings", tags=["postings"])


@router.get("/", response_model=List[PostingOut])
def list_postings(
    min_score: Optional[float] = Query(None, description="only postings scoring at least this high"),
    source: Optional[str] = Query(None, description="filter by source, e.g. 'adzuna'"),
    limit: int = Query(50, le=200),
    offset: int = Query(0),
    db: Session = Depends(get_db),
):
    query = db.query(Posting)
    if min_score is not None:
        query = query.filter(Posting.match_score >= min_score)
    if source is not None:
        query = query.filter(Posting.source == source)

    query = query.order_by(Posting.match_score.desc().nullslast())
    return query.offset(offset).limit(limit).all()


@router.get("/{posting_id}", response_model=PostingOut)
def get_posting(posting_id: int, db: Session = Depends(get_db)):
    posting = db.query(Posting).filter(Posting.id == posting_id).first()
    if not posting:
        raise HTTPException(status_code=404, detail="Posting not found")
    return posting
