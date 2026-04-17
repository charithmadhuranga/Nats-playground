CREATE TABLE nats_data (
    time TIMESTAMPTZ NOT NULL,
    subject TEXT,
    value DOUBLE PRECISION,
    unit TEXT
);

-- Convert into a hypertable for time-series performance
SELECT create_hypertable('nats_data', 'time');