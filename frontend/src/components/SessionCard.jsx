import React from 'react';
import './SessionCard.css';

export default function SessionCard({ day, session }) {
  const sessionTypeEmoji = {
    concept: '💡',
    practice: '💻',
    revision: '🔄'
  };

  return (
    <div className="session-card">
      <div className="session-header">
        <span className="session-emoji">{sessionTypeEmoji[session.session_type] || '📚'}</span>
        <div className="session-title">
          <h4>{session.subject}</h4>
          <p className="session-type">{session.session_type}</p>
        </div>
      </div>
      <div className="session-content">
        <div className="duration-badge">{session.duration_hours}h</div>
      </div>
      <p className="session-notes">{session.notes}</p>
    </div>
  );
}
