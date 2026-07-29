from typing import List, Optional

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from backend.app.db import get_db
from backend.app.models import Application, Posting, ApplicationStatus
from backend.app.schemas import ApplicationCreate, ApplicationUpdate, ApplicationOut

router = APIRouter(prefix="/applications", tags=["applications"])


@router.post("/", response_model=ApplicationOut, status_code=201)
def create_application(payload: ApplicationCreate, db: Session = Depends(get_db)):
    posting = db.query(Posting).filter(Posting.id == payload.posting_id).first()
    if not posting:
        raise HTTPException(status_code=404, detail="Posting not found")

    existing = db.query(Application).filter(Application.posting_id == payload.posting_id).first()
    if existing:
        raise HTTPException(status_code=400, detail="This posting is already being tracked")

    application = Application(
        posting_id=payload.posting_id,
        status=payload.status,
        notes=payload.notes,
    )
    db.add(application)
    db.commit()
    db.refresh(application)
    return application


@router.get("/", response_model=List[ApplicationOut])
def list_applications(
    status: Optional[ApplicationStatus] = Query(None),
    db: Session = Depends(get_db),
):
    query = db.query(Application)
    if status is not None:
        query = query.filter(Application.status == status)
    return query.order_by(Application.updated_at.desc()).all()


@router.patch("/{application_id}", response_model=ApplicationOut)
def update_application(application_id: int, payload: ApplicationUpdate, db: Session = Depends(get_db)):
    application = db.query(Application).filter(Application.id == application_id).first()
    if not application:
        raise HTTPException(status_code=404, detail="Application not found")

    if payload.status is not None:
        application.status = payload.status
    if payload.notes is not None:
        application.notes = payload.notes

    db.commit()
    db.refresh(application)
    return application


@router.delete("/{application_id}", status_code=204)
def delete_application(application_id: int, db: Session = Depends(get_db)):
    application = db.query(Application).filter(Application.id == application_id).first()
    if not application:
        raise HTTPException(status_code=404, detail="Application not found")
    db.delete(application)
    db.commit()
    return None
