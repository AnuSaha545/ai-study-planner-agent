"""AI Study Planner Backend API.

FastAPI application providing endpoints for generating personalized
study plans using multi-agent orchestration.
"""

import logging
from typing import Dict, List

from fastapi import FastAPI, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field

from agents.planner_agent import DailyPlan
from agents.resource_agent import SubjectResources
from workflows.agent_workflow import run_workflow

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)


class StudyPlanRequest(BaseModel):
    """Request model for study plan generation.
    
    Attributes:
        subjects: List of subjects to create a plan for
        hours: Daily study hours (must be positive)
        days_per_week: Number of days per week to study (default: 6)
    """
    subjects: List[str] = Field(
        ...,
        min_items=1,
        max_items=8,
        description="Subjects to study (1-8 subjects)"
    )
    hours: float = Field(
        ...,
        gt=0,
        le=12,
        description="Daily study hours (0.5-12)"
    )
    days_per_week: int = Field(
        default=6,
        ge=1,
        le=7,
        description="Days per week to study (1-7)"
    )

    class Config:
        """Pydantic configuration."""
        schema_extra = {
            "example": {
                "subjects": ["Python", "Data Structures", "Web Development"],
                "hours": 3,
                "days_per_week": 6
            }
        }


class StudyPlanResponse(BaseModel):
    """Response model for study plan generation.
    
    Attributes:
        plan: List of daily study plans
        resources: Dictionary of curated resources per subject
    """
    plan: List[DailyPlan]
    resources: Dict[str, SubjectResources]

    class Config:
        """Pydantic configuration."""
        schema_extra = {
            "description": "Complete study plan with personalized schedule and resources"
        }


class HealthResponse(BaseModel):
    """Response model for health check endpoint.
    
    Attributes:
        status: Health status ("ok" or "error")
        version: API version
    """
    status: str
    version: str = "1.0.0"


# Initialize FastAPI application
app = FastAPI(
    title="AI Study Planner Agent Backend",
    description="Multi-agent orchestrated study planning service",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Configure for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get(
    "/health",
    response_model=HealthResponse,
    tags=["Health"],
    summary="Health check endpoint",
    description="Verify the API is running and healthy"
)
def health() -> HealthResponse:
    """Check API health status.
    
    Returns:
        HealthResponse with status and version
    """
    logger.info("Health check requested")
    return HealthResponse(status="ok")


@app.post(
    "/plan",
    response_model=StudyPlanResponse,
    status_code=status.HTTP_200_OK,
    tags=["Study Planning"],
    summary="Generate personalized study plan",
    description="Creates a personalized weekly study plan with curated resources",
    responses={
        200: {"description": "Study plan generated successfully"},
        422: {"description": "Invalid input parameters"},
        500: {"description": "Server error during plan generation"},
    }
)
def create_plan(request: StudyPlanRequest) -> StudyPlanResponse:
    """Generate a personalized study plan.
    
    Orchestrates multiple agents to create:
    1. A personalized weekly study schedule
    2. Curated learning resources for each subject
    
    Args:
        request: Study plan request with subjects and hours
        
    Returns:
        StudyPlanResponse with complete plan and resources
        
    Raises:
        HTTPException: If plan generation fails
    """
    logger.info(
        f"Study plan request received: subjects={request.subjects}, "
        f"hours={request.hours}, days={request.days_per_week}"
    )

    try:
        # Execute workflow
        result = run_workflow(
            subjects=request.subjects,
            daily_hours=request.hours,
            days_per_week=request.days_per_week
        )

        logger.info("Study plan generated successfully")
        return StudyPlanResponse(**result)

    except ValueError as e:
        logger.warning(f"Validation error: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=f"Invalid input: {str(e)}"
        )
    except RuntimeError as e:
        logger.error(f"Workflow error: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to generate study plan"
        )
    except Exception as e:
        logger.exception(f"Unexpected error: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An unexpected error occurred"
        )


@app.on_event("startup")
async def startup_event():
    """Log application startup."""
    logger.info("AI Study Planner Backend Starting")
    logger.info("FastAPI Docs available at: /docs")


@app.on_event("shutdown")
async def shutdown_event():
    """Log application shutdown."""
    logger.info("AI Study Planner Backend Shutting Down")
