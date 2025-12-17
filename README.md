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


## 🐇 Why CodeRabbit?

CodeRabbit is integrated to provide **AI-powered code review** during development.

It helps maintain clean, readable, and consistent code by automatically reviewing pull requests, identifying potential issues, 
and suggesting improvements. CodeRabbit acts as an additional quality layer, 
supporting best practices and long-term maintainability of the codebase.

---


## 🛠️ Why Cline?

Cline is used as an **AI development assistant** to improve developer productivity during implementation.

It assists with debugging, refactoring, architectural exploration, and feature development while keeping the developer fully in control. 
Cline accelerates development without replacing engineering judgment, making it a valuable productivity tool rather than an automated solution.

---


## 🚀 Why Vercel?

Vercel is used to deploy and host the frontend application.

It provides seamless GitHub integration, optimized builds for modern frontend frameworks,
automatic deployments on each commit, and fast global content delivery. 
Vercel ensures the frontend is production-ready, reliable, and easy to maintain with minimal configuration.

---


## Why Kestra?

Kestra is used as the workflow orchestration layer to coordinate
backend API calls, validate execution logic, and enable decision-based
agent behavior. This allows the AI Study Planner to scale from a simple
API into a production-ready, observable agent system with retries,
branching, and scheduling support.

---

## ⚠️ Backend Availability Note

The frontend of this project is deployed on Vercel and is publicly accessible.

The backend (FastAPI and AI planning logic) is currently designed to run locally or via Docker 
and is not deployed to a public cloud environment yet. As a result, AI-powered features require the backend service to be running.

This setup reflects a common development-stage architecture and allows the system 
to be easily extended by deploying the backend to platforms such as Render, Railway, or a VPS in the future.

---

## Author

**Anu Saha**

Engineering student and full-stack developer with a strong interest in
AI systems, workflow orchestration, and scalable backend architectures.

GitHub: https://github.com/AnuSaha545


---

CodeRabbit review enabled.

