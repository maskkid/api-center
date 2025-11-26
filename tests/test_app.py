from fastapi.testclient import TestClient
import sys
import os

# Add app directory to path so imports work
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'app'))

from api_center import app


client = TestClient(app)


def test_root():
    resp = client.get("/")
    assert resp.status_code == 200
    data = resp.json()
    assert "api_prefix" in data


def test_user_profile():
    resp = client.get("/api/v1/user/profile")
    assert resp.status_code == 200
    data = resp.json()
    # API uses unified response format {code,msg,data}
    assert data.get("code") == 0
    assert "data" in data
