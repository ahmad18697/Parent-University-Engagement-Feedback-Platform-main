# Parent–University Engagement & Feedback Platform

A production-ready, AI-powered feedback management system that streamlines communication between parents and educational institutions. Built with **FastAPI** and enhanced with optional **LangChain AI routing**, it automatically analyzes, categorizes, prioritizes, and routes feedback to the right department.

![FastAPI](https://img.shields.io/badge/FastAPI-005571?style=for-the-badge\&logo=fastapi)
![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge\&logo=python\&logoColor=white)
![SQLite](https://img.shields.io/badge/SQLite-07405E?style=for-the-badge\&logo=sqlite\&logoColor=white)
![LangChain](https://img.shields.io/badge/LangChain-FF6B00?style=for-the-badge)
![AI-Powered](https://img.shields.io/badge/AI-Powered-FF6B00?style=for-the-badge)

---

## 🚀 Key Features

* **🤖 Intelligent AI Routing**: Automated sentiment analysis, category detection, and priority scoring.
* **🌐 Modern Web Interface**: Clean, responsive UI with a built‑in admin dashboard.
* **📊 Filters & Analytics**: View by department, sentiment, status, and category.
* **🔌 RESTful API**: JSON endpoints for integration with other systems.
* **📱 Mobile Responsive**: Works great on desktop and mobile.
* **🔒 Persistence**: SQLite + SQLAlchemy ORM; easy to swap to other DBs.
* **🎨 Professional UI**: Dark themed dashboard with intuitive navigation.

---

## 🏗️ Architecture Overview

```
Request → FastAPI → AI Processing → Database → Response
                 ├── Sentiment Analysis
                 ├── Category Classification
                 ├── Priority Assessment
                 └── Department Routing
```

* **Sentiment Analysis**: VADER (no external API required)
* **Routing**: Rule‑based by default; optionally upgrade to LangChain + LLM

---

## 📦 Installation & Setup

### Prerequisites

* Python 3.10+ recommended (3.8+ supported)
* `pip` package manager

### 1) Clone & Create Virtual Environment

```bash
python -m venv .venv
# Linux/Mac
source .venv/bin/activate
# Windows (PowerShell)
.\.venv\Scripts\Activate.ps1
```

### 2) Install Dependencies

```bash
pip install -r requirements.txt
```

### 3) Configure Environment

Create a `.env` (or copy `.env.example`):

```env
APP_NAME="Parent–University Engagement Portal"
DATABASE_URL="sqlite:///./feedback.db"
USE_LLM=false
# If USE_LLM=true, provide an API key compatible with your LLM provider
OPENAI_API_KEY="sk-..."
```

### 4) Launch the Application

```bash
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

### 5) Access the Platform

* **Web Interface**: [http://localhost:8000](http://localhost:8000)
* **Admin Dashboard**: [http://localhost:8000/feedback](http://localhost:8000/feedback)
* **API Documentation (Swagger)**: [http://localhost:8000/docs](http://localhost:8000/docs)

> 💡 To enable the LangChain LLM router, set `USE_LLM=true` in `.env` and provide `OPENAI_API_KEY`. When disabled, the app uses local VADER + keyword routing.

---

## 🗂️ Project Structure

```
app/
├── main.py                  # FastAPI app & web routes
├── database.py              # SQLAlchemy engine/session setup
├── models.py                # ORM models
├── schemas.py               # Pydantic schemas
├── routers/
│   └── feedback.py          # JSON API endpoints
├── services/
│   ├── feedback_service.py  # Create/list logic
│   ├── routing_agent.py     # Sentiment + category + priority + routing
│   ├── sentiment.py         # VADER sentiment wrapper
│   └── categorizer.py       # Keyword classifier + priority/department maps
├── static/
│   ├── style.css            # UI styles
│   └── script.js            # Dashboard interactivity
└── templates/
    ├── base.html            # Layout
    ├── index.html           # Feedback submission form
    └── feedback_list.html   # Admin dashboard
```

---

## 🎯 How It Works

1. **Submission**: Parents submit via the web form or API (name, optional email & student, message, channel).
2. **AI Pipeline**:

   * *Sentiment*: positive/neutral/negative
   * *Category*: academics/hostel/finance/health/transport/admissions/discipline/other
   * *Priority*: high/medium/low (keywords + sentiment)
   * *Routing*: maps to department (e.g., **Finance → Bursar's Office**)
3. **Management**: Admin dashboard lists items with filters, status updates, and quick actions.

---

## 📡 API Endpoints

### Feedback Operations

| Method | Endpoint             | Description                    |              |             |
| -----: | -------------------- | ------------------------------ | ------------ | ----------- |
|   POST | `/api/feedback`      | Submit new feedback            |              |             |
|    GET | `/api/feedback`      | Retrieve feedback (filterable) |              |             |
|    GET | `/api/departments`   | List available departments     |              |             |
|  PATCH | `/api/feedback/{id}` | Update status (\`open          | in\_progress | resolved\`) |

### Example Requests

**Create feedback**

```bash
curl -X POST http://localhost:8000/api/feedback \
  -H "Content-Type: application/json" \
  -d '{
    "parent_name": "A. Raza",
    "parent_email": "raza@example.com",
    "student_name": "Imran",
    "message": "Bus service is often late and hostel mess needs improvement.",
    "channel": "web"
  }'
```

**List feedback (filter by department)**

```bash
curl "http://localhost:8000/api/feedback?department=Transport%20Office"
```

**Update status**

```bash
curl -X PATCH http://localhost:8000/api/feedback/1 \
  -H "Content-Type: application/json" \
  -d '{"status":"in_progress"}'
```

---

## 🔧 Configuration Options

* **`APP_NAME`**: Title shown in the UI & OpenAPI docs.
* **`DATABASE_URL`**: Set to Postgres/MySQL easily (e.g., `postgresql+psycopg://...`).
* **`USE_LLM`**: `true` to enable LangChain routing with an LLM.
* **`OPENAI_API_KEY`**: Required only when `USE_LLM=true`.

> For production, consider running behind a reverse proxy and using a managed DB.

---

## 🧪 Testing (optional)

If you add tests under `tests/`, run them with:

```bash
pytest -v
```

---

## 🐳 Docker (optional)

Build and run with Docker:

```bash
docker build -t parent-feedback .
docker run -p 8000:8000 --env-file .env parent-feedback
```

---

## ✅ Checklist

* [ ] Create and activate virtualenv
* [ ] `pip install -r requirements.txt`
* [ ] Copy `.env.example` → `.env`
* [ ] `uvicorn app.main:app --reload`
* [ ] Open **/docs** and test the API
* [ ] (Optional) Enable `USE_LLM=true`

---


