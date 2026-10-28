
from fastapi.testclient import TestClient

from main import app


client = TestClient(app)


def test_get_existing_job():
    response = client.get("/api/jobs/3")

    assert response.status_code == 200

    data = response.json()

    assert data["id"] == 3
    assert data["title"] == "Python Developer"
    assert data["company"] == "Test Company"
    assert isinstance(data["skills"], list)


def test_get_nonexistent_job():
    response = client.get("/api/jobs/9999")

    assert response.status_code == 404
    assert response.json()["detail"] == "Job not found"
