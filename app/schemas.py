from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import datetime

class DepartmentBase(BaseModel):
    name: str

class DepartmentCreate(DepartmentBase):
    pass

class DepartmentOut(DepartmentBase):
    id: int
    created_at: datetime
    
    class Config:
        from_attributes = True

class FeedbackBase(BaseModel):
    parent_name: str
    parent_email: EmailStr
    student_id: Optional[str] = None
    message: str
    channel: Optional[str] = "web"

class FeedbackCreate(FeedbackBase):
    pass

class FeedbackOut(FeedbackBase):
    id: int
    sentiment: str
    sentiment_score: float
    sentiment_confidence: float
    category: str
    priority: str
    department: str
    department_id: Optional[int]
    status: str
    created_at: datetime
    updated_at: Optional[datetime]
    
    class Config:
        from_attributes = True