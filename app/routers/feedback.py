from fastapi import APIRouter, Depends, HTTPException, Query, Request
from sqlalchemy.orm import Session
from typing import List, Optional
from ..database import SessionLocal
from .. import models, schemas
from ..services.feedback_service import create_feedback_service

router = APIRouter(prefix="/api", tags=["feedback"])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.get("/departments", response_model=List[schemas.DepartmentOut])
def list_departments(db: Session = Depends(get_db)):
    return db.query(models.Department).order_by(models.Department.name.asc()).all()

@router.get("/feedback", response_model=List[schemas.FeedbackOut])
def list_feedback(
    department: Optional[str] = None,
    sentiment: Optional[str] = None,
    status: Optional[str] = None,
    db: Session = Depends(get_db),
):
    q = db.query(models.Feedback)
    if department:
        q = q.filter(models.Feedback.department == department)
    if sentiment:
        q = q.filter(models.Feedback.sentiment == sentiment)
    if status:
        q = q.filter(models.Feedback.status == status)
    return q.order_by(models.Feedback.created_at.desc()).all()

@router.post("/feedback", response_model=schemas.FeedbackOut)
def create_feedback(payload: schemas.FeedbackCreate, db: Session = Depends(get_db)):
    from ..services.feedback_service import create_feedback_service
    
    payload_dict = payload.model_dump()
    fb = create_feedback_service(payload_dict, db)
    return fb