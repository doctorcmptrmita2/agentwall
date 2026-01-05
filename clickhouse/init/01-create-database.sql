-- AgentWall ClickHouse Schema
-- Time-series logs for agent requests/responses

-- Create database
CREATE DATABASE IF NOT EXISTS agentwall;

USE agentwall;

-- Main logs table (partitioned by month)
CREATE TABLE IF NOT EXISTS agent_logs (
    -- Identifiers
    log_id UUID DEFAULT generateUUIDv4(),
    run_id String,
    user_id String,
    team_id String,
    agent_id String,
    api_key_id String,
    
    -- Timestamps (partitioning key)
    timestamp DateTime64(3) DEFAULT now64(3),
    date Date DEFAULT toDate(timestamp),
    
    -- Request metadata
    request_method String,
    request_path String,
    request_model String,
    request_stream Bool,
    
    -- Request/Response content (compressed)
    request_messages String CODEC(ZSTD(3)),
    response_content String CODEC(ZSTD(3)),
    
    -- Response metadata
    response_status UInt16,
    response_finish_reason String,
    
    -- Metrics
    latency_ms UInt32,
    tokens_prompt UInt32,
    tokens_completion UInt32,
    tokens_total UInt32,
    cost_usd Float64,
    
    -- Agent Firewall specific
    step_number UInt16,
    is_streaming Bool,
    
    -- Loop Detection
    is_loop_detected Bool DEFAULT false,
    loop_reason String,
    loop_similarity Float32,
    
    -- DLP (Data Loss Prevention)
    is_sensitive_detected Bool DEFAULT false,
    sensitive_types Array(String),
    is_redacted Bool DEFAULT false,
    redaction_mode String,
    
    -- Budget & Limits
    is_budget_exceeded Bool DEFAULT false,
    is_step_limit_exceeded Bool DEFAULT false,
    is_timeout_exceeded Bool DEFAULT false,
    
    -- Tool calls (if any)
    tool_calls_count UInt16,
    tool_names Array(String),
    
    -- Error tracking
    is_error Bool DEFAULT false,
    error_type String,
    error_message String,
    
    -- Indexes for fast lookups
    INDEX idx_run_id run_id TYPE bloom_filter GRANULARITY 1,
    INDEX idx_user_id user_id TYPE bloom_filter GRANULARITY 1,
    INDEX idx_team_id team_id TYPE bloom_filter GRANULARITY 1,
    INDEX idx_agent_id agent_id TYPE bloom_filter GRANULARITY 1,
    INDEX idx_loop_detected is_loop_detected TYPE set(2) GRANULARITY 1,
    INDEX idx_sensitive_detected is_sensitive_detected TYPE set(2) GRANULARITY 1
)
ENGINE = MergeTree()
PARTITION BY toYYYYMM(date)
ORDER BY (team_id, user_id, timestamp)
TTL date + INTERVAL 90 DAY DELETE
SETTINGS index_granularity = 8192;

-- Materialized view for real-time analytics
CREATE MATERIALIZED VIEW IF NOT EXISTS agent_logs_hourly
ENGINE = SummingMergeTree()
PARTITION BY toYYYYMM(date)
ORDER BY (team_id, user_id, date, hour)
AS SELECT
    team_id,
    user_id,
    agent_id,
    date,
    toHour(timestamp) as hour,
    count() as request_count,
    sum(tokens_total) as total_tokens,
    sum(cost_usd) as total_cost,
    sum(latency_ms) as total_latency,
    avg(latency_ms) as avg_latency,
    countIf(is_loop_detected) as loop_count,
    countIf(is_sensitive_detected) as sensitive_count,
    countIf(is_error) as error_count
FROM agent_logs
GROUP BY team_id, user_id, agent_id, date, hour;

-- Materialized view for daily summaries
CREATE MATERIALIZED VIEW IF NOT EXISTS agent_logs_daily
ENGINE = SummingMergeTree()
PARTITION BY toYYYYMM(date)
ORDER BY (team_id, user_id, date)
AS SELECT
    team_id,
    user_id,
    agent_id,
    date,
    count() as request_count,
    sum(tokens_total) as total_tokens,
    sum(cost_usd) as total_cost,
    avg(latency_ms) as avg_latency,
    countIf(is_loop_detected) as loop_count,
    countIf(is_sensitive_detected) as sensitive_count,
    countIf(is_error) as error_count,
    max(timestamp) as last_request_time
FROM agent_logs
GROUP BY team_id, user_id, agent_id, date;

-- Table for loop detection patterns (for analysis)
CREATE TABLE IF NOT EXISTS loop_patterns (
    pattern_id UUID DEFAULT generateUUIDv4(),
    run_id String,
    team_id String,
    detected_at DateTime64(3) DEFAULT now64(3),
    
    -- Pattern details
    pattern_type String, -- 'repetitive_prompt', 'tool_spam', 'state_oscillation'
    similarity_score Float32,
    repetition_count UInt16,
    
    -- Context
    prompt_hash String,
    tool_name String,
    
    -- Action taken
    action_taken String, -- 'killed', 'warned', 'logged'
    cost_saved Float64,
    
    INDEX idx_run_id run_id TYPE bloom_filter GRANULARITY 1,
    INDEX idx_team_id team_id TYPE bloom_filter GRANULARITY 1
)
ENGINE = MergeTree()
PARTITION BY toYYYYMM(toDate(detected_at))
ORDER BY (team_id, detected_at)
TTL toDate(detected_at) + INTERVAL 90 DAY DELETE;

-- Table for DLP incidents (shadow logs)
CREATE TABLE IF NOT EXISTS dlp_incidents (
    incident_id UUID DEFAULT generateUUIDv4(),
    run_id String,
    team_id String,
    user_id String,
    detected_at DateTime64(3) DEFAULT now64(3),
    
    -- Incident details
    sensitive_type String, -- 'api_key', 'credit_card', 'email', etc.
    pattern_matched String,
    redaction_mode String, -- 'block', 'mask', 'shadow_log'
    
    -- Context (encrypted/hashed)
    request_hash String,
    matched_text_hash String, -- SHA256 hash (not actual text)
    
    -- Action taken
    was_blocked Bool,
    was_alerted Bool,
    
    INDEX idx_run_id run_id TYPE bloom_filter GRANULARITY 1,
    INDEX idx_team_id team_id TYPE bloom_filter GRANULARITY 1,
    INDEX idx_sensitive_type sensitive_type TYPE set(20) GRANULARITY 1
)
ENGINE = MergeTree()
PARTITION BY toYYYYMM(toDate(detected_at))
ORDER BY (team_id, detected_at)
TTL toDate(detected_at) + INTERVAL 180 DAY DELETE; -- 6 months retention for compliance

-- Table for budget tracking
CREATE TABLE IF NOT EXISTS budget_usage (
    usage_id UUID DEFAULT generateUUIDv4(),
    team_id String,
    user_id String,
    agent_id String,
    date Date,
    hour UInt8,
    
    -- Usage metrics
    request_count UInt32,
    tokens_used UInt32,
    cost_usd Float64,
    
    -- Limits
    daily_limit Float64,
    monthly_limit Float64,
    is_limit_exceeded Bool
)
ENGINE = SummingMergeTree()
PARTITION BY toYYYYMM(date)
ORDER BY (team_id, user_id, date, hour);

-- Insert sample data for testing
INSERT INTO agent_logs (
    run_id, user_id, team_id, agent_id, api_key_id,
    request_method, request_path, request_model,
    request_messages, response_content,
    response_status, response_finish_reason,
    latency_ms, tokens_prompt, tokens_completion, tokens_total, cost_usd,
    step_number
) VALUES (
    'test-run-001',
    'dev-user-1',
    'dev-team-1',
    'test-agent',
    'dev-key-1',
    'POST',
    '/v1/chat/completions',
    'gpt-4',
    '[{"role":"user","content":"Hello"}]',
    'Hello! How can I help you?',
    200,
    'stop',
    150,
    10,
    20,
    30,
    0.0015,
    1
);

-- Verify tables created
SELECT 
    name,
    engine,
    total_rows,
    total_bytes
FROM system.tables
WHERE database = 'agentwall'
ORDER BY name;
