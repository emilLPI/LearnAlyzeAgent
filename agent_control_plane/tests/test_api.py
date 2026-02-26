from fastapi.testclient import TestClient

from app.main import app


client = TestClient(app)


def test_email_to_task_to_job_flow():
    email = client.post(
        "/emails",
        json={
            "tenant_id": "tenant-a",
            "from_address": "ops@example.com",
            "subject": "Please opret kunde",
            "body": "new customer onboarding",
        },
    )
    assert email.status_code == 200
    email_id = email.json()["id"]

    task = client.post("/tasks/from-email", json={"email_id": email_id})
    assert task.status_code == 200
    task_id = task.json()["id"]

    job = client.post(f"/jobs/plan/{task_id}")
    assert job.status_code == 200
    assert job.json()["status"] in {"planned", "executing", "requires_approval"}


def test_settings_store_outlook_and_manual_login_constraint():
    response = client.post(
        "/settings",
        json={
            "tenant_id": "tenant-a",
            "autonomy_mode": "SUPERVISED",
            "scopes": ["Customers", "Emails"],
            "kill_switch": False,
            "policy": {"no_delete_without_approval": True},
            "outlook_connected": True,
            "require_manual_learnalyze_login": True,
        },
    )
    assert response.status_code == 200

    read_back = client.get("/settings", params={"tenant_id": "tenant-a"})
    assert read_back.status_code == 200
    assert read_back.json()["outlook_connected"] is True
    assert read_back.json()["require_manual_learnalyze_login"] is True


def test_webapp_root_is_served():
    response = client.get("/")
    assert response.status_code == 200
    assert "ARX Agent Control Plane" in response.text


def test_capability_insights_endpoint():
    bootstrap = client.get("/capabilities/insights")
    assert bootstrap.status_code == 200
    assert bootstrap.json()["total_snapshots"] >= 0

    client.post("/capabilities/rescan")
    after = client.get("/capabilities/insights")
    assert after.status_code == 200
    assert after.json()["total_snapshots"] >= 1
    assert "learned_actions" in after.json()


def test_learnalyze_embed_is_not_used():
    response = client.get("/")
    assert response.status_code == 200
    assert "Open LearnAlyze directly" in response.text
    assert "<iframe" not in response.text
