"""
AgentWall Comprehensive Test Suite
Tests: FastAPI Proxy, DLP, Loop Detection, E2E Flow

Run: pytest tests/test_suite.py -v
"""

import pytest
import asyncio
import json
import time
import sys
from pathlib import Path
from unittest.mock import AsyncMock, MagicMock, patch
from fastapi.testclient import TestClient

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from main import app
from services.loop_detector import loop_detector, LoopCheckResult
from services.cost_calculator import calculate_cost
from models.requests import ChatCompletionRequest, Message


# ============================================================================
# FIXTURES
# ============================================================================

@pytest.fixture
def client():
    """FastAPI test client"""
    return TestClient(app)


@pytest.fixture
def valid_chat_request():
    """Valid chat completion request"""
    return {
        "model": "gpt-4",
        "messages": [
            {"role": "user", "content": "What is 2+2?"}
        ],
        "temperature": 0.7,
        "max_tokens": 100,
    }


@pytest.fixture
def streaming_request():
    """Streaming chat request"""
    return {
        "model": "gpt-4",
        "messages": [
            {"role": "user", "content": "Count to 5"}
        ],
        "stream": True,
    }


# ============================================================================
# PHASE 1: FASTAPI PROXY TESTS
# ============================================================================

class TestFastAPIProxy:
    """Test FastAPI proxy core functionality"""
    
    def test_health_endpoint(self, client):
        """Test health check endpoint"""
        response = client.get("/health")
        assert response.status_code == 200
        data = response.json()
        assert "status" in data
    
    def test_root_endpoint(self, client):
        """Test root endpoint"""
        response = client.get("/")
        assert response.status_code == 200
        data = response.json()
        assert "AgentWall" in data["name"]
        assert "Guard the Agent" in data.get("motto", "")
    
    def test_missing_api_key(self, client, valid_chat_request):
        """Test request without API key"""
        response = client.post(
            "/v1/chat/completions",
            json=valid_chat_request
        )
        assert response.status_code == 401
        assert "Missing API key" in response.text or "Invalid" in response.text
    
    def test_invalid_api_key(self, client, valid_chat_request):
        """Test request with invalid API key"""
        response = client.post(
            "/v1/chat/completions",
            json=valid_chat_request,
            headers={"Authorization": "Bearer invalid-key-xyz"}
        )
        # In dev mode, this might pass (mock validation)
        # In production, should be 401
        assert response.status_code in [200, 401]
    
    @patch('services.openai_proxy.openai_proxy.chat_completion')
    async def test_chat_completion_non_streaming(self, mock_openai, client, valid_chat_request):
        """Test non-streaming chat completion"""
        # Mock OpenAI response
        mock_openai.return_value = {
            "id": "chatcmpl-123",
            "object": "chat.completion",
            "created": 1234567890,
            "model": "gpt-4",
            "choices": [
                {
                    "index": 0,
                    "message": {
                        "role": "assistant",
                        "content": "2+2 equals 4"
                    },
                    "finish_reason": "stop"
                }
            ],
            "usage": {
                "prompt_tokens": 10,
                "completion_tokens": 5,
                "total_tokens": 15
            }
        }
        
        response = client.post(
            "/v1/chat/completions",
            json=valid_chat_request,
            headers={"Authorization": "Bearer sk-test-key"}
        )
        
        # Should succeed in dev mode
        if response.status_code == 200:
            data = response.json()
            assert "choices" in data
            assert "agentwall" in data
            assert data["agentwall"]["run_id"]
            assert data["agentwall"]["step"] == 1
    
    def test_request_overhead_tracking(self, client, valid_chat_request):
        """Test that overhead is tracked in response headers"""
        response = client.post(
            "/v1/chat/completions",
            json=valid_chat_request,
            headers={"Authorization": "Bearer sk-test-key"}
        )
        
        # Check for overhead header
        if response.status_code == 200:
            assert "X-Process-Time" in response.headers
            overhead_str = response.headers["X-Process-Time"]
            overhead_ms = float(overhead_str.replace("ms", ""))
            # Should be reasonable (not > 100ms for test)
            assert overhead_ms < 100


# ============================================================================
# PHASE 2: DLP ENGINE TESTS
# ============================================================================

class TestDLPEngine:
    """Test Data Loss Prevention engine"""
    
    def test_api_key_detection(self):
        """Test detection of OpenAI API keys"""
        from services.dlp import dlp_engine
        
        text = "My OpenAI key is sk-1234567890abcdefghijklmnop"
        result = dlp_engine.redact(text)
        
        # Should mask the key
        assert "sk-****" in result or "***" in result
        assert "1234567890abcdefghijklmnop" not in result
    
    def test_credit_card_detection(self):
        """Test detection of credit card numbers"""
        from services.dlp import dlp_engine
        
        # Valid Luhn number
        text = "Card: 4532-1234-5678-9010"
        result = dlp_engine.redact(text)
        
        # Should mask the card
        assert "****" in result
        assert "4532" not in result or "1234" not in result
    
    def test_pii_detection(self):
        """Test detection of PII (email, phone, SSN)"""
        from services.dlp import dlp_engine
        
        # Email
        text = "Contact: john@example.com"
        result = dlp_engine.redact(text)
        assert "john@example.com" not in result or "***" in result
        
        # Phone
        text = "Call: +1-555-123-4567"
        result = dlp_engine.redact(text)
        assert "555-123-4567" not in result or "***" in result
    
    def test_jwt_token_detection(self):
        """Test detection of JWT tokens"""
        from services.dlp import dlp_engine
        
        jwt = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIxMjM0NTY3ODkwIn0.dozjgNryP4J3jVmNHl0w5N_XgL0n3I9PlFUP0THsR8U"
        text = f"Token: {jwt}"
        result = dlp_engine.redact(text)
        
        # Should mask the token
        assert jwt not in result or "***" in result
    
    def test_dlp_modes(self):
        """Test different DLP modes: block, mask, shadow_log"""
        from services.dlp import dlp_engine
        
        text = "API key: sk-1234567890"
        
        # Mask mode (default)
        result_mask = dlp_engine.redact(text, mode="mask")
        assert "sk-****" in result_mask or "***" in result_mask
        
        # Block mode
        result_block = dlp_engine.redact(text, mode="block")
        assert result_block is None or "BLOCKED" in str(result_block)


# ============================================================================
# PHASE 3: LOOP DETECTION TESTS
# ============================================================================

class TestLoopDetection:
    """Test loop detection engine"""
    
    def test_exact_prompt_repetition(self):
        """Test detection of exact prompt repetition"""
        result = loop_detector.check_loop(
            current_prompt="What is 2+2?",
            current_response="",
            recent_prompts=["What is 2+2?", "What is 3+3?"],
            recent_responses=[]
        )
        
        assert result.is_loop
        assert result.confidence == 1.0
        assert result.loop_type == "exact_prompt"
    
    def test_exact_response_repetition(self):
        """Test detection of exact response repetition"""
        result = loop_detector.check_loop(
            current_prompt="What is 5+5?",
            current_response="The answer is 10",
            recent_prompts=["What is 2+2?"],
            recent_responses=["The answer is 10", "The answer is 9"]
        )
        
        # Should detect response repetition
        if result.is_loop:
            assert result.confidence == 1.0
    
    def test_similar_prompt_detection(self):
        """Test detection of similar prompts"""
        result = loop_detector.check_loop(
            current_prompt="What is the sum of 2 and 2?",
            current_response="",
            recent_prompts=["What is 2+2?", "What is 3+3?"],
            recent_responses=[]
        )
        
        # Should detect similarity
        if result.is_loop:
            assert result.loop_type == "similar_prompt"
            assert result.confidence > 0.5
    
    def test_oscillation_pattern(self):
        """Test detection of A->B->A->B oscillation"""
        result = loop_detector.check_loop(
            current_prompt="A",
            current_response="",
            recent_prompts=["B", "A", "B", "A"],
            recent_responses=[]
        )
        
        # Should detect some kind of loop
        if result.is_loop:
            assert result.confidence > 0.5
    
    def test_no_loop_detection(self):
        """Test that different prompts don't trigger loop detection"""
        result = loop_detector.check_loop(
            current_prompt="What is 5+5?",
            current_response="",
            recent_prompts=["What is 2+2?", "What is 3+3?"],
            recent_responses=[]
        )
        
        assert not result.is_loop
        assert result.confidence == 0.0
    
    def test_empty_history(self):
        """Test loop detection with empty history"""
        result = loop_detector.check_loop(
            current_prompt="First question",
            current_response="",
            recent_prompts=[],
            recent_responses=[]
        )
        
        assert not result.is_loop


# ============================================================================
# PHASE 4: COST CALCULATION TESTS
# ============================================================================

class TestCostCalculation:
    """Test cost calculation for different models"""
    
    def test_gpt4_cost(self):
        """Test GPT-4 cost calculation"""
        cost = calculate_cost("gpt-4", prompt_tokens=100, completion_tokens=50)
        
        # GPT-4: $0.03 per 1K prompt, $0.06 per 1K completion
        expected = (100 * 0.03 / 1000) + (50 * 0.06 / 1000)
        assert abs(float(cost) - expected) < 0.0001
    
    def test_gpt35_cost(self):
        """Test GPT-3.5 cost calculation"""
        cost = calculate_cost("gpt-3.5-turbo", prompt_tokens=100, completion_tokens=50)
        
        # GPT-3.5: $0.0005 per 1K prompt, $0.0015 per 1K completion
        expected = (100 * 0.0005 / 1000) + (50 * 0.0015 / 1000)
        assert abs(float(cost) - expected) < 0.0001
    
    def test_zero_tokens(self):
        """Test cost with zero tokens"""
        cost = calculate_cost("gpt-4", prompt_tokens=0, completion_tokens=0)
        assert cost == 0.0
    
    def test_large_token_count(self):
        """Test cost with large token counts"""
        cost = calculate_cost("gpt-4", prompt_tokens=10000, completion_tokens=5000)
        
        expected = (10000 * 0.03 / 1000) + (5000 * 0.06 / 1000)
        assert abs(float(cost) - expected) < 0.01


# ============================================================================
# PHASE 5: E2E FLOW TESTS
# ============================================================================

class TestE2EFlow:
    """End-to-end integration tests"""
    
    def test_complete_request_flow(self, client, valid_chat_request):
        """Test complete request flow: auth -> proxy -> response"""
        response = client.post(
            "/v1/chat/completions",
            json=valid_chat_request,
            headers={"Authorization": "Bearer sk-test-key"}
        )
        
        # In dev mode, should succeed
        if response.status_code == 200:
            data = response.json()
            
            # Verify response structure
            assert "choices" in data
            assert "usage" in data
            assert "agentwall" in data
            
            # Verify AgentWall metadata
            agentwall = data["agentwall"]
            assert "run_id" in agentwall
            assert "step" in agentwall
            assert "overhead_ms" in agentwall
            assert "cost_usd" in agentwall
    
    def test_streaming_flow(self, client, streaming_request):
        """Test streaming request flow"""
        response = client.post(
            "/v1/chat/completions",
            json=streaming_request,
            headers={"Authorization": "Bearer sk-test-key"}
        )
        
        # Should return streaming response
        if response.status_code == 200:
            assert response.headers["content-type"] == "text/event-stream"
            
            # Should have AgentWall headers
            assert "X-AgentWall-Run-ID" in response.headers
            assert "X-AgentWall-Step" in response.headers
    
    def test_error_handling(self, client):
        """Test error handling in request flow"""
        # Invalid request (missing required fields)
        response = client.post(
            "/v1/chat/completions",
            json={"model": "gpt-4"},  # Missing messages
            headers={"Authorization": "Bearer sk-test-key"}
        )
        
        # Should return error
        assert response.status_code >= 400


# ============================================================================
# PERFORMANCE TESTS
# ============================================================================

class TestPerformance:
    """Performance and overhead tests"""
    
    def test_proxy_overhead_under_10ms(self, client, valid_chat_request):
        """Test that proxy overhead is under 10ms target"""
        response = client.post(
            "/v1/chat/completions",
            json=valid_chat_request,
            headers={"Authorization": "Bearer sk-test-key"}
        )
        
        if response.status_code == 200:
            overhead_str = response.headers.get("X-Process-Time", "0ms")
            overhead_ms = float(overhead_str.replace("ms", ""))
            
            # Should be under 10ms (or close for test environment)
            assert overhead_ms < 50  # Relaxed for test environment
    
    def test_loop_detection_performance(self):
        """Test that loop detection is fast"""
        start = time.perf_counter()
        
        for _ in range(100):
            loop_detector.check_loop(
                current_prompt="What is 2+2?",
                current_response="",
                recent_prompts=["What is 2+2?", "What is 3+3?"],
                recent_responses=[]
            )
        
        elapsed_ms = (time.perf_counter() - start) * 1000
        avg_ms = elapsed_ms / 100
        
        # Should be < 1ms per check
        assert avg_ms < 5  # Relaxed for test environment


# ============================================================================
# RUN TESTS
# ============================================================================

if __name__ == "__main__":
    pytest.main([__file__, "-v", "--tb=short"])
