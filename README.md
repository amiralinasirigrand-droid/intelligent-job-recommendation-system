# Intelligent Job and Skill Recommendation System

A full-stack thesis project for browsing jobs, maintaining a skill profile, calculating job-to-skill compatibility, and identifying skills to develop.

## Stack

- Frontend: React + Vite
- Backend: Python + FastAPI
- Database: PostgreSQL
- Authentication: JWT bearer tokens
- Recommendation logic: weighted required/optional skill matching and proficiency-level scoring

## Prerequisites

- Python 3.11 or newer (the project was developed with Python 3.13)
- Node.js compatible with the Vite version in `fronted/package.json`
- PostgreSQL

## Backend setup

1. Open a terminal in `backend`.
2. Create and activate a virtual environment.
3. Install dependencies:

   ```bash
   python -m venv .venv
   # Windows CMD:
   .venv\\Scripts\\activate
   # macOS/Linux:
   source .venv/bin/activate
   pip install -r requirements.txt
   ```

4. Copy `.env.example` to `.env` and set your local PostgreSQL URL and a long random `SECRET_KEY`.
5. Create the `job_recommendation_db` database in PostgreSQL and apply `database/schema.sql/schema.sql` if setting up a fresh database.
6. Start the API from the `backend` directory:

   ```bash
   uvicorn main:app --reload
   ```

7. Open `http://127.0.0.1:8000/docs` to inspect the API.

## Frontend setup

1. Open a second terminal in `fronted`.
2. Install packages and start Vite:

   ```bash
   npm install
   npm run dev
   ```

3. Open the local URL printed by Vite (normally `http://localhost:5173`).

The frontend expects the API at `http://127.0.0.1:8000`. CORS is configured for `http://localhost:5173` in `backend/main.py`.

## Main user flow

1. Browse and search the available jobs.
2. Register or sign in.
3. Add skills to the profile and choose a proficiency level.
4. Open a job to view its required/optional skills and personalized match analysis.
5. Review missing skills and learning recommendations.

## Notes

- Never commit the real `.env` file or credentials.
- `database/schema.sql/schema.sql` describes a fresh database. If an existing local database has already been created using a different schema, compare it with the SQLAlchemy models before applying schema changes.
- Recommendation scores are rule-based scores, not claims of machine-learning model accuracy. The current implementation weights required skills more heavily than optional skills.
