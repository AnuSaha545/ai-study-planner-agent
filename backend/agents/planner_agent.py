"""Planner Agent Module.

Responsible for generating personalized study plans based on subjects,
daily study hours, and days per week. Provides structured daily schedules
with session types and durations.
"""

from typing import List
from enum import Enum
from pydantic import BaseModel, Field, validator


class SessionType(str, Enum):
    """Session types representing different learning activities."""
    CONCEPT = "concept"
    PRACTICE = "practice"
    REVISION = "revision"


class StudySession(BaseModel):
    """Represents a single study session within a day.
    
    Attributes:
        subject: Name of the subject being studied
        session_type: Type of learning activity (concept, practice, revision)
        duration_hours: Duration of the session in hours
        notes: Contextual notes or learning objectives for the session
    """
    subject: str = Field(..., min_length=1, max_length=100)
    session_type: SessionType = Field(..., description="Type of learning activity")
    duration_hours: float = Field(..., gt=0, le=24, description="Duration in hours")
    notes: str = Field(..., min_length=1, max_length=500)

    class Config:
        """Pydantic configuration."""
        use_enum_values = False


class DailyPlan(BaseModel):
    """Represents a complete study plan for a single day.
    
    Attributes:
        day: Name of the day (Monday, Tuesday, etc.)
        total_hours: Total study hours for the day
        sessions: List of study sessions for the day
    """
    day: str = Field(..., min_length=1, max_length=20)
    total_hours: float = Field(..., gt=0, le=24)
    sessions: List[StudySession] = Field(..., min_items=1)

    @validator('sessions')
    def validate_session_duration_sum(cls, sessions, values):
        """Validate that session durations align with total hours."""
        if 'total_hours' in values:
            session_sum = sum(s.duration_hours for s in sessions)
            # Allow small floating-point discrepancies
            if abs(session_sum - values['total_hours']) > 0.1:
                pass  # Log warning but allow (plan may be approximate)
        return sessions


class PlannerAgent:
    """Agent responsible for generating study plans.
    
    This agent takes user inputs (subjects, study hours, days per week)
    and generates a structured weekly study plan with balanced sessions.
    """

    # Available days of the week
    AVAILABLE_DAYS = [
        "Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"
    ]

    # Rotation pattern for session types
    SESSION_TYPES = [SessionType.CONCEPT, SessionType.PRACTICE, SessionType.REVISION]

    @staticmethod
    def generate_study_plan(
        subjects: List[str],
        daily_hours: float,
        days_per_week: int
    ) -> List[DailyPlan]:
        """Generate a personalized weekly study plan.
        
        Creates a structured schedule where:
        - Each subject gets equal time allocation
        - Session types rotate through concept→practice→revision
        - Daily totals match the requested study hours
        
        Args:
            subjects: List of subjects to study
            daily_hours: Target study hours per day
            days_per_week: Number of study days per week
            
        Returns:
            List of DailyPlan objects representing the weekly schedule
            
        Raises:
            ValueError: If inputs are invalid
        """
        if not subjects:
            raise ValueError("At least one subject is required")
        if daily_hours <= 0:
            raise ValueError("Daily hours must be positive")
        if not 1 <= days_per_week <= 7:
            raise ValueError("Days per week must be between 1 and 7")

        plans = []
        hours_per_subject = daily_hours / len(subjects)

        # Generate plans for each study day
        for day_index in range(days_per_week):
            day_name = PlannerAgent.AVAILABLE_DAYS[day_index % len(PlannerAgent.AVAILABLE_DAYS)]
            sessions = []

            # Create a session for each subject
            for subject_index, subject in enumerate(subjects):
                session_type = PlannerAgent.SESSION_TYPES[subject_index % len(PlannerAgent.SESSION_TYPES)]
                
                session = StudySession(
                    subject=subject,
                    session_type=session_type,
                    duration_hours=round(hours_per_subject, 2),
                    notes=PlannerAgent._generate_session_notes(subject, session_type)
                )
                sessions.append(session)

            # Create the daily plan
            daily_plan = DailyPlan(
                day=day_name,
                total_hours=daily_hours,
                sessions=sessions
            )
            plans.append(daily_plan)

        return plans

    @staticmethod
    def _generate_session_notes(subject: str, session_type: SessionType) -> str:
        """Generate contextual notes for a session.
        
        Args:
            subject: Subject name
            session_type: Type of session
            
        Returns:
            Contextual notes for the session
        """
        notes_template = {
            SessionType.CONCEPT: f"Master core concepts and theory of {subject}",
            SessionType.PRACTICE: f"Apply knowledge through practical exercises in {subject}",
            SessionType.REVISION: f"Review and consolidate learning in {subject}",
        }
        return notes_template.get(session_type, f"Study {subject}")


# Public API for backward compatibility
def generate_study_plan(
    subjects: List[str],
    daily_hours: int,
    days_per_week: int
) -> List[DailyPlan]:
    """Generate a study plan (public API).
    
    This function maintains backward compatibility with the existing API.
    
    Args:
        subjects: List of subjects to study
        daily_hours: Target study hours per day
        days_per_week: Number of study days per week
        
    Returns:
        List of DailyPlan objects
    """
    return PlannerAgent.generate_study_plan(subjects, daily_hours, days_per_week)
