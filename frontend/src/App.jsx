import { useState } from "react";
import "./App.css";

export default function App() {
  const [subjects, setSubjects] = useState("Python, DSA");
  const [hours, setHours] = useState(3);
  const [data, setData] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  const handleGenerate = async () => {
    setLoading(true);
    setError("");
    setData(null);

    try {
      const res = await fetch("http://127.0.0.1:8000/plan", {
        method: "POST",
        headers: {
          "Content-Type": "application/json"
        },
        body: JSON.stringify({
          subjects: subjects
            .split(",")
            .map((s) => s.trim())
            .filter(Boolean),
          hours: Number(hours),
          days_per_week: 6
        })
      });

      if (!res.ok) {
        throw new Error(`Request failed with status ${res.status}`);
      }

      const json = await res.json();
      setData(json);
    } catch (err) {
      console.error(err);
      setError("Could not reach backend. Make sure FastAPI is running.");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="app-shell">
      <main className="app">
        {/* Header */}
        <header className="header">
          <h1 className="title">AI Study Planner</h1>
          <p className="subtitle">
            Multi-agent powered personalized study assistant
          </p>
        </header>

        {/* Controls */}
        <section className="controls">
          <input
            className="text-input"
            value={subjects}
            onChange={(e) => setSubjects(e.target.value)}
            placeholder="Python, DSA"
          />
          <input
            className="text-input"
            type="number"
            min="1"
            value={hours}
            onChange={(e) => setHours(e.target.value)}
            placeholder="Daily hours"
          />
          <button
            className="primary-button"
            onClick={handleGenerate}
            disabled={loading}
          >
            {loading ? "Generating..." : "Generate Study Plan"}
          </button>
        </section>

        {error && <p className="error">{error}</p>}

        {/* Weekly Study Plan */}
        {data && (
          <>
            <section className="section">
              <h2 className="section-title">Weekly Study Plan</h2>

              <div className="cards-grid">
                {data.plan.map((day, idx) => (
                  <article key={idx} className="card">
                    <h3 className="card-title">
                      {day.day} — {day.total_hours} hrs
                    </h3>

                    <ul className="card-list">
                      {day.sessions.map((s, i) => (
                        <li key={i} className="card-item">
                          <span className="card-item-main">
                            {s.subject} — {s.session_type}
                          </span>
                          <span className="card-item-meta">
                            {s.duration_hours} hrs
                          </span>
                          <span className="card-item-note">{s.notes}</span>
                        </li>
                      ))}
                    </ul>
                  </article>
                ))}
              </div>
            </section>

            {/* Learning Resources */}
            <section className="section">
              <h2 className="section-title">Learning Resources</h2>

              <div className="cards-grid resources-grid">
                {Object.entries(data.resources).map(([subject, links], idx) => (
                  <article key={idx} className="card">
                    <h3 className="card-title">{subject}</h3>
                    <ul className="card-list">
                      <li className="card-item">
                        <a
                          href={links.youtube_search}
                          target="_blank"
                          rel="noreferrer"
                          className="link"
                        >
                          ▶ YouTube Course
                        </a>
                      </li>
                      <li className="card-item">
                        <a
                          href={links.pdf_search}
                          target="_blank"
                          rel="noreferrer"
                          className="link"
                        >
                          📄 PDF Notes
                        </a>
                      </li>
                      <li className="card-item">
                        <a
                          href={links.freecodecamp}
                          target="_blank"
                          rel="noreferrer"
                          className="link"
                        >
                          💻 FreeCodeCamp Path
                        </a>
                      </li>
                    </ul>
                  </article>
                ))}
              </div>
            </section>
          </>
        )}

        {/* Footer */}
        <footer className="footer">
          Happy Learning!
        </footer>
      </main>
    </div>
  );
}
