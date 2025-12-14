import React from 'react';

export default function StudyPlanDisplay({ data, onExportJSON }) {
  return (
    <section className="results-section">
      {/* Export Button */}
      <div className="export-controls">
        <button className="btn btn-secondary" onClick={onExportJSON}>
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
  );
}
