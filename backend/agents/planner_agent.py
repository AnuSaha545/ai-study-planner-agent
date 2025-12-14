from typing import List
from enum import Enum
from pydantic import BaseModel, Field
import math
import itertools


class SessionType(str, Enum):
    CONCEPT = "concept"
    PRACTICE = "practice"
    REVISION = "revision"


class StudySession(BaseModel):
    subject: str
    session_type: SessionType
    duration_hours: float
    notes: str


class DailyPlan(BaseModel):
    day: str
    total_hours: float
    sessions: List[StudySession]


class PlannerAgent:
    DAYS = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]

    @staticmethod
    def generate_study_plan(
        subjects: List[str],
        daily_hours: float,
        days_per_week: int
    ) -> List[DailyPlan]:

        if not subjects:
            raise ValueError("Subjects required")

        total_hours = daily_hours * days_per_week
        hours_per_subject = total_hours / len(subjects)
        # Determine how many 1-hour blocks each subject should approximately receive
        blocks_per_subject = {
            s: max(1, int(round(hours_per_subject))) for s in subjects
        }

        # Track how many times a subject has been scheduled so far
        subject_scheduled_counts = {s: 0 for s in subjects}

        # Create a rotating subject iterator biased by blocks_per_subject
        subject_pool = []
        for s, count in blocks_per_subject.items():
            subject_pool.extend([s] * count)

        # If pool is empty for any reason, fallback to subjects list
        if not subject_pool:
            subject_pool = list(subjects)

        subject_cycle = itertools.cycle(subject_pool)

        plans: List[DailyPlan] = []

        # Helper to pick a session type & note based on per-subject progress
        def subject_progress_session(subject: str, occurrence_index: int, total_occurrences: int, day_progress: float):
            # Calculate fraction of progress for this subject across its scheduled occurrences
            denom = max(total_occurrences - 1, 1)
            frac = occurrence_index / denom if denom > 0 else 0.0

            # Blend overall day progress and per-subject fraction to decide phase
            combined = (frac * 0.7) + (day_progress * 0.3)

            if combined < 0.35:
                st = SessionType.CONCEPT
                note = (
                    f"Foundations for {subject}: focus on core concepts, terminology and basic syntax."
                )
            elif combined < 0.75:
                st = SessionType.PRACTICE
                note = (
                    f"Practice & implement: write small programs, exercises and strengthen syntax usage for {subject}."
                )
            else:
                st = SessionType.REVISION
                note = (
                    f"Deepen & review: consolidate knowledge, tackle integrated projects and revise tricky topics in {subject}."
                )

            return st, note

        # Pre-calc expected total occurrences for each subject across the week
        # We'll approximate by distributing total_hours proportionally in 1-hour blocks
        approx_total_blocks = {}
        for s in subjects:
            # total blocks = proportion * total_hours rounded to nearest int (at least 1)
            proportion = 1 / len(subjects)
            approx_blocks = max(1, int(round(proportion * total_hours)))
            approx_total_blocks[s] = approx_blocks

        # Build week schedule
        for day_index in range(days_per_week):
            day_name = PlannerAgent.DAYS[day_index]
            sessions: List[StudySession] = []
            remaining_hours = daily_hours

            while remaining_hours > 0:
                block = 1.0 if remaining_hours >= 1 else remaining_hours
                subject = next(subject_cycle)

                # occurrence index for this subject (0-based)
                occ_idx = subject_scheduled_counts.get(subject, 0)
                total_occ = approx_total_blocks.get(subject, 1)

                # Day-level progress (0 early -> 1 late)
                day_progress = day_index / max(days_per_week - 1, 1)

                session_type, notes = subject_progress_session(subject, occ_idx, total_occ, day_progress)

                sessions.append(
                    StudySession(
                        subject=subject,
                        session_type=session_type,
                        duration_hours=block,
                        notes=notes,
                    )
                )

                # increment scheduled count for the subject
                subject_scheduled_counts[subject] = occ_idx + 1
                remaining_hours -= block

            plans.append(
                DailyPlan(day=day_name, total_hours=daily_hours, sessions=sessions)
            )

        return plans
