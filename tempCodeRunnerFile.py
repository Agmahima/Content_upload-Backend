CREATE TABLE IF NOT EXISTS movie(
        id SERIAL PRIMARY KEY,
        budget INT,
        homepage VARCHAR(255),
        original_language VARCHAR(10),
        original_title VARCHAR(255),
        overview TEXT,
        release_date DATE,
        revenue BIGINT,
        runtime INT,
        status VARCHAR(50),
        title VARCHAR(255),
        vote_average FLOAT,
        vote_count INT,
        production_company_id VARCHAR(255)
        genre_id VARCHAR(255)
        languages VARCHAR(255)
    )