"""
Pytest configuration and fixtures
"""

import pytest
from fastapi.testclient import TestClient
from main import app


@pytest.fixture
def client():
    """FastAPI test client"""
    return TestClient(app)


@pytest.fixture
def mock_openai_response():
    """Mock OpenAI response"""
    return {
        "id": "chatcmpl-test123",
        "object": "chat.completion",
        "created": 1234567890,
        "model": "gpt-4",
        "choices": [
            {
                "index": 0,
                "message": {
                    "role": "assistant",
                    "content": "Hello! How can I help you?"
                },
                "finish_reason": "stop"
            }
        ],
        "usage": {
            "prompt_tokens": 10,
            "completion_tokens": 20,
            "total_tokens": 30
        }
    }


@pytest.fixture
def mock_api_key():
    """Mock API key for testing"""
    return "af-test-key-123456789"


@pytest.fixture
def auth_headers(mock_api_key):
    """Authentication headers"""
    return {
        "Authorization": f"Bearer {mock_api_key}"
    }
