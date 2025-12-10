"""Agent Workflow Orchestration Module.

Orchestrates the execution of multiple agents to generate comprehensive
study plans with accompanying resources. Handles agent coordination,
error handling, and result aggregation.
"""

from typing import Dict, List, Any
import logging

from agents.planner_agent import PlannerAgent, DailyPlan
from agents.resource_agent import ResourceAgent, SubjectResources

# Configure logging
logger = logging.getLogger(__name__)


class AgentOrchestrator:
    """Orchestrates multi-agent workflow execution.
    
    Coordinates the planner and resource agents to generate comprehensive
    study plans with curated learning resources.
    """

    @staticmethod
    def run_workflow(
        subjects: List[str],
        daily_hours: float,
        days_per_week: int
    ) -> Dict[str, Any]:
        """Execute the complete study planning workflow.
        
        This orchestrator:
        1. Validates input parameters
        2. Executes the planner agent to generate study schedule
        3. Executes the resource agent to curate learning materials
        4. Aggregates results and returns comprehensive plan
        
        Args:
            subjects: List of subjects to plan for
            daily_hours: Target study hours per day
            days_per_week: Number of days to study per week
            
        Returns:
            Dictionary containing plan and resources
            
        Raises:
            ValueError: If input validation fails
            RuntimeError: If workflow execution fails
        """
        # Validate inputs
        AgentOrchestrator._validate_inputs(subjects, daily_hours, days_per_week)

        logger.info(
            f"Starting workflow: subjects={subjects}, "
            f"daily_hours={daily_hours}, days_per_week={days_per_week}"
        )

        try:
            # Execute planner agent
            logger.debug("Executing Planner Agent...")
            study_plan = PlannerAgent.generate_study_plan(
                subjects=subjects,
                daily_hours=daily_hours,
                days_per_week=days_per_week
            )
            logger.debug(f"Planner Agent completed: {len(study_plan)} days generated")

            # Execute resource agent
            logger.debug("Executing Resource Agent...")
            resources = ResourceAgent.generate_resources(subjects=subjects)
            logger.debug(f"Resource Agent completed: {len(resources)} subjects processed")

            # Aggregate results
            result = {
                "plan": study_plan,
                "resources": resources,
            }

            logger.info("Workflow completed successfully")
            return result

        except ValueError as e:
            logger.error(f"Validation error in workflow: {str(e)}")
            raise RuntimeError(f"Workflow validation failed: {str(e)}") from e
        except Exception as e:
            logger.error(f"Unexpected error in workflow: {str(e)}", exc_info=True)
            raise RuntimeError(f"Workflow execution failed: {str(e)}") from e

    @staticmethod
    def _validate_inputs(
        subjects: List[str],
        daily_hours: float,
        days_per_week: int
    ) -> None:
        """Validate workflow input parameters.
        
        Args:
            subjects: List of subjects
            daily_hours: Daily study hours
            days_per_week: Days per week to study
            
        Raises:
            ValueError: If any parameter is invalid
        """
        if not subjects or not isinstance(subjects, list):
            raise ValueError("Subjects must be a non-empty list")

        if not all(isinstance(s, str) and len(s.strip()) > 0 for s in subjects):
            raise ValueError("All subjects must be non-empty strings")

        if not isinstance(daily_hours, (int, float)) or daily_hours <= 0:
            raise ValueError("Daily hours must be a positive number")

        if not isinstance(days_per_week, int) or not (1 <= days_per_week <= 7):
            raise ValueError("Days per week must be an integer between 1 and 7")


# Public API for backward compatibility
def run_workflow(
    subjects: List[str],
    daily_hours: float,
    days_per_week: int
) -> Dict[str, Any]:
    """Execute the study planning workflow (public API).
    
    This function maintains backward compatibility with the existing API.
    
    Args:
        subjects: List of subjects
        daily_hours: Daily study hours
        days_per_week: Days per week
        
    Returns:
        Dictionary with plan and resources
    """
    return AgentOrchestrator.run_workflow(
        subjects=subjects,
        daily_hours=daily_hours,
        days_per_week=days_per_week
    )
