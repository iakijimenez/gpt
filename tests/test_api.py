from fastapi.testclient import TestClient

from app.main import app


client = TestClient(app)


def test_health_ok() -> None:
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_generate_ok() -> None:
    payload = {
        "prompt": "Quiero una casa moderna de 2 pisos, 3 habitaciones, patio con jardín y mucha luz natural"
    }
    response = client.post("/generate", json=payload)

    assert response.status_code == 200
    data = response.json()

    assert "summary" in data
    assert len(data["images"]) >= 1
    assert "rooms" in data["plan"]
    assert len(data["video"]["storyboard"]) >= 1
