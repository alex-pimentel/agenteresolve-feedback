import pytest
from fastapi.testclient import TestClient

from app import main, tools
from app.providers import ProviderUnavailable


def test_health() -> None:
    client = TestClient(main.app)
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "ok"


def test_job_flow(monkeypatch: pytest.MonkeyPatch) -> None:
    def fake_run(_ti: object) -> tuple[bytes, str, str]:
        return b"ok", "text/plain", "result.txt"

    monkeypatch.setattr(tools, "run", fake_run)
    client = TestClient(main.app)
    created = client.post("/api/feedback/", json={"text": "hello"})
    assert created.status_code == 200
    task_id = created.json()["task_id"]
    job = client.get(f"/api/feedback/{task_id}").json()
    assert job["status"] == "done"
    assert job["result_url"].endswith("result.txt")
    assert client.get(job["result_url"]).content == b"ok"


def test_provider_unavailable(monkeypatch: pytest.MonkeyPatch) -> None:
    def boom(_ti: object) -> tuple[bytes, str, str]:
        raise ProviderUnavailable("no provider")

    monkeypatch.setattr(tools, "run", boom)
    client = TestClient(main.app)
    response = client.post("/api/feedback/", json={"text": "x"})
    assert response.status_code == 503


def test_unknown_tool() -> None:
    client = TestClient(main.app)
    assert client.post("/api/nope/", json={"text": "x"}).status_code == 404
