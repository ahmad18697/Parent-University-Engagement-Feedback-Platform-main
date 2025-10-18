from sqlalchemy import Column, Integer, String, DateTime, Text, ForeignKey, Float
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from .database import Base

class Department(Base):
    __tablename__ = "departments"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    feedback = relationship("Feedback", back_populates="department_rel")

class Feedback(Base):
    __tablename__ = "feedback"
    
    id = Column(Integer, primary_key=True, index=True)
    parent_name = Column(String, index=True)
    parent_email = Column(String, index=True)
    student_id = Column(String, index=True, nullable=True)
    message = Column(Text)
    channel = Column(String, default="web")
    
    # AI-processed fields
    sentiment = Column(String, default="neutral")
    sentiment_score = Column(Float, default=0.0)
    sentiment_confidence = Column(Float, default=0.0)
    category = Column(String, default="General")
    priority = Column(String, default="low")
    department = Column(String, default="Student Affairs")
    department_id = Column(Integer, ForeignKey("departments.id"), nullable=True)
    
    # Status tracking
    status = Column(String, default="new")
    
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    department_rel = relationship("Department", back_populates="feedback")