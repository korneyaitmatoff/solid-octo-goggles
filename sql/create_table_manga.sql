DROP TABLE IF EXISTS manga;
CREATE TABLE manga(
    id SERIAL PRIMARY KEY,
    name VARCHAR(255),
    info TEXT,
    genres TEXT
);