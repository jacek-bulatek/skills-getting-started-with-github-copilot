from fastapi.testclient import TestClient

from src.app import activities, app


client = TestClient(app)


def test_unregister_participant_removes_participant_from_activity():
    activity_name = "Soccer Team"
    email = "student@example.edu"
    activities[activity_name]["participants"].append(email)

    response = client.delete(
        f"/activities/{activity_name}/participants",
        params={"email": email},
    )

    assert response.status_code == 200
    assert email not in activities[activity_name]["participants"]
    assert response.json()["message"] == f"Unregistered {email} from {activity_name}"


def test_unregister_participant_returns_not_found_when_not_registered():
    response = client.delete(
        "/activities/Soccer Team/participants",
        params={"email": "missing@example.edu"},
    )

    assert response.status_code == 404
    assert response.json()["detail"] == "Participant not found"
