from copy import deepcopy

import pytest
from fastapi.testclient import TestClient

import src.app as app_module
from src.app import app


@pytest.fixture
def client(monkeypatch):
    """Provide an isolated application state and real FastAPI test client."""
    monkeypatch.setattr(app_module, "activities", deepcopy(app_module.activities))
    with TestClient(app) as test_client:
        yield test_client


def test_unregister_participant_removes_participant_from_activity(client):
    # Arrange
    activity_name = "Soccer Team"
    email = "student@example.edu"
    app_module.activities[activity_name]["participants"].append(email)

    # Act
    response = client.delete(
        f"/activities/{activity_name}/participants",
        params={"email": email},
    )

    # Assert
    assert response.status_code == 200
    assert email not in app_module.activities[activity_name]["participants"]
    assert response.json()["message"] == f"Unregistered {email} from {activity_name}"


def test_unregister_participant_returns_not_found_when_not_registered(client):
    # Arrange
    activity_name = "Soccer Team"
    email = "missing@example.edu"

    # Act
    response = client.delete(
        f"/activities/{activity_name}/participants",
        params={"email": email},
    )

    # Assert
    assert response.status_code == 404
    assert response.json()["detail"] == "Participant not found"
