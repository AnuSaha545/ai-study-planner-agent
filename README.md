✨ AI Study Planner Agent

An AI-powered system that generates personalized weekly study plans with intelligent scheduling and curated learning resources.

This project is designed to help students plan their studies efficiently using AI-driven reasoning,
a clean user interface, and a scalable backend architecture.

---

🚀 Live Demo

Frontend (Vercel)
👉 https://ai-study-planner-agent.vercel.app

---

## 🎯 Key Features

✅ **AI-Powered Planning** - Personalized weekly schedules generated using Groq’s llama3-8b model.  
✅ **Beautiful UI** - Dark-themed interface focused on productivity and reduced distraction.  
✅ **Weekly Calendar** - Monday–Sunday calendar layout with structured time slots.  
✅ **Resource Curation** - YouTube, PDFs, FreeCodeCamp links    
✅ **Multi-Agent Architecture** - Planner Agent and Resource Agent working together for modular intelligence.
✅ **Production-Ready Setup** -Dockerized backend and Vercel-deployed frontend. 

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

## 🛠 Tech Stack

- **Frontend :** Vite, React, CSS  
- FastAPI, Python  
- **AI :** Groq (llama3-8b)  
- **Database :** PostgreSQL  
- **Orchestration :** Kestra  
- **Deployment :** Vercel, Docker


---


## Why Kestra?

Kestra is used as the workflow orchestration layer to coordinate
backend API calls, validate execution logic, and enable decision-based
agent behavior. This allows the AI Study Planner to scale from a simple
API into a production-ready, observable agent system with retries,
branching, and scheduling support.

---

## Author

**Anu Saha**

Engineering student and full-stack developer with a strong interest in
AI systems, workflow orchestration, and scalable backend architectures.


---

CodeRabbit review enabled.

---
