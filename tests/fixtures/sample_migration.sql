-- Migration: Create constitution_results table
-- Description: Stores constitution test results for users
-- Version: 1.0.0

CREATE TABLE constitution_results (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID REFERENCES users(id) ON DELETE CASCADE,
    primary_constitution VARCHAR(50) NOT NULL,
    secondary_constitutions JSONB,
    scores JSONB NOT NULL,
    answers JSONB,
    ip_address INET,
    user_agent TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Create index for user_id lookups
CREATE INDEX idx_constitution_results_user_id ON constitution_results(user_id);

-- Create index for primary_constitution queries
CREATE INDEX idx_constitution_results_primary ON constitution_results(primary_constitution);

-- Create index for created_at sorting
CREATE INDEX idx_constitution_results_created_at ON constitution_results(created_at DESC);

-- Add trigger for updated_at
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = CURRENT_TIMESTAMP;
    RETURN NEW;
END;
$$ language 'plpgsql';

CREATE TRIGGER update_constitution_results_updated_at
    BEFORE UPDATE ON constitution_results
    FOR EACH ROW
    EXECUTE FUNCTION update_updated_at_column();

-- Add comment
COMMENT ON TABLE constitution_results IS 'Stores constitution test results';
COMMENT ON COLUMN constitution_results.scores IS 'Constitution scores in percentage (0-100)';
COMMENT ON COLUMN constitution_results.answers IS 'Raw questionnaire answers (1-5 scale)';
