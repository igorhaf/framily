CREATE TABLE IF NOT EXISTS calendar_events (
    id SERIAL PRIMARY KEY,
    title VARCHAR NOT NULL,
    description VARCHAR,
    start_date TIMESTAMP NOT NULL,
    end_date TIMESTAMP NOT NULL,
    event_type VARCHAR NOT NULL,
    family_member_id INTEGER REFERENCES family_members(id),
    location VARCHAR,
    is_all_day BOOLEAN NOT NULL DEFAULT FALSE,
    color VARCHAR
); 