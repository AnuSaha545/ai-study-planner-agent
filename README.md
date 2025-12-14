# ✨ AI Study Planner Agent

> **An AI-powered system for generating personalized weekly study plans with intelligent scheduling and curated learning resources.**
> 
---

## 🎯 Key Features

✅ **AI-Powered Planning** - Groq's llama3-8b generates personalized schedules  
✅ **Beautiful UI** - Dark theme with cool & calm aesthetics  
✅ **Weekly Calendar** - Mon-Sun view with time slots  
✅ **Resource Curation** - YouTube, PDFs, FreeCodeCamp links  
✅ **Multi-Agent System** - Planner + Resource agents  
✅ **Docker Ready** - Full containerization  
✅ **Vercel Deploy** - Production-ready frontend  

---

## 🚀 Quick Start

### Option 1: Local Development
```bash
# Backend
cd backend
python -m venv venv && source venv/bin/activate
pip install -r requirements.txt
echo "GROQ_API_KEY=your_key" > .env
uvicorn main:app --reload

# Frontend (new terminal)
cd frontend
npm install
VITE_API_URL=http://localhost:8000 npm run dev
```

**Visit**: http://localhost:5173

### Option 2: Docker
```bash
echo "GROQ_API_KEY=your_key" > .env
docker-compose up -d
```

**Services**:
- Frontend: http://localhost:5173
- Backend: http://localhost:8000
- Kestra: http://localhost:8080

---

## 📖 Usage

### Web Interface
1. Enter subjects: "Python, DSA, React"
2. Set hours (0.5-12) and days (1-7)
3. Generate plan
4. View weekly schedule with resources

### API
```bash
curl -X POST http://localhost:8000/plan \
  -H "Content-Type: application/json" \
  -d '{"subjects": ["Python", "DSA"], "hours": 3, "days_per_week": 6}'
```

### CLI
```bash
python cli.py --subjects "Python,DSA" --hours 3 --days 6
```

---

## 🏗️ Architecture

```
React Frontend 
         ↓
FastAPI Backend (/plan endpoint)
         ↓
PlannerAgent → ResourceAgent
         ↓
PostgreSQL + Kestra
```

---

---

## 🔧 Configuration

Create `backend/.env`:
```env
GROQ_API_KEY=sk_...your_key...
LOG_LEVEL=INFO
DATABASE_URL=postgresql://planner:planner_password_123@localhost:5432/study_planner
```

---

## 📊 API Response

```json
{
  "plan": [
    {
      "day": "Monday",
      "total_hours": 3.0,
      "sessions": [{
        "subject": "Python",
        "session_type": "concept",
        "duration_hours": 1.0,
        "notes": "Build fundamentals..."
      }]
    }
  ],
  "resources": {
    "Python": {
      "youtube_search": "...",
      "pdf_search": "...",
      "freecodecamp": "..."
    }
  }
}
```

---

## 🚀 Deployment

**Vercel** (Frontend):
- Auto-deploy from GitHub
- Set `VITE_API_URL` environment variable

**Docker** (Backend):
- Run `docker-compose up -d`
- Deploy to Railway, Render, or your VPS

---

## 📚 Documentation

- **Setup Guide**: [SETUP.md](SETUP.md)
- **API Docs**: http://localhost:8000/docs
- **Groq Console**: https://console.groq.com/

---

## ✨ Technologies

- **Backend**: FastAPI, Pydantic, Groq API
- **Frontend**: React 19, Vite, CSS Grid
- **Database**: PostgreSQL 16
- **Orchestration**: Kestra
- **Deployment**: Docker, Vercel
- **CLI**: Click (Python)

---


## Why Kestra?

Kestra is used as the workflow orchestration layer to coordinate
backend API calls, validate execution logic, and enable decision-based
agent behavior. This allows the AI Study Planner to scale from a simple
API into a production-ready, observable agent system with retries,
branching, and scheduling support.


## Author

**Anu Saha**

Engineering student and full-stack developer with a strong interest in
AI systems, workflow orchestration, and scalable backend architectures.
