# 📋 Quick Reference Guide

## 🚀 Start Development Immediately

### Backend (3 steps)
```bash
cd backend
python -m venv venv && source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
echo "GROQ_API_KEY=your_key_here" > .env
uvicorn main:app --reload
```
📍 **http://localhost:8000/docs** - API documentation

### Frontend (2 steps)
```bash
cd frontend
npm install
npm run dev
```
📍 **http://localhost:5173** - Web interface

---

## 🐳 Start with Docker

```bash
echo "GROQ_API_KEY=your_key_here" > .env
docker-compose up -d
```

| Service | URL | Port |
|---------|-----|------|
| Backend | http://localhost:8000 | 8000 |
| Kestra | http://localhost:8080 | 8080 |
| Database | localhost:5432 | 5432 |

---

## 📁 File Locations

| File | Location | Purpose |
|------|----------|---------|
| Dockerfile | `./Dockerfile` | Backend container |
| docker-compose.yml | `./docker-compose.yml` | Multi-service setup |
| .env | `./` (root) | Environment secrets |
| Backend API | `backend/main.py` | FastAPI app |
| Frontend App | `frontend/src/App.jsx` | React component |
| Weekly Planner | `frontend/src/components/WeeklyPlanner.jsx` | Calendar view |
| Database Schema | `database/init.sql` | PostgreSQL tables |
| Workflows | `kestra/flows/*.yml` | Kestra definitions |

---

## 🔧 Configuration Files

### Create Backend `.env`
```env
GROQ_API_KEY=sk_...
LOG_LEVEL=INFO
```

### Create Frontend `.env`
```env
VITE_API_URL=http://localhost:8000
```

### Get Groq API Key
1. Visit https://console.groq.com/keys
2. Create API key
3. Copy and paste into `.env`

---

## 📞 API Endpoints

### Generate Plan
```bash
POST /plan
Content-Type: application/json

{
  "subjects": ["Python", "DSA"],
  "hours": 3,
  "days_per_week": 6
}
```

### Health Check
```bash
GET /health
```

### API Documentation
```
GET /docs        # Swagger UI
GET /redoc       # ReDoc
```

---

## 🧪 Quick Tests

### Test Backend Health
```bash
curl http://localhost:8000/health
```

### Test Plan Generation
```bash
curl -X POST http://localhost:8000/plan \
  -H "Content-Type: application/json" \
  -d '{"subjects":["Python"],"hours":3,"days_per_week":6}'
```

### Test Database
```bash
psql -h localhost -U planner -d study_planner
# Password: planner_password_123
```

---

## 🐛 Troubleshooting

| Issue | Solution |
|-------|----------|
| `GROQ_API_KEY not found` | Add to `backend/.env` |
| Port 8000 in use | `lsof -i :8000 \| kill -9 <PID>` |
| VITE_API_URL undefined | Create `frontend/.env` |
| Database connection error | `docker-compose up -d postgres` |
| Node modules issue | `rm -rf node_modules && npm install` |

---

## 📚 File Checklist

✅ Dockerfile (at root)
✅ docker-compose.yml (at root)
✅ .dockerignore (at root)
✅ backend/.env (create with GROQ_API_KEY)
✅ backend/main.py (FastAPI)
✅ backend/agents/planner_agent.py
✅ backend/agents/resource_agent.py
✅ backend/cli.py
✅ backend/requirements.txt
✅ frontend/src/App.jsx
✅ frontend/src/App.css
✅ frontend/src/index.css
✅ frontend/src/components/WeeklyPlanner.jsx
✅ frontend/src/components/SessionCard.jsx
✅ frontend/src/components/SessionCard.css
✅ frontend/src/components/WeeklyPlanner.css
✅ database/init.sql
✅ kestra/flows/study-planner-flow.yml
✅ vercel.json
✅ SETUP.md
✅ README.md
✅ INTEGRATION_SUMMARY.md
✅ QUICK_REFERENCE.md (this file)

---

## 🚀 Deployment Checklist

### Pre-Deployment
- [ ] Add GROQ_API_KEY to backend/.env
- [ ] Test locally: `npm run dev` & `uvicorn main:app --reload`
- [ ] Test with Docker: `docker-compose up -d`
- [ ] Run backend tests: `curl http://localhost:8000/health`
- [ ] Run frontend: check http://localhost:5173

### GitHub
- [ ] `git add -A`
- [ ] `git commit -m "Deploy to production"`
- [ ] `git push origin main`

### Vercel (Frontend)
- [ ] Connect GitHub repo
- [ ] Set `VITE_API_URL` env var
- [ ] Auto-deploys on push

### Backend Hosting (Choose one)
- [ ] **Railway**: `railway link` + `railway up`
- [ ] **Render**: Import GitHub repo
- [ ] **Heroku**: `git push heroku main`
- [ ] **Your VPS**: `docker-compose up -d`

---

## 💡 Pro Tips

1. **Hot Reload**: Use `uvicorn main:app --reload` for automatic restarts
2. **API Testing**: Use `http://localhost:8000/docs` for interactive testing
3. **Clear Cache**: `rm -rf .venv node_modules && reinstall`
4. **Docker Logs**: `docker-compose logs -f backend`
5. **Reset DB**: `docker-compose down -v && docker-compose up`
6. **Check Ports**: `lsof -i -P | grep LISTEN`

---

## 📖 Documentation Links

- **Full Setup**: [SETUP.md](SETUP.md)
- **Integration**: [INTEGRATION_SUMMARY.md](INTEGRATION_SUMMARY.md)
- **Overview**: [README.md](README.md)
- **API Docs**: http://localhost:8000/docs

---

## 🎯 Common Commands

```bash
# Backend
uvicorn main:app --reload              # Dev server
python cli.py --help                   # CLI help
pip install -r requirements.txt        # Install deps

# Frontend
npm run dev                             # Dev server
npm run build                           # Build for production
npm install                             # Install deps

# Docker
docker-compose up -d                   # Start all services
docker-compose down                    # Stop all services
docker-compose logs -f                 # View logs
docker-compose ps                      # List containers

# Database
psql -h localhost -U planner -d study_planner
psql -f database/init.sql              # Run schema

# Git
git add -A && git commit -m "msg"
git push origin main
```

---

## 🔑 Environment Variables Reference

| Variable | Value | Required |
|----------|-------|----------|
| GROQ_API_KEY | sk_... | YES |
| VITE_API_URL | http://localhost:8000 | NO |
| LOG_LEVEL | INFO/DEBUG | NO |
| DATABASE_URL | postgresql://... | NO |
| BACKEND_PORT | 8000 | NO |

---

**Last Updated**: January 2025
**Version**: 1.0.0
**Status**: ✅ Production Ready
