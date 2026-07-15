CREATE TABLE derived_indicators (
    derived_id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    base_indicator_id INTEGER REFERENCES indicators(indicator_id),
    formula_desc TEXT,
    created_at TIMESTAMP DEFAULT NOW()
    UNIQUE (name, base_indicator_id)
);


CREATE TABLE derived_values (
    id SERIAL PRIMARY KEY,
    derived_id INTEGER NOT NULL REFERENCES derived_indicators(derived_id), -- foreign key to indicators table
    date DATE NOT NULL,
    value NUMERIC(18,6), -- number with 18 digits, 6 being decimals
    inserted_at TIMESTAMP DEFAULT NOW(),
    UNIQUE (derived_id, date) -- avoid duplicates based on date and id
);

CREATE INDEX idx_derived_values_lookup ON derived_values (derived_id, date);