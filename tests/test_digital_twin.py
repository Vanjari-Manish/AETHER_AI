"""
GPO Backend Test Suite — Digital Twin & Topology Endpoints
Path: tests/test_digital_twin.py
"""
import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src-backend"))

from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_get_digital_twin_summary():
    # Login as admin to get the token
    login_response = client.post("/api/auth/login", json={
        "email": "admin@gpo.gov",
        "password": "admin"
    })
    assert login_response.status_code == 200
    token = login_response.json()["access_token"]
    
    # Query summary
    response = client.get("/api/v1/digital-twin/summary", headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == 200
    data = response.json()
    assert data["success"] is True
    
    # Assert metrics exist
    metrics = data["data"]["metrics"]
    assert metrics["total_substations"] == 3
    assert metrics["total_buses"] == 4
    assert metrics["total_transmission_lines"] == 2
    assert metrics["total_transformers"] == 1
    assert metrics["total_generators"] == 2
    assert metrics["total_loads"] == 2
    assert metrics["connected_components"] == 1
    assert metrics["asset_validation_status"] == "Passed"
    assert metrics["database_synchronization_status"] == "Synchronized"
    assert metrics["topology_completeness"] == 100.0
    
    # Assert topology lists exist
    topology = data["data"]["topology"]
    assert len(topology["substations"]) == 3
    assert len(topology["buses"]) == 4
    assert len(topology["transmission_lines"]) == 2
    assert len(topology["transformers"]) == 1
    assert len(topology["generators"]) == 2
    assert len(topology["loads"]) == 2
    assert len(topology["switches"]) == 2
    
    # Assert recent events exist
    events = data["data"]["recent_events"]
    assert len(events) > 0
