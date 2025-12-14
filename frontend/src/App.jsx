import { useState, useCallback } from "react";
import WeeklyPlanner from "./components/WeeklyPlanner";
import "./App.css";

// Constants
const BACKEND_URL = import.meta.env.VITE_API_URL || "http://localhost:8000";
const INITIAL_SUBJECTS = "Python, Data Structures";
const INITIAL_HOURS = 3;
const INITIAL_DAYS = 6;

/**
 * Main App Component
 * Manages study plan generation and displays weekly schedule with resources
 */
export default function App() {
  // State Management
  const [subjects, setSubjects] = useState(INITIAL_SUBJECTS);
  const [hours, setHours] = useState(INITIAL_HOURS);
  const [daysPerWeek, setDaysPerWeek] = useState(INITIAL_DAYS);
  const [data, setData] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");
  const [success, setSuccess] = useState(false);

  /**
   * Validates user inputs for study plan generation
   * @returns {Object|null} Validated inputs or null if invalid
   */
  const validateInputs = useCallback(() => {
    // Parse and validate subjects
    const subjectList = subjects
      .split(",")
      .map((s) => s.trim())
      .filter(Boolean);

    if (subjectList.length === 0) {
      setError("Please enter at least one subject");
      return null;
    }

    if (subjectList.length > 8) {
      setError("Maximum 8 subjects allowed");
      return null;
    }

    // Validate daily study hours
    const hoursNum = Number(hours);
    if (isNaN(hoursNum) || hoursNum < 0.5 || hoursNum > 12) {
      setError("Daily hours must be between 0.5 and 12");
      return null;
    }

    // Validate days per week
    const daysNum = Number(daysPerWeek);
    if (isNaN(daysNum) || daysNum < 1 || daysNum > 7) {
      setError("Days per week must be between 1 and 7");
      return null;
    }

    return { subjectList, hoursNum, daysNum };
  }, [subjects, hours, daysPerWeek]);

  /**
   * Handles study plan generation via API call
   */
  const handleGenerate = useCallback(async () => {
    const validated = validateInputs();
    if (!validated) return;

    setLoading(true);
    setError("");
    setSuccess(false);
    setData(null);

    try {
      const response = await fetch(`${BACKEND_URL}/plan`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          subjects: validated.subjectList,
          hours: validated.hoursNum,
          days_per_week: validated.daysNum,
        }),
      });

      if (!response.ok) {
        const errorData = await response.json();
        throw new Error(
          errorData.detail || "Failed to generate study plan"
        );
      }

      const planData = await response.json();
      setData(planData);
      setSuccess(true);
      
      // Auto-hide success message after 4 seconds
      setTimeout(() => setSuccess(false), 4000);
    } catch (err) {
      console.error("Study plan generation error:", err);
      setError(`❌ ${err.message || "An unexpected error occurred"}`);
    } finally {
      setLoading(false);
    }
  }, [validateInputs]);

  /**
   * Exports the generated study plan as JSON file
   */
  const handleExportJSON = useCallback(() => {
    if (!data) {
      setError("No data to export");
      return;
    }

    try {
      const jsonString = JSON.stringify(data, null, 2);
      const blob = new Blob([jsonString], { type: "application/json" });
      const url = URL.createObjectURL(blob);
      const link = document.createElement("a");
      
      link.href = url;
      link.download = `study-plan-${new Date().toISOString().split("T")[0]}.json`;
      link.click();
      
      URL.revokeObjectURL(url);
    } catch (err) {
      console.error("Export error:", err);
      setError("Failed to export plan");
    }
  }, [data]);

  return (
    <div className="app-container">
      {/* Navigation Bar */}
      <nav className="navbar">
        <div className="navbar-content">
          <div className="navbar-brand">
            <span className="logo-icon">📚</span>
            <h1 className="logo-text">AI Study Planner</h1>
          </div>
          <div className="navbar-links">
            <a href="#features" className="nav-link">
              Features
            </a>
            <a href="#about" className="nav-link">
              About
            </a>
          </div>
        </div>
      </nav>

      <main className="app">
        {/* Hero Section */}
        <section className="hero">
          <div className="hero-content">
            <h2 className="hero-title">✨ Create Your Perfect Study Plan</h2>
            <p className="hero-subtitle">
              Powered by AI • Personalized for you • Intelligent scheduling
            </p>
          </div>
        </section>

        {/* Input Section */}
        <section className="input-section">
          <div className="input-card">
            <h2 className="input-title">📋 Plan Generator</h2>
            <p className="input-description">
              Enter your subjects and study preferences
            </p>

            {/* Subjects Input */}
            <div className="form-group">
              <label className="form-label" htmlFor="subjects-input">
                Subjects to Study
              </label>
              <input
                id="subjects-input"
                className="form-input"
                type="text"
                value={subjects}
                onChange={(e) => setSubjects(e.target.value)}
                placeholder="e.g., Python, Data Structures, Web Development"
                aria-label="Subjects to study"
              />
              <span className="form-hint">Separate multiple subjects with commas</span>
            </div>

            {/* Hours and Days Input */}
            <div className="form-row">
              <div className="form-group">
                <label className="form-label" htmlFor="hours-input">
                  Daily Study Hours
                </label>
                <input
                  id="hours-input"
                  className="form-input"
                  type="number"
                  min="0.5"
                  max="12"
                  step="0.5"
                  value={hours}
                  onChange={(e) => setHours(e.target.value)}
                  aria-label="Daily study hours"
                />
                <span className="form-hint">0.5 - 12 hours</span>
              </div>
              <div className="form-group">
                <label className="form-label" htmlFor="days-input">
                  Days Per Week
                </label>
                <input
                  id="days-input"
                  className="form-input"
                  type="number"
                  min="1"
                  max="7"
                  value={daysPerWeek}
                  onChange={(e) => setDaysPerWeek(e.target.value)}
                  aria-label="Days per week"
                />
                <span className="form-hint">1 - 7 days</span>
              </div>
            </div>

            {/* Error Alert */}
            {error && (
              <div className="alert alert-error" role="alert">
                <span className="alert-icon" aria-hidden="true">⚠️</span>
                <span>{error}</span>
              </div>
            )}

            {/* Success Alert */}
            {success && (
              <div className="alert alert-success" role="status">
                <span className="alert-icon" aria-hidden="true">✅</span>
                <span>Study plan generated successfully!</span>
              </div>
            )}

            {/* Generate Button */}
            <button
              className="btn btn-primary btn-large"
              onClick={handleGenerate}
              disabled={loading}
              aria-busy={loading}
              aria-label="Generate study plan"
            >
              {loading ? (
                <>
                  <span className="spinner" aria-hidden="true"></span>
                  Generating Plan...
                </>
              ) : (
                <>🚀 Generate Study Plan</>
              )}
            </button>
          </div>
        </section>

        {/* Results Section */}
        {data && (
          <section className="results-section">
            {/* Export Controls */}
            <div className="export-controls">
              <button
                className="btn btn-secondary"
                onClick={handleExportJSON}
                aria-label="Export study plan as JSON"
              >
                📥 Export as JSON
              </button>
            </div>

            {/* Weekly Study Plan Component */}
            <WeeklyPlanner plan={data.plan} />

            {/* Learning Resources Section */}
            <section className="resources-section" aria-label="Learning resources">
              <div className="section-header">
                <h2 className="section-title">🔗 Learning Resources</h2>
                <p className="section-description">Curated resources for each subject</p>
              </div>

              <div className="resources-grid">
                {Object.entries(data.resources).map(([subject, links]) => (
                  <div key={subject} className="resource-card">
                    <h3 className="resource-title">{subject}</h3>
                    <div className="resource-links">
                      <a
                        href={links.youtube_search}
                        target="_blank"
                        rel="noopener noreferrer"
                        className="resource-link"
                        aria-label={`YouTube courses for ${subject}`}
                      >
                        <span className="resource-icon" aria-hidden="true">▶️</span>
                        <span>YouTube Courses</span>
                      </a>
                      <a
                        href={links.pdf_search}
                        target="_blank"
                        rel="noopener noreferrer"
                        className="resource-link"
                        aria-label={`PDF notes for ${subject}`}
                      >
                        <span className="resource-icon" aria-hidden="true">📄</span>
                        <span>PDF Notes</span>
                      </a>
                      <a
                        href={links.freecodecamp}
                        target="_blank"
                        rel="noopener noreferrer"
                        className="resource-link"
                        aria-label={`FreeCodeCamp course for ${subject}`}
                      >
                        <span className="resource-icon" aria-hidden="true">💻</span>
                        <span>FreeCodeCamp</span>
                      </a>
                    </div>
                  </div>
                ))}
              </div>
            </section>
          </section>
        )}
      </main>

      {/* Footer */}
      <footer className="footer">
        <div className="footer-content">
          <p className="footer-copyright">
            © 2025 AI Study Planner. All rights reserved.
          </p>
        </div>
      </footer>
    </div>
  );
}
