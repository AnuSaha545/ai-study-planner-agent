# 🚀 AI Study Planner - Complete Setup & Integration Guide

## 📋 Table of Contents
1. [Project Overview](#project-overview)
2. [Prerequisites](#prerequisites)
3. [Local Development Setup](#local-development-setup)
4. [Docker Setup](#docker-setup)
5. [Vercel Deployment](#vercel-deployment)
6. [Integration Guide](#integration-guide)
7. [Environment Variables](#environment-variables)
8. [Troubleshooting](#troubleshooting)

---

## 🎯 Project Overview

**AI Study Planner** is a full-stack application that uses AI to generate personalized weekly study plans with:
- **Backend**: Python FastAPI with Groq AI integration
- **Frontend**: React 19 with Vite bundler
- **Database**: PostgreSQL for persistent storage
- **Orchestration**: Kestra for workflow scheduling
- **Deployment**: Docker containerization + Vercel hosting

### Architecture
```
┌─────────────────────────────────────────────────┐
│           Frontend (React + Vite)               │
│  • Beautiful dark theme UI                      │
│  • Weekly planner component (Mon-Sun)           │
│  • Real-time form validation                    │
└─────────────┬───────────────────────────────────┘
              │ HTTP/REST API
┌─────────────▼───────────────────────────────────┐
│        Backend (FastAPI Python)                 │
│  • /plan endpoint for plan generation           │
│  • Agent orchestration (Planner + Resource)     │
│  • Groq AI integration (llama3-8b)              │
└─────────────┬───────────────────────────────────┘
              │
┌─────────────▼───────────────────────────────────┐
│     Database & Orchestration                    │
│  • PostgreSQL: Persistent storage               │
│  • Kestra: Workflow scheduling & monitoring     │
└─────────────────────────────────────────────────┘
```

---

## 📦 Prerequisites

### Required Software
- **Python 3.11+** ([download](https://www.python.org/downloads/))
- **Node.js 18+** ([download](https://nodejs.org/))
- **Docker & Docker Compose** ([download](https://www.docker.com/products/docker-desktop))
- **Git** ([download](https://git-scm.com/))
- **Groq API Key** ([get free key](https://console.groq.com/keys))

### System Requirements
- **RAM**: Minimum 4GB (8GB recommended)
- **Disk**: At least 2GB free space
- **OS**: Windows 10+, macOS 10.15+, or Linux

---

## 🏠 Local Development Setup

### Step 1: Clone & Enter Directory
```bash
cd /path/to/ai_study_planner_agent
```

### Step 2: Setup Backend

#### Create Virtual Environment
```bash
cd backend
python -m venv venv
```

#### Activate Virtual Environment
**Windows:**
```bash
venv\Scripts\activate
```

**macOS/Linux:**
```bash
source venv/bin/activate
```

#### Install Dependencies
```bash
pip install --upgrade pip
pip install -r requirements.txt
```

#### Configure Environment
Create `.env` in `backend/` directory:
```env
GROQ_API_KEY=your_actual_groq_api_key_here
LOG_LEVEL=INFO
DATABASE_URL=postgresql://planner:planner_password_123@localhost:5432/study_planner
```

#### Run Backend Server
```bash
# Development mode with auto-reload
uvicorn main:app --reload --port 8000

# Production mode
uvicorn main:app --host 0.0.0.0 --port 8000
```

Backend API will be available at: `http://localhost:8000`
- **API Docs**: http://localhost:8000/docs (Swagger UI)
- **Health Check**: http://localhost:8000/health

### Step 3: Setup Frontend

#### Install Dependencies
```bash
cd frontend
npm install
```

#### Configure Environment
Create `frontend/.env`:
```env
VITE_API_URL=http://localhost:8000
```

#### Run Development Server
```bash
npm run dev
```

Frontend will be available at: `http://localhost:5173`

### Step 4: Setup Database (Optional for Local Dev)

If you want to use PostgreSQL locally:

```bash
# Using Docker (easiest)
docker run -d \
  --name study_planner_db \
  -e POSTGRES_USER=planner \
  -e POSTGRES_PASSWORD=planner_password_123 \
  -e POSTGRES_DB=study_planner \
  -p 5432:5432 \
  -v postgres_data:/var/lib/postgresql/data \
  postgres:16-alpine

# Apply schema
psql postgresql://planner:planner_password_123@localhost:5432/study_planner < database/init.sql
```

---

## 🐳 Docker Setup

### Step 1: Verify File Structure
Ensure these files are at PROJECT ROOT:
- ✅ `Dockerfile`
- ✅ `docker-compose.yml`
- ✅ `.dockerignore`

### Step 2: Create `.env` File
At PROJECT ROOT, create `.env`:
```env
GROQ_API_KEY=your_actual_groq_api_key_here
```

### Step 3: Build & Start Containers
```bash
# Build images
docker-compose build

# Start all services
docker-compose up -d

# View logs
docker-compose logs -f
```

### Step 4: Verify Services
```bash
# Check running containers
docker-compose ps

# Access services
# Backend API: http://localhost:8000
# Kestra UI: http://localhost:8080
# PostgreSQL: localhost:5432 (planner:planner_password_123)
```

### Step 5: Stop Containers
```bash
# Stop all services
docker-compose down

# Stop and remove volumes (clears database)
docker-compose down -v

# Restart services
docker-compose restart
```

---

## 🚀 Vercel Deployment

### Step 1: Push to GitHub
```bash
git add -A
git commit -m "Deploy to Vercel"
git push origin main
```

### Step 2: Deploy on Vercel

1. Go to [vercel.com](https://vercel.com)
2. Click "New Project"
3. Import your GitHub repository
4. Configure settings:
   - **Framework Preset**: Vite
   - **Build Command**: `cd frontend && npm run build`
   - **Output Directory**: `frontend/dist`
   - **Install Command**: `cd frontend && npm install`

5. Add Environment Variables:
   ```
   VITE_API_URL=https://your-backend-domain.com
   ```

6. Click "Deploy"

### Step 3: Deploy Backend

Options:
- **Railway**: `railway link`
- **Render**: Import GitHub repo
- **Heroku**: `git push heroku main`
- **Your Own VPS**: Deploy Docker containers

---

## 🔧 Integration Guide

### API Integration

#### Generate Study Plan
```bash
curl -X POST http://localhost:8000/plan \
  -H "Content-Type: application/json" \
  -d '{
    "subjects": ["Python", "DSA", "React"],
    "hours": 3,
    "days_per_week": 6
  }'
```

#### Response Format
```json
{
  "plan": [
    {
      "day": "Monday",
      "total_hours": 3.0,
      "sessions": [
        {
          "subject": "Python",
          "session_type": "concept",
          "duration_hours": 1.0,
          "notes": "Build fundamentals of Python"
        }
      ]
    }
  ],
  "resources": {
    "Python": {
      "youtube_search": "https://www.youtube.com/results?search_query=Python",
      "pdf_search": "https://www.google.com/search?q=Python+pdf",
      "freecodecamp": "https://freecodecamp.org/..."
    }
  }
}
```

### Kestra Workflow Integration

Workflows are auto-loaded from `kestra/flows/` directory.

#### Example Workflow (`kestra/flows/study-planner-flow.yml`)
```yaml
id: generate-study-plan
namespace: ai.study_planner
description: Daily study plan generation

triggers:
  - id: daily-trigger
    type: io.kestra.core.models.triggers.types.Schedule
    expression: "0 8 * * *"  # 8 AM daily

tasks:
  - id: generate-plan
    type: io.kestra.core.tasks.http.Request
    url: "http://backend:8000/plan"
    method: POST
    contentType: application/json
    body: |
      {
        "subjects": ["Python", "DSA"],
        "hours": 3,
        "days_per_week": 6
      }

  - id: save-result
    type: io.kestra.core.tasks.log.Log
    message: "{{ taskrun.output }}"
```

---

## 🔐 Environment Variables

### Backend Environment Variables

| Variable | Required | Default | Description |
|----------|----------|---------|-------------|
| `GROQ_API_KEY` | Yes | - | Groq API key from [console.groq.com](https://console.groq.com/keys) |
| `DATABASE_URL` | No | - | PostgreSQL connection string |
| `LOG_LEVEL` | No | `INFO` | Logging level (DEBUG, INFO, WARNING, ERROR) |
| `BACKEND_PORT` | No | `8000` | Port for FastAPI server |
| `BACKEND_HOST` | No | `0.0.0.0` | Host binding for server |

### Frontend Environment Variables

| Variable | Required | Default | Description |
|----------|----------|---------|-------------|
| `VITE_API_URL` | No | `http://localhost:8000` | Backend API URL |

### Docker Environment Variables

| Variable | Value | Purpose |
|----------|-------|---------|
| `POSTGRES_USER` | `planner` | Database user |
| `POSTGRES_PASSWORD` | `planner_password_123` | Database password |
| `POSTGRES_DB` | `study_planner` | Database name |

---

## 🛠️ Troubleshooting

### Backend Issues

**Error: `GROQ_API_KEY not found`**
```bash
# Add to backend/.env
echo "GROQ_API_KEY=your_key" > backend/.env
```

**Error: `Cannot connect to database`**
```bash
# Check if PostgreSQL is running
docker ps | grep postgres

# Start database
docker-compose up -d postgres
```

**Error: `ModuleNotFoundError`**
```bash
# Reinstall dependencies
pip install -r requirements.txt --force-reinstall
```

### Frontend Issues

**Error: `Cannot find module`**
```bash
# Clear node_modules and reinstall
rm -rf node_modules package-lock.json
npm install
```

**Error: `VITE_API_URL undefined`**
```bash
# Check .env file exists in frontend/
cat frontend/.env

# Add if missing:
echo "VITE_API_URL=http://localhost:8000" > frontend/.env
```

### Docker Issues

**Error: `docker-compose: not found`**
```bash
# Update Docker
docker --version  # Should be 20.10+

# Use `docker compose` (newer syntax)
docker compose up -d
```

**Error: `port already in use`**
```bash
# Change ports in docker-compose.yml
# Or kill process using port:

# Windows
netstat -ano | findstr :8000
taskkill /PID <PID> /F

# macOS/Linux
lsof -i :8000
kill -9 <PID>
```

**Error: `database error`**
```bash
# Remove and reinitialize
docker-compose down -v
docker-compose up -d postgres
docker-compose up backend
```

### General Troubleshooting

**1. Check Service Health**
```bash
# Backend health
curl http://localhost:8000/health

# Kestra
curl http://localhost:8080

# Database
psql postgresql://planner:planner_password_123@localhost:5432/study_planner
```

**2. View Logs**
```bash
# Backend logs
docker-compose logs -f backend

# All logs
docker-compose logs -f

# Specific service
docker-compose logs -f postgres
```

**3. Reset Everything**
```bash
# Complete reset
docker-compose down -v
rm -rf backend/.venv frontend/node_modules
docker-compose build --no-cache
docker-compose up -d

# Clear frontend build cache
rm -rf frontend/dist
npm run build
```

---

## 📚 Additional Resources

- **FastAPI Docs**: https://fastapi.tiangolo.com/
- **React Documentation**: https://react.dev/
- **Groq API**: https://console.groq.com/
- **Kestra Workflow**: https://kestra.io/
- **Docker Guide**: https://docs.docker.com/

---

## 🤝 Contributing

To contribute to this project:

1. Create a feature branch: `git checkout -b feature/your-feature`
2. Make changes and test locally
3. Commit with clear messages: `git commit -am 'Add your feature'`
4. Push to GitHub: `git push origin feature/your-feature`
5. Create Pull Request

---

## 📝 License

This project is open source and available under the MIT License.

---

## 💡 Tips & Best Practices

### Development
- Use `npm run dev` for frontend development with hot reload
- Use `uvicorn main:app --reload` for backend development
- Check API docs at `/docs` for testing endpoints

### Production
- Always use environment variables, never hardcode secrets
- Set `LOG_LEVEL=WARNING` for production
- Enable database backups
- Use HTTPS for all connections
- Implement rate limiting on API endpoints

### Performance
- Cache study plans for 1 hour
- Use CDN for static assets
- Optimize database queries with indexes
- Monitor API response times

---

**Last Updated**: 2025-01-01
**Version**: 1.0.0
