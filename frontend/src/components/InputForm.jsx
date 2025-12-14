import React from 'react';

export default function InputForm({
  subjects,
  setSubjects,
  hours,
  setHours,
  daysPerWeek,
  setDaysPerWeek,
  error,
  success,
  loading,
  onGeneratePlan
}) {
  return (
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
          onClick={onGeneratePlan}
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
  );
}
