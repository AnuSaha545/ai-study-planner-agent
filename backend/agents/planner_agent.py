from typing import List
from pydantic import BaseModel


class StudySession(BaseModel):
    subject: str
    session_type: str
    duration_hours: float
    notes: str


class DailyPlan(BaseModel):
    day: str
    total_hours: float
    sessions: List[StudySession]


DAYS = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday"]


def generate_study_plan(
    subjects: List[str],
    daily_hours: int,
    days_per_week: int
) -> List[DailyPlan]:

    plans = []
    hours_each = daily_hours / len(subjects)

    for i in range(days_per_week):
        sessions = []

        for j, subject in enumerate(subjects):
            sessions.append(
                StudySession(
                    subject=subject,
                    session_type=["concept", "practice", "revision"][j % 3],
                    duration_hours=round(hours_each, 2),
                    notes=f"Focus on key topics of {subject}"
                )
            )

        plans.append(
            DailyPlan(
                day=DAYS[i % len(DAYS)],
                total_hours=daily_hours,
                sessions=sessions
            )
        )

    return plans
