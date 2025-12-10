#!/usr/bin/env python
"""
AI Study Planner CLI Tool

A command-line interface to generate personalized study plans using the FastAPI backend.
Calls the /plan endpoint and displays formatted weekly study schedules.
"""

import argparse
import sys
from typing import List
import requests
import json
from urllib.parse import urljoin


class StudyPlannerCLI:
    """CLI tool for generating and displaying study plans."""

    def __init__(self, api_url: str = "http://localhost:8000"):
        """
        Initialize the CLI tool.

        Args:
            api_url: Base URL of the FastAPI backend (default: http://localhost:8000)
        """
        self.api_url = api_url
        self.plan_endpoint = urljoin(api_url, "/plan")

    def fetch_plan(self, subjects: List[str], hours: int, days_per_week: int) -> dict:
        """
        Fetch study plan from the FastAPI backend.

        Args:
            subjects: List of subjects to study
            hours: Daily study hours
            days_per_week: Number of days to study per week

        Returns:
            Study plan response as dictionary

        Raises:
            requests.RequestException: If API call fails
            ValueError: If response is invalid
        """
        payload = {
            "subjects": subjects,
            "hours": hours,
            "days_per_week": days_per_week,
        }

        try:
            response = requests.post(self.plan_endpoint, json=payload, timeout=30)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.ConnectionError:
            raise ConnectionError(
                f"❌ Cannot connect to API at {self.api_url}. "
                "Make sure the FastAPI backend is running with: uvicorn main:app --reload"
            )
        except requests.exceptions.Timeout:
            raise TimeoutError(
                "❌ API request timed out. The backend took too long to respond."
            )
        except requests.exceptions.HTTPError as e:
            if response.status_code == 422:
                raise ValueError(
                    f"❌ Invalid input: {response.json().get('detail', 'Check your parameters')}"
                )
            raise requests.RequestException(
                f"❌ API Error {response.status_code}: {response.text}"
            )

    def print_study_plan(self, plan_data: dict) -> None:
        """
        Pretty-print the study plan to the terminal.

        Args:
            plan_data: Study plan response from API
        """
        plan = plan_data.get("plan", [])
        resources = plan_data.get("resources", {})

        print("\n" + "=" * 80)
        print(" " * 20 + "📚 PERSONALIZED STUDY PLAN 📚")
        print("=" * 80 + "\n")

        # Display daily plans
        if plan:
            print("📅 WEEKLY SCHEDULE")
            print("-" * 80)

            for day_plan in plan:
                day = day_plan["day"]
                total_hours = day_plan["total_hours"]
                sessions = day_plan["sessions"]

                print(f"\n🔹 {day.upper()} ({total_hours} hours)")
                print("  " + "─" * 76)

                for i, session in enumerate(sessions, 1):
                    subject = session["subject"]
                    session_type = session["session_type"].upper()
                    duration = session["duration_hours"]
                    notes = session["notes"]

                    print(f"  {i}. {subject}")
                    print(f"     Type: {session_type} | Duration: {duration}h")
                    print(f"     📝 {notes}")

        # Display learning resources
        if resources:
            print("\n\n" + "=" * 80)
            print("🔗 LEARNING RESOURCES")
            print("-" * 80)

            for subject, resource_links in resources.items():
                print(f"\n📖 {subject.upper()}")
                print(f"  • YouTube: {resource_links['youtube_search']}")
                print(f"  • PDFs: {resource_links['pdf_search']}")
                print(f"  • FreeCodeCamp: {resource_links['freecodecamp']}")

        print("\n" + "=" * 80 + "\n")
        print("✅ Study plan generated successfully!")
        print("💡 Tip: Save this output with the -o flag for future reference.\n")

    def run(self) -> None:
        """Execute the CLI with parsed arguments."""
        parser = self._create_parser()
        args = parser.parse_args()

        try:
            # Validate subjects
            subjects = [s.strip() for s in args.subjects.split(",") if s.strip()]
            if not subjects:
                parser.error("At least one subject is required")

            print(f"📋 Fetching study plan for: {', '.join(subjects)}")
            print(f"   Daily hours: {args.hours} | Days/week: {args.days}\n")

            # Fetch plan from API
            plan_data = self.fetch_plan(subjects, args.hours, args.days)

            # Print formatted plan
            self.print_study_plan(plan_data)

            # Optionally save to file
            if args.output:
                self._save_to_file(plan_data, args.output)

        except (ConnectionError, TimeoutError, ValueError) as e:
            print(f"\n{str(e)}\n")
            sys.exit(1)
        except Exception as e:
            print(f"\n❌ Unexpected error: {str(e)}\n")
            sys.exit(1)

    def _create_parser(self) -> argparse.ArgumentParser:
        """Create and configure argument parser."""
        parser = argparse.ArgumentParser(
            prog="python cli.py",
            description="Generate personalized study plans using AI Study Planner Agent",
            formatter_class=argparse.RawDescriptionHelpFormatter,
            epilog="""
Examples:
  python cli.py -s "Mathematics, Physics" --hours 3 --days 6
  python cli.py -s "Python, JavaScript, React" --hours 2 --days 5 -o study_plan.json
  python cli.py --subjects "Biology" --hours 4 --api-url http://localhost:8000
            """,
        )

        parser.add_argument(
            "-s",
            "--subjects",
            required=True,
            help="Comma-separated list of subjects (required)",
            metavar="SUBJECTS",
        )
        parser.add_argument(
            "--hours",
            type=int,
            default=3,
            help="Daily study hours (default: 3)",
            metavar="HOURS",
        )
        parser.add_argument(
            "--days",
            type=int,
            default=6,
            help="Days per week to study (default: 6)",
            metavar="DAYS",
        )
        parser.add_argument(
            "-o",
            "--output",
            help="Save plan as JSON to file (optional)",
            metavar="FILE",
        )
        parser.add_argument(
            "--api-url",
            default="http://localhost:8000",
            help="FastAPI backend URL (default: http://localhost:8000)",
            metavar="URL",
        )
        parser.add_argument(
            "-v",
            "--version",
            action="version",
            version="AI Study Planner CLI v1.0",
        )

        return parser

    @staticmethod
    def _save_to_file(plan_data: dict, filepath: str) -> None:
        """
        Save study plan to a JSON file.

        Args:
            plan_data: Study plan response
            filepath: Path to save the file
        """
        try:
            with open(filepath, "w") as f:
                json.dump(plan_data, f, indent=2)
            print(f"💾 Plan saved to: {filepath}")
        except IOError as e:
            print(f"⚠️  Warning: Could not save to {filepath}: {str(e)}")


def main():
    """Entry point for the CLI."""
    cli = StudyPlannerCLI()
    cli.run()


if __name__ == "__main__":
    main()
