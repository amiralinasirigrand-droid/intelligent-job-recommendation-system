import pytest
from datetime import date
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool
from database import Base
from main import app
from routers.users import get_db, get_current_user
from models.user import User
from models.education import Education
from models.experience import Experience

@pytest.fixture
def security_client():
    engine = create_engine("sqlite://", connect_args={"check_same_thread": False}, poolclass=StaticPool)
    TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    Base.metadata.create_all(bind=engine)
    db = TestingSessionLocal()
    user_a = User(email="a@example.test", password_hash="x", first_name="User", last_name="A")
    user_b = User(email="b@example.test", password_hash="x", first_name="User", last_name="B")
    db.add_all([user_a, user_b])
    db.commit()
    db.refresh(user_a)
    db.refresh(user_b)
    education = Education(user_id=user_a.id, degree="BSc", field_of_study="CS", institution="Test University")
    experience = Experience(user_id=user_a.id, job_title="Developer", company="Test Company", start_date=date(2024, 1, 1))
    db.add_all([education, experience])
    db.commit()
    education_id, experience_id = education.id, experience.id
    db.close()
    def override_db():
        session = TestingSessionLocal()
        try:
            yield session
        finally:
            session.close()
    def override_user():
        session = TestingSessionLocal()
        try:
            return session.query(User).filter(User.email == "b@example.test").first()
        finally:
            session.close()
    app.dependency_overrides[get_db] = override_db
    app.dependency_overrides[get_current_user] = override_user
    try:
        with TestClient(app) as client:
            yield client, education_id, experience_id, TestingSessionLocal
    finally:
        app.dependency_overrides.clear()
        Base.metadata.drop_all(bind=engine)
        engine.dispose()

def test_user_cannot_read_another_users_education(security_client):
    client, education_id, _, _ = security_client
    response = client.get(f"/api/users/me/education/{education_id}")
    assert response.status_code == 404

def test_user_cannot_update_another_users_education(security_client):
    client, education_id, _, TestingSessionLocal = security_client
    response = client.put(f"/api/users/me/education/{education_id}", json={"degree": "Changed", "field_of_study": "Changed", "institution": "Changed", "start_date": "2024-01-01", "end_date": None})
    assert response.status_code == 404
    db = TestingSessionLocal()
    try:
        assert db.query(Education).filter(Education.id == education_id).first().degree == "BSc"
    finally:
        db.close()

def test_user_cannot_delete_another_users_experience(security_client):
    client, _, experience_id, TestingSessionLocal = security_client
    response = client.delete(f"/api/users/me/experience/{experience_id}")
    assert response.status_code == 404
    db = TestingSessionLocal()
    try:
        assert db.query(Experience).filter(Experience.id == experience_id).first() is not None
    finally:
        db.close()
def test_user_cannot_delete_another_users_skill(security_client):
    from models.user_skill import UserSkill
    from models.skill import Skill

    client, _, _, TestingSessionLocal = security_client

    db = TestingSessionLocal()
    try:
        user_a = db.query(User).filter(
            User.email == "a@example.test"
        ).first()

        skill = Skill(
            name="Test Python",
            description="Test skill"
        )
        db.add(skill)
        db.commit()
        db.refresh(skill)

        skill_id = skill.id
        user_a_id = user_a.id

        db.add(UserSkill(
            user_id=user_a_id,
            skill_id=skill_id,
            skill_level="Advanced"
        ))
        db.commit()
    finally:
        db.close()

    response = client.delete(
        f"/api/users/me/skills/{skill_id}"
    )

    assert response.status_code == 404

    db = TestingSessionLocal()
    try:
        skill_record = db.query(UserSkill).filter(
            UserSkill.user_id == user_a_id,
            UserSkill.skill_id == skill_id
        ).first()

        assert skill_record is not None
    finally:
        db.close()