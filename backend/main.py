from typing import List, Dict
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field

from agents.planner_agent import DailyPlan
from agents.resource_agent import SubjectResources
from workflows.agent_workflow import run_workflow


class StudyPlanRequest(BaseModel):
    subjects: List[str] = Field(..., min_items=1)
    hours: int = Field(..., gt=0)
    days_per_week: int = Field(default=6, gt=0)


class StudyPlanResponse(BaseModel):
    plan: List[DailyPlan]
    resources: Dict[str, SubjectResources]


app = FastAPI(
    title="AI Study Planner Agent Backend",
    version="1.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_headers=["*"],
    allow_methods=["*"],
)


@app.get("/health")
def health():
    return {"status": "ok"}


@app.post("/plan", response_model=StudyPlanResponse)
def create_plan(request: StudyPlanRequest):

    output = run_workflow(
        subjects=request.subjects,
        daily_hours=request.hours,
        days_per_week=request.days_per_week
    )

    return output
