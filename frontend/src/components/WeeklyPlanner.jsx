import React from 'react';
import SessionCard from './SessionCard';
import './WeeklyPlanner.css';

const DAYS = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday'];

export default function WeeklyPlanner({ plan }) {
  return (
    <div className="weekly-planner">
      <div className="planner-header">
        <h2>📅 Your Weekly Study Plan</h2>
        <p>Structured learning for maximum productivity</p>
      </div>

      <div className="days-grid">
        {plan.map((day, dayIndex) => (
          <div key={dayIndex} className="day-card">
            <div className="day-header">
              <h3>{day.day}</h3>
              <span className="total-hours">{day.total_hours}h</span>
            </div>

            <div className="sessions-container">
              {day.sessions.length > 0 ? (
                day.sessions.map((session, sessionIndex) => (
                  <SessionCard
                    key={`${day.day}-${sessionIndex}-${session.subject}`}
                    day={day.day}
                    session={session}
                  />
                ))
              ) : (
                <p className="no-sessions">Rest day 😌</p>
              )}
            </div>
          </div>
        ))}
      </div>
    </div>
  );
}
