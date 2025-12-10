import { useState } from "react";
import "./App.css";

const API_BASE_URL = "http://127.0.0.1:8000";

export default function App() {
  const [subjects, setSubjects] = useState("Python, DSA");
  const [hours, setHours] = useState(3);
  const [daysPerWeek, setDaysPerWeek] = useState(6);
  const [data, setData] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");
  const [success, setSuccess] = useState(false);

  const validateInputs = () => {
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

    const hoursNum = Number(hours);
    if (hoursNum < 0.5 || hoursNum > 12) {
      setError("Daily hours must be between 0.5 and 12");
      return null;
    }

    const daysNum = Number(daysPerWeek);
    if (daysNum < 1 || daysNum > 7) {
      setError("Days per week must be between 1 and 7");
      return null;
    }

    return { subjectList, hoursNum, daysNum };
  };

  const handleGenerate = async () => {
    const validated = validateInputs();
    if (!validated) return;

    setLoading(true);
    setError("");
    setSuccess(false);
    setData(null);

    try {
      const res = await fetch(`${API_BASE_URL}/plan`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json"
        },
        body: JSON.stringify({
          subjects: validated.subjectList,
          hours: validated.hoursNum,
          days_per_week: validated.daysNum
        })
      });

      if (!res.ok) {
        throw new Error(
          res.status === 422
            ? "Invalid input parameters"
            : `Server error: ${res.status}`
        );
      }

      const json = await res.json();
      setData(json);
      setSuccess(true);
      setTimeout(() => setSuccess(false), 5000);
    } catch (err) {
      console.error(err);
      setError(
        err.message.includes("Failed to fetch")
          ? "❌ Backend unreachable. Start the server with: uvicorn main:app --reload"
          : `❌ ${err.message}`
      );
    } finally {
      setLoading(false);
    }
  };

  const handleExportJSON = () => {
    if (!data) return;
    const json = JSON.stringify(data, null, 2);
    const blob = new Blob([json], { type: "application/json" });
    const url = URL.createObjectURL(blob);
    const a = document.createElement("a");
    a.href = url;
    a.download = `study-plan-${new Date().toISOString().split('T')[0]}.json`;
    a.click();
    URL.revokeObjectURL(url);
  };

  return (
    <div className="app-container">
      {/* Navigation Bar */}
      <nav className="navbar">
        <div className="navbar-content">
          <div className="navbar-brand">
            <span className="logo-icon">📚</span>
            <span className="logo-text">AI Study Planner</span>
          </div>
          <div className="navbar-links">
            <a href="#features" className="nav-link">Features</a>
            <a href="#about" className="nav-link">About</a>
          </div>
        </div>
      </nav>

      <main className="app">
        {/* Hero Section */}
        <section className="hero">
          <div className="hero-content">
            <h1 className="hero-title">Create Your Perfect Study Plan</h1>
            <p className="hero-subtitle">
              Powered by AI. Personalized for you. Multi-agent orchestrated workflows.
            </p>
          </div>
        </section>

        {/* Input Section */}
        <section className="input-section">
          <div className="input-card">
            <h2 className="input-title">Plan Generator</h2>
            <p className="input-description">Enter your subjects and study preferences</p>

            <div className="form-group">
              <label className="form-label">Subjects to Study</label>
              <input
                className="form-input"
                value={subjects}
                onChange={(e) => setSubjects(e.target.value)}
                placeholder="e.g., Python, Data Structures, Web Development"
                type="text"
              />
              <span className="form-hint">Separate multiple subjects with commas</span>
            </div>

            <div className="form-row">
              <div className="form-group">
                <label className="form-label">Daily Study Hours</label>
                <input
                  className="form-input"
                  type="number"
                  min="0.5"
                  max="12"
                  step="0.5"
                  value={hours}
                  onChange={(e) => setHours(e.target.value)}
                />
                <span className="form-hint">0.5 - 12 hours</span>
              </div>
              <div className="form-group">
                <label className="form-label">Days Per Week</label>
                <input
                  className="form-input"
                  type="number"
                  min="1"
                  max="7"
                  value={daysPerWeek}
                  onChange={(e) => setDaysPerWeek(e.target.value)}
                />
                <span className="form-hint">1 - 7 days</span>
              </div>
            </div>

            {error && (
              <div className="alert alert-error">
                <span className="alert-icon">⚠️</span>
                <span>{error}</span>
              </div>
            )}

            {success && (
              <div className="alert alert-success">
                <span className="alert-icon">✅</span>
                <span>Study plan generated successfully!</span>
              </div>
            )}

            <button
              className="btn btn-primary btn-large"
              onClick={handleGenerate}
              disabled={loading}
            >
              {loading ? (
                <>
                  <span className="spinner"></span>
                  Generating Plan...
                </>
              ) : (
                <>Generate Study Plan</>
              )}
            </button>
          </div>
        </section>

        {/* Results Section */}
        {data && (
          <section className="results-section">
            {/* Export Button */}
            <div className="export-controls">
              <button className="btn btn-secondary" onClick={handleExportJSON}>
                📥 Export as JSON
              </button>
            </div>

            {/* Weekly Study Plan */}
            <section className="plan-section">
              <div className="section-header">
                <h2 className="section-title">📅 Weekly Study Schedule</h2>
                <p className="section-description">Your personalized learning journey</p>
              </div>

              <div className="schedule-grid">
                {data.plan.map((day, idx) => (
                  <div key={idx} className="schedule-card">
                    <div className="schedule-header">
                      <h3 className="schedule-day">{day.day}</h3>
                      <span className="schedule-hours">{day.total_hours}h</span>
                    </div>

                    <div className="sessions-list">
                      {day.sessions.map((session, i) => (
                        <div key={i} className="session-item">
                          <div className="session-info">
                            <span className={`session-type session-${session.session_type.toLowerCase()}`}>
                              {session.session_type.charAt(0).toUpperCase() + session.session_type.slice(1)}
                            </span>
                            <span className="session-subject">{session.subject}</span>
                          </div>
                          <span className="session-duration">{session.duration_hours}h</span>
                          <p className="session-notes">{session.notes}</p>
                        </div>
                      ))}
                    </div>
                  </div>
                ))}
              </div>
            </section>

            {/* Learning Resources */}
            <section className="resources-section">
              <div className="section-header">
                <h2 className="section-title">🔗 Learning Resources</h2>
                <p className="section-description">Curated resources for each subject</p>
              </div>

              <div className="resources-grid">
                {Object.entries(data.resources).map(([subject, links], idx) => (
                  <div key={idx} className="resource-card">
                    <h3 className="resource-title">{subject}</h3>
                    <div className="resource-links">
                      <a
                        href={links.youtube_search}
                        target="_blank"
                        rel="noreferrer"
                        className="resource-link"
                      >
                        <span className="resource-icon">▶️</span>
                        <span>YouTube Courses</span>
                      </a>
                      <a
                        href={links.pdf_search}
                        target="_blank"
                        rel="noreferrer"
                        className="resource-link"
                      >
                        <span className="resource-icon">📄</span>
                        <span>PDF Notes</span>
                      </a>
                      <a
                        href={links.freecodecamp}
                        target="_blank"
                        rel="noreferrer"
                        className="resource-link"
                      >
                        <span className="resource-icon">💻</span>
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
          <p>Made with ❤️ by AI Study Planner Team</p>
          <p className="footer-copyright">© 2025 AI Study Planner. All rights reserved.</p>
        </div>
      </footer>
    </div>
  );
}
