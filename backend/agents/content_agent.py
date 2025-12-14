"""Content Agent Module.

Uses GroqCloud (via backend.services.ai_client.AIClient) to generate
*structured* learning content per subject:
- Core concepts/topics (ordered)
- Practice tasks / problem types

The output is designed to be distributed across the timetable sessions
created by PlannerAgent.
"""

from __future__ import annotations

from typing import Dict, List

from pydantic import BaseModel, Field

from services.ai_client import AIClient


class SubjectOutline(BaseModel):
    """AI-generated outline for a subject."""

    subject: str = Field(..., min_length=1, max_length=100)
    concepts: List[str] = Field(default_factory=list, max_length=60)
    practice_tasks: List[str] = Field(default_factory=list, max_length=60)


class ContentAgent:
    """Generates structured study content using Groq."""

    def __init__(self, ai_client: AIClient | None = None) -> None:
        self.ai = ai_client or AIClient()

    def generate_outline(self, subject: str) -> SubjectOutline:
        """Generate a concept/practice outline for a single subject."""

        prompt = f"""
You are generating a weekly study plan outline for the subject: "{subject}".

Return STRICT VALID JSON ONLY (no markdown, no commentary) with this schema:
{{
  "subject": string,
  "concepts": string[],
  "practice_tasks": string[]
}}

Rules:
- concepts: 12-20 items, ordered from beginner -> advanced, each item short.
- practice_tasks: 12-20 items, each is a concrete task/problem type.
- Avoid URLs.
- Keep each string <= 80 characters.
""".strip()

        raw = self.ai.generate_text(prompt)
        return SubjectOutline.model_validate_json(raw)

    def generate_outlines(self, subjects: List[str]) -> Dict[str, SubjectOutline]:
        """Generate outlines for multiple subjects."""

        outlines: Dict[str, SubjectOutline] = {}
        for s in subjects:
            ss = (s or "").strip()
            if not ss:
                continue
            outlines[ss] = self.generate_outline(ss)
        return outlines
