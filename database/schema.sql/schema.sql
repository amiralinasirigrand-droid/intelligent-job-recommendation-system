-- Intelligent Job Recommendation System
-- PostgreSQL Database Schema


-- =========================================
-- 1. USERS
-- =========================================

CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    email VARCHAR(255) NOT NULL UNIQUE,
    password_hash VARCHAR(255) NOT NULL,
    first_name VARCHAR(100) NOT NULL,
    last_name VARCHAR(100) NOT NULL,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);


-- =========================================
-- 2. EDUCATION
-- =========================================

CREATE TABLE education (
    id SERIAL PRIMARY KEY,
    user_id INTEGER NOT NULL,
    degree VARCHAR(100) NOT NULL,
    field_of_study VARCHAR(150) NOT NULL,
    institution VARCHAR(200) NOT NULL,
    start_date DATE,
    end_date DATE,

    CONSTRAINT fk_education_user
        FOREIGN KEY (user_id)
        REFERENCES users(id)
        ON DELETE CASCADE
);


-- =========================================
-- 3. EXPERIENCE
-- =========================================

CREATE TABLE experience (
    id SERIAL PRIMARY KEY,
    user_id INTEGER NOT NULL,
    job_title VARCHAR(150) NOT NULL,
    company VARCHAR(200) NOT NULL,
    description TEXT,
    start_date DATE NOT NULL,
    end_date DATE,

    CONSTRAINT fk_experience_user
        FOREIGN KEY (user_id)
        REFERENCES users(id)
        ON DELETE CASCADE
);


-- =========================================
-- 4. SKILLS
-- =========================================

CREATE TABLE skills (
    id SERIAL PRIMARY KEY,
    name VARCHAR(150) NOT NULL UNIQUE,
    description TEXT
);


-- =========================================
-- 5. USER SKILLS
-- =========================================

CREATE TABLE user_skills (
    user_id INTEGER NOT NULL,
    skill_id INTEGER NOT NULL,
    skill_level VARCHAR(50) NOT NULL DEFAULT 'Beginner',

    PRIMARY KEY (user_id, skill_id),

    CONSTRAINT fk_user_skills_user
        FOREIGN KEY (user_id)
        REFERENCES users(id)
        ON DELETE CASCADE,

    CONSTRAINT fk_user_skills_skill
        FOREIGN KEY (skill_id)
        REFERENCES skills(id)
        ON DELETE CASCADE
);


-- =========================================
-- 6. JOBS
-- =========================================

CREATE TABLE jobs (
    id SERIAL PRIMARY KEY,
    title VARCHAR(200) NOT NULL,
    company VARCHAR(200) NOT NULL,
    description TEXT,
    location VARCHAR(200),
    employment_type VARCHAR(50),
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);


-- =========================================
-- 7. JOB SKILLS
-- =========================================

CREATE TABLE job_skills (
    job_id INTEGER NOT NULL,
    skill_id INTEGER NOT NULL,
    required_level VARCHAR(50),
    is_required BOOLEAN NOT NULL DEFAULT TRUE,

    PRIMARY KEY (job_id, skill_id),

    CONSTRAINT fk_job_skills_job
        FOREIGN KEY (job_id)
        REFERENCES jobs(id)
        ON DELETE CASCADE,

    CONSTRAINT fk_job_skills_skill
        FOREIGN KEY (skill_id)
        REFERENCES skills(id)
        ON DELETE CASCADE
);