# AI Study Planner Agent

A workflow-orchestrated multi-agent system that generates personalized
study plans and curated learning resources based on user inputs.

## Features

- Multi-Agent architecture (Planner Agent & Resource Agent)
- Workflow orchestration
- FastAPI backend
- React + Vite frontend
- Command-line interface for quick access
- Modular clean codebase

## Architecture Overview

User → React UI → FastAPI → Workflow Orchestrator → Agents → Response → UI

## Quick Start

### Prerequisites

- Python 3.8+
- pip (Python package manager)

### Backend Setup

1. **Install dependencies:**
   ```bash
   cd backend
   pip install fastapi uvicorn requests pydantic
   ```

2. **Run the FastAPI server:**
   ```bash
   uvicorn main:app --reload
   ```
   The API will be available at `http://localhost:8000`

### Using the CLI Tool

The CLI tool provides a convenient way to generate study plans from the command line.

#### Basic Usage

```bash
python cli.py --subjects "Mathematics, Physics" --hours 3 --days 6
```

#### Command-Line Arguments

- `--subjects` / `-s` (required): Comma-separated list of subjects
- `--hours` (optional): Daily study hours (default: 3)
- `--days` (optional): Days per week to study (default: 6)
- `--output` / `-o` (optional): Save plan as JSON file
- `--api-url` (optional): FastAPI backend URL (default: http://localhost:8000)

#### Examples

**Generate a study plan for multiple subjects:**
```bash
python cli.py -s "Python, JavaScript, React" --hours 2 --days 5
```

**Generate and save the plan to a file:**
```bash
python cli.py -s "Mathematics, Physics, Chemistry" --hours 4 --days 6 -o my_study_plan.json
```

**Use custom API endpoint:**
```bash
python cli.py -s "Biology" --api-url http://192.168.1.100:8000
```

#### Output Format

The CLI displays a beautifully formatted study plan with:
- 📅 **Weekly Schedule**: Day-by-day breakdown with session types and durations
- 📝 **Study Notes**: Specific focus areas for each session
- 🔗 **Learning Resources**: YouTube, PDF, and FreeCodeCamp links for each subject

#### Error Handling

The CLI gracefully handles:
- ✅ Connection failures (if backend is not running)
- ✅ Request timeouts
- ✅ Invalid input validation
- ✅ API errors with clear error messages

## CodeRabbit Integration

This repository uses **CodeRabbit** for automated pull-request reviews,
documentation checks, and code-quality improvement as part of open-source
best practices.

_Small edit to trigger CodeRabbit review._
