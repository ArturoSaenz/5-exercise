import sys
import pathlib
from fastapi.testclient import TestClient

# Ensure src is importable
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1] / "src"))

from app import app, activities

client = TestClient(app)


def test_get_activities():
    r = client.get("/activities")
    assert r.status_code == 200
    data = r.json()
    assert "Chess Club" in data


def test_signup_success_and_cleanup():
    activity = "Basketball Team"
    email = "testuser@example.com"
    # ensure not present
    assert email not in activities[activity]["participants"]

    r = client.post(f"/activities/{activity}/signup", params={"email": email})
    assert r.status_code == 200
    assert email in activities[activity]["participants"]

    # cleanup
    activities[activity]["participants"].remove(email)


def test_signup_duplicate():
    activity = "Chess Club"
    # pick an existing participant
    email = activities[activity]["participants"][0]
    r = client.post(f"/activities/{activity}/signup", params={"email": email})
    assert r.status_code == 400


def test_signup_not_found():
    r = client.post("/activities/NoSuchActivity/signup", params={"email": "a@b.com"})
    assert r.status_code == 404
