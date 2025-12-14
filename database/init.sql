-- Study Planner Database Schema

-- Create study_plans table
CREATE TABLE IF NOT EXISTS study_plans (
    plan_id SERIAL PRIMARY KEY,
    subjects TEXT NOT NULL,
    hours_per_week FLOAT NOT NULL,
    days_per_week INT NOT NULL,
    plan_data JSONB NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Create workflow_executions table
CREATE TABLE IF NOT EXISTS workflow_executions (
    execution_id SERIAL PRIMARY KEY,
    plan_id INT REFERENCES study_plans(plan_id) ON DELETE CASCADE,
    workflow_name VARCHAR(255) NOT NULL,
    status VARCHAR(50) NOT NULL,
    started_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    completed_at TIMESTAMP,
    error_message TEXT
);

-- Create study_sessions table
CREATE TABLE IF NOT EXISTS study_sessions (
    session_id SERIAL PRIMARY KEY,
    plan_id INT REFERENCES study_plans(plan_id) ON DELETE CASCADE,
    day_name VARCHAR(20) NOT NULL,
    subject VARCHAR(255) NOT NULL,
    session_type VARCHAR(50) NOT NULL,
    duration_hours FLOAT NOT NULL,
    notes TEXT,
    time_slot VARCHAR(50),
    completed BOOLEAN DEFAULT FALSE,
    completed_at TIMESTAMP
);

-- Create indexes for faster queries
CREATE INDEX idx_study_plans_created_at ON study_plans(created_at);
CREATE INDEX idx_workflow_executions_plan_id ON workflow_executions(plan_id);
CREATE INDEX idx_workflow_executions_status ON workflow_executions(status);
CREATE INDEX idx_study_sessions_plan_id ON study_sessions(plan_id);
CREATE INDEX idx_study_sessions_day_name ON study_sessions(day_name);

-- Create view for quick plan summary
CREATE OR REPLACE VIEW plan_summary AS
SELECT 
    p.plan_id,
    p.subjects,
    p.hours_per_week,
    p.days_per_week,
    p.created_at,
    COUNT(DISTINCT ss.session_id) as total_sessions,
    COUNT(CASE WHEN ss.completed = TRUE THEN 1 END) as completed_sessions
FROM study_plans p
LEFT JOIN study_sessions ss ON p.plan_id = ss.plan_id
GROUP BY p.plan_id, p.subjects, p.hours_per_week, p.days_per_week, p.created_at;
