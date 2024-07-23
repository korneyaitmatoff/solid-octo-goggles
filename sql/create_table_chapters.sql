BEGIN;
DROP TABLE IF EXISTS chapters CASCADE;
CREATE TABLE chapters(
    id SERIAL PRIMARY KEY,
    manga_id INT,
    url VARCHAR(255),
    CONSTRAINT fk_anga FOREIGN KEY (manga_id) REFERENCES manga(id)
);
COMMIT;