import os
from datetime import datetime
from fastapi import FastAPI, Request, Form, Depends, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse, RedirectResponse
from jinja2 import Environment, FileSystemLoader, select_autoescape
from .database import Base, engine, SessionLocal
from .models import Feedback, Department
from .routers import feedback as feedback_router
from .schemas import FeedbackCreate
from sqlalchemy.orm import Session
from sqlalchemy import select
from dotenv import load_dotenv

load_dotenv()

Base.metadata.create_all(bind=engine)

app = FastAPI(title=os.getenv("APP_NAME", "Parent–University Engagement"))

# Mount static files
static_dir = os.path.join(os.path.dirname(__file__), "static")
app.mount("/static", StaticFiles(directory=static_dir), name="static")

# Templates
templates_dir = os.path.join(os.path.dirname(__file__), "templates")
jinja_env = Environment(
    loader=FileSystemLoader(templates_dir),
    autoescape=select_autoescape(["html", "xml"]),
)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Include API router
app.include_router(feedback_router.router)

# Template context processor
def get_template_context(request: Request, **additional_context):
    base_context = {
        "request": request,
        "year": datetime.utcnow().year,
    }
    base_context.update(additional_context)
    return base_context

# ✅ Startup event to auto-seed departments
@app.on_event("startup")
def startup_event():
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()
    try:
        if db.query(Department).count() == 0:
            default_departments = [
                "Hostel", "Academics", "Finance", "Transport",
                "Health", "Counselling", "IT Support", "Student Affairs"
            ]
            for name in default_departments:
                db.add(Department(name=name))
            db.commit()
    except Exception as e:
        db.rollback()
        print(f"❌ Error seeding departments: {e}")
    finally:
        db.close()

# ---------------- ROUTES ---------------- #

@app.get("/", response_class=HTMLResponse)
def index(request: Request):
    template = jinja_env.get_template("index.html")
    context = get_template_context(request, title="Submit Feedback", result=None)
    html = template.render(**context)
    return HTMLResponse(html)

@app.post("/submit", response_class=HTMLResponse)
def submit_feedback(
    request: Request,
    parent_name: str = Form(...),
    parent_email: str = Form(...),
    student_id: str = Form(""),
    channel: str = Form("web"),
    message: str = Form(...),
    db: Session = Depends(get_db)
):
    from .services.feedback_service import create_feedback_service
    
    payload = {
        "parent_name": parent_name,
        "parent_email": parent_email,
        "student_id": student_id or None,
        "channel": channel or "web",
        "message": message,
    }
    
    fb = create_feedback_service(payload, db)
    
    template = jinja_env.get_template("index.html")
    context = get_template_context(
        request,
        title="Submit Feedback",
        result={
            "id": fb.id,
            "sentiment": fb.sentiment,
            "category": fb.category,
            "priority": fb.priority,
            "department": fb.department,
            "status": fb.status,
        }
    )
    html = template.render(**context)
    return HTMLResponse(html)

@app.get("/feedback", response_class=HTMLResponse)
def admin_feedback(
    request: Request,
    department: str | None = None,
    sentiment: str | None = None,
    status: str | None = None,
    db: Session = Depends(get_db)
):
    departments = db.execute(select(Department).order_by(Department.name.asc())).scalars().all()
    q = db.query(Feedback)
    if department:
        q = q.filter(Feedback.department == department)
    if sentiment:
        q = q.filter(Feedback.sentiment == sentiment)
    if status:
        q = q.filter(Feedback.status == status)
    items = q.order_by(Feedback.created_at.desc()).all()
    
    template = jinja_env.get_template("feedback_list.html")
    context = get_template_context(
        request,
        title="Feedback Admin",
        departments=departments,
        feedback=items,
    )
    html = template.render(**context)
    return HTMLResponse(html)

# ✅ Department card view
@app.get("/feedback/department/{dept_id}", response_class=HTMLResponse)
def department_feedback(request: Request, dept_id: int, db: Session = Depends(get_db)):
    department = db.query(Department).filter(Department.id == dept_id).first()
    if not department:
        raise HTTPException(status_code=404, detail="Department not found")
    assignments = db.query(Feedback).filter(Feedback.department == department.name).all()
    template = jinja_env.get_template("department_cards.html")
    context = get_template_context(
        request,
        title=f"{department.name} Assignments",
        department=department,
        assignments=assignments
    )
    html = template.render(**context)
    return HTMLResponse(html)

# ✅ Update feedback status
@app.post("/feedback/{fb_id}/status")
def update_feedback_status(
    fb_id: int,
    status: str = Form(...),
    db: Session = Depends(get_db)
):
    feedback = db.query(Feedback).filter(Feedback.id == fb_id).first()
    if not feedback:
        raise HTTPException(status_code=404, detail="Feedback not found")
    feedback.status = status
    db.commit()
    return HTMLResponse(f"""
        <script>
        alert("Status updated to {status}");
        window.history.back();
        </script>
    """)
