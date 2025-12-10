from agents.planner_agent import generate_study_plan
from agents.resource_agent import generate_resources


def run_workflow(subjects, daily_hours, days_per_week):

    plan = generate_study_plan(
        subjects=subjects,
        daily_hours=daily_hours,
        days_per_week=days_per_week
    )

    resources = generate_resources(subjects)

    return {
        "plan": plan,
        "resources": resources,
    }
