CREATE TABLE indicators (
    indicator_id SERIAL PRIMARY KEY,
    external_code VARCHAR(50) UNIQUE NOT NULL, -- code for the series on the API
    indicator_name VARCHAR(100) NOT NULL, -- descriptive name for the series
    source VARCHAR(50) NOT NULL, -- where the data was collected
    frequency VARCHAR(20) NOT NULL, -- whether the series is daily, monthly or other
    unit VARCHAR(30), -- optional measuring unit, can be left blank if not applicable
    created_at TIMESTAMP DEFAULT NOW() -- date of when data was added (check for outdated values)
    );


CREATE TABLE indicator_values (
    id SERIAL PRIMARY KEY,
    indicator_id INTEGER NOT NULL REFERENCES indicators(indicator_id), -- foreign key to indicators table
    date DATE NOT NULL,
    value NUMERIC(18,6), -- number with 18 digits, 6 being decimals
    inserted_at TIMESTAMP DEFAULT NOW(),
    UNIQUE (indicator_id, date) -- avoid duplicates based on date and id
    );

-- most queries would be interested in getting the series values for a particular time period
-- so this index is enough for now
CREATE INDEX idx_indicator_values_lookup ON indicator_values (indicator_id, date);
