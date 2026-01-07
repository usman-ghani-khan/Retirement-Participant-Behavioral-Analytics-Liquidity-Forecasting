-- ==========================================================
-- PROJECT: US Retirement Ecosystem Analytics
-- DESCRIPTION: Database Schema and Data Architecture
-- TOOLS: PostgreSQL & pgAdmin 4
-- ==========================================================

-- 1. SCHEMA INITIALIZATION
-- Create the Dimension Table for Participant Profiles
CREATE TABLE participants (
    participant_id VARCHAR(10) PRIMARY KEY,
    salary NUMERIC(12,2),
    savings_rate NUMERIC(5,4),
    login_frequency INTEGER,
    segment_label VARCHAR(20)
);

-- Create the Fact Table for Monthly Transactions
CREATE TABLE transactions (
    participant_id VARCHAR(10),
    month_id INTEGER,
    market_return NUMERIC(6,4),
    loan_event INTEGER,           
    loan_amount NUMERIC(12,2),
    FOREIGN KEY (participant_id) REFERENCES participants(participant_id)
);

-- 2. DATA INGESTION PROCESS
/* NOTE: For this project, data was imported using the pgAdmin 4 Import/Export Tool:
   - File Format: CSV
   - Encoding: UTF-8
   - Header: Yes
   - Delimiter: ','
   - Strategy: Manual mapping of CSV columns to PostgreSQL schema to ensure data integrity.
*/

-- 3. ANALYTICAL BRIDGE (Query for SQLAlchemy)
-- This JOIN creates the flattened dataset used for Clustering and Time Series analysis.
SELECT 
    p.participant_id,
    p.salary,
    p.savings_rate,
    p.login_frequency,
    t.month_id,
    t.market_return,
    t.loan_event,
    t.loan_amount
FROM participants p
JOIN transactions t ON p.participant_id = t.participant_id
ORDER BY p.participant_id, t.month_id;

-- 4. VALIDATION QUERY
-- Validating the Market Crash anomaly at Month 18
SELECT 
    month_id, 
    COUNT(CASE WHEN loan_event = 1 THEN 1 END) as total_loans, 
    SUM(loan_amount) as total_outflow
FROM transactions
WHERE month_id BETWEEN 17 AND 19
GROUP BY month_id
ORDER BY month_id;
