"""Integration tests for the FastAPI layer (:mod:`app.main`)."""

from __future__ import annotations

import pytest
from fastapi.testclient import TestClient

from app.main import create_app


@pytest.fixture(scope="module")
def client() -> TestClient:
    """Provide a TestClient bound to a fresh application instance."""
    return TestClient(create_app())


def test_health(client: TestClient):
    response = client.get("/api/health")
    assert response.status_code == 200
    body = response.json()
    assert body["status"] == "ok"
    assert "version" in body


def test_solve_reynolds(client: TestClient):
    payload = {
        "variables": [
            {"symbol": "rho", "exponents": [1, -3, 0]},
            {"symbol": "V", "exponents": [0, 1, -1]},
            {"symbol": "D", "exponents": [0, 1, 0]},
            {"symbol": "mu", "exponents": [1, -1, -1]},
        ]
    }
    response = client.post("/api/pi/solve", json=payload)
    assert response.status_code == 200
    body = response.json()
    assert body["n_groups"] == 1
    assert body["rank"] == 3
    assert body["groups"][0]["ascii"] == "Pi_1 = rho*V*D/mu"


def test_solve_underdetermined_returns_422(client: TestClient):
    payload = {
        "variables": [
            {"symbol": "L", "exponents": [0, 1, 0]},
            {"symbol": "t", "exponents": [0, 0, 1]},
        ]
    }
    response = client.post("/api/pi/solve", json=payload)
    assert response.status_code == 422


def test_solve_requires_two_variables(client: TestClient):
    payload = {"variables": [{"symbol": "L", "exponents": [0, 1, 0]}]}
    response = client.post("/api/pi/solve", json=payload)
    # Pydantic min_length=2 -> 422 at validation time.
    assert response.status_code == 422


def test_library_endpoint(client: TestClient):
    response = client.get("/api/library")
    assert response.status_code == 200
    body = response.json()
    assert len(body["base_dimensions"]) == 7
    category_ids = {cat["id"] for cat in body["categories"]}
    assert {"mechanics", "fluid_mechanics", "electromagnetism"} <= category_ids


def test_examples_list_and_chen(client: TestClient):
    response = client.get("/api/examples")
    assert response.status_code == 200
    ids = {ex["id"] for ex in response.json()}
    assert "chen_1990" in ids

    chen = client.get("/api/examples/chen_1990")
    assert chen.status_code == 200
    assert len(chen.json()["variables"]) == 11


def test_unknown_example_returns_404(client: TestClient):
    response = client.get("/api/examples/does_not_exist")
    assert response.status_code == 404
