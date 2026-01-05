"""
Test health check endpoints
"""

import pytest
from fastapi.testclient import TestClient
from main import app

client = TestClient(app)


def test_root_endpoint():
    """Test root endpoint returns API info"""
    response = client.get("/")
    assert response.status_code == 200
    
    data = response.json()
    assert data["name"] == "AgentWall Proxy Engine"
    assert data["status"] == "operational"
    assert "motto" in data


def test_health_check():
    """Test basic health check"""
    response = client.get("/health/")
    assert response.status_code == 200
    
    data = response.json()
    assert data["status"] == "healthy"
    assert "timestamp" in data
    assert "version" in data


def test_liveness_check():
    """Test liveness probe"""
    response = client.get("/health/live")
    assert response.status_code == 200
    
    data = response.json()
    assert data["alive"] is True
    assert "timestamp" in data


def test_readiness_check():
    """Test readiness probe"""
    response = client.get("/health/ready")
    assert response.status_code == 200
    
    data = response.json()
    assert "ready" in data
    assert "checks" in data
    assert "timestamp" in data
