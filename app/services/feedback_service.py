from sqlalchemy.orm import Session
from .. import models
from .routing_agent import run_agent

def create_feedback_service(payload, db: Session):
    """
    Service function to create feedback (to avoid circular imports)
    """
    agent_out = run_agent(payload)
    # Find department_id if exists
    dept = db.query(models.Department).filter(models.Department.name==agent_out["department"]).first()
    
    fb = models.Feedback(
        parent_name=payload["parent_name"],
        parent_email=payload["parent_email"],
        student_id=payload.get("student_id"),
        message=payload["message"],
        channel=payload.get("channel", "web"),
        sentiment=agent_out["sentiment"],
        sentiment_score=float(agent_out["sentiment_score"]),
        sentiment_confidence=float(agent_out["sentiment_confidence"]),
        category=agent_out["category"],
        priority=agent_out["priority"],
        department=agent_out["department"],
        department_id=dept.id if dept else None,
    )
    db.add(fb)
    db.commit()
    db.refresh(fb)
    return fb