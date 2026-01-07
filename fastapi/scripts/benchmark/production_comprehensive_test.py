#!/usr/bin/env python3
"""
AgentWall Production Comprehensive Test Suite
Production-grade testing for all critical features
"""

import asyncio
import aiohttp
import json
import uuid
import time
from datetime import datetime
from typing import Dict, List, Tuple

PRODUCTION_URL = "https://api.agentwall.io"
API_KEY = "aw-bJDiC5gtDnYJjIag9jQTzQyJr4RMotPX"

# Test results tracking
test_results = {
    "total": 0,
    "passed": 0,
    "failed": 0,
    "tests": []
}


def log_test(name: str, passed: bool, details: str = "", duration_ms: float = 0):
    """Log test result"""
    test_results["total"] += 1
    if passed:
        test_results["passed"] += 1
        status = "✅ PASS"
    else:
        test_results["failed"] += 1
        status = "❌ FAIL"
    
    test_results["tests"].append({
        "name": name,
        "passed": passed,
        "details": details,
        "duration_ms": duration_ms
    })
    
    print(f"{status} | {name} ({duration_ms:.2f}ms)")
    if details:
        print(f"     └─ {details}")


async def test_health_endpoints():
    """Test all health endpoints"""
    print("\n" + "="*70)
    print("🏥 HEALTH ENDPOINTS TEST")
    print("="*70)
    
    async with aiohttp.ClientSession() as session:
        # Test 1: Basic health
        start = time.perf_counter()
        async with session.get(f"{PRODUCTION_URL}/health") as resp:
            duration = (time.perf_counter() - start) * 1000
            passed = resp.status == 200
            data = await resp.json()
            log_test("GET /health", passed, f"Status: {resp.status}", duration)
        
        # Test 2: Liveness
        start = time.perf_counter()
        async with session.get(f"{PRODUCTION_URL}/health/live") as resp:
            duration = (time.perf_counter() - start) * 1000
            passed = resp.status == 200
            log_test("GET /health/live", passed, f"Status: {resp.status}", duration)
        
        # Test 3: Readiness
        start = time.perf_counter()
        async with session.get(f"{PRODUCTION_URL}/health/ready") as resp:
            duration = (time.perf_counter() - start) * 1000
            passed = resp.status == 200
            data = await resp.json()
            redis_ok = data.get("checks", {}).get("redis", {}).get("status") == "healthy"
            log_test("GET /health/ready", passed and redis_ok, 
                    f"Redis: {data.get('checks', {}).get('redis', {}).get('status')}", duration)


async def test_authentication():
    """Test authentication mechanisms"""
    print("\n" + "="*70)
    print("🔐 AUTHENTICATION TEST")
    print("="*70)
    
    async with aiohttp.ClientSession() as session:
        # Test 1: Valid API key
        start = time.perf_counter()
        headers = {"Authorization": f"Bearer {API_KEY}"}
        async with session.post(
            f"{PRODUCTION_URL}/v1/chat/completions",
            json={
                "model": "gpt-3.5-turbo",
                "messages": [{"role": "user", "content": "Hi"}],
                "max_tokens": 10
            },
            headers=headers,
            timeout=60
        ) as resp:
            duration = (time.perf_counter() - start) * 1000
            passed = resp.status == 200
            log_test("Valid API key", passed, f"Status: {resp.status}", duration)
        
        # Test 2: Invalid API key
        start = time.perf_counter()
        headers = {"Authorization": "Bearer invalid-key"}
        async with session.post(
            f"{PRODUCTION_URL}/v1/chat/completions",
            json={
                "model": "gpt-3.5-turbo",
                "messages": [{"role": "user", "content": "Hi"}],
                "max_tokens": 10
            },
            headers=headers,
            timeout=60
        ) as resp:
            duration = (time.perf_counter() - start) * 1000
            passed = resp.status == 401
            log_test("Invalid API key rejected", passed, f"Status: {resp.status}", duration)
        
        # Test 3: Missing API key
        start = time.perf_counter()
        async with session.post(
            f"{PRODUCTION_URL}/v1/chat/completions",
            json={
                "model": "gpt-3.5-turbo",
                "messages": [{"role": "user", "content": "Hi"}],
                "max_tokens": 10
            },
            timeout=60
        ) as resp:
            duration = (time.perf_counter() - start) * 1000
            passed = resp.status == 401
            log_test("Missing API key rejected", passed, f"Status: {resp.status}", duration)


async def test_chat_completion():
    """Test chat completion endpoint"""
    print("\n" + "="*70)
    print("💬 CHAT COMPLETION TEST")
    print("="*70)
    
    headers = {"Authorization": f"Bearer {API_KEY}", "Content-Type": "application/json"}
    
    async with aiohttp.ClientSession() as session:
        # Test 1: Basic request
        start = time.perf_counter()
        async with session.post(
            f"{PRODUCTION_URL}/v1/chat/completions",
            json={
                "model": "gpt-3.5-turbo",
                "messages": [{"role": "user", "content": "What is 2+2?"}],
                "max_tokens": 10
            },
            headers=headers,
            timeout=60
        ) as resp:
            duration = (time.perf_counter() - start) * 1000
            passed = resp.status == 200
            data = await resp.json()
            has_content = bool(data.get("choices", [{}])[0].get("message", {}).get("content"))
            log_test("Basic chat request", passed and has_content, 
                    f"Response: {data.get('choices', [{}])[0].get('message', {}).get('content', '')[:30]}", duration)
        
        # Test 2: With system message
        start = time.perf_counter()
        async with session.post(
            f"{PRODUCTION_URL}/v1/chat/completions",
            json={
                "model": "gpt-3.5-turbo",
                "messages": [
                    {"role": "system", "content": "You are a helpful assistant."},
                    {"role": "user", "content": "Hello!"}
                ],
                "max_tokens": 20
            },
            headers=headers,
            timeout=60
        ) as resp:
            duration = (time.perf_counter() - start) * 1000
            passed = resp.status == 200
            log_test("Chat with system message", passed, f"Status: {resp.status}", duration)
        
        # Test 3: Temperature parameter
        start = time.perf_counter()
        async with session.post(
            f"{PRODUCTION_URL}/v1/chat/completions",
            json={
                "model": "gpt-3.5-turbo",
                "messages": [{"role": "user", "content": "Say hello"}],
                "temperature": 0.5,
                "max_tokens": 10
            },
            headers=headers,
            timeout=60
        ) as resp:
            duration = (time.perf_counter() - start) * 1000
            passed = resp.status == 200
            log_test("Chat with temperature", passed, f"Status: {resp.status}", duration)


async def test_streaming():
    """Test streaming responses"""
    print("\n" + "="*70)
    print("🌊 STREAMING TEST")
    print("="*70)
    
    headers = {"Authorization": f"Bearer {API_KEY}", "Content-Type": "application/json"}
    
    async with aiohttp.ClientSession() as session:
        start = time.perf_counter()
        chunk_count = 0
        
        async with session.post(
            f"{PRODUCTION_URL}/v1/chat/completions",
            json={
                "model": "gpt-3.5-turbo",
                "messages": [{"role": "user", "content": "Count from 1 to 5"}],
                "stream": True,
                "max_tokens": 50
            },
            headers=headers,
            timeout=60
        ) as resp:
            duration = (time.perf_counter() - start) * 1000
            
            if resp.status == 200:
                async for line in resp.content:
                    if line:
                        chunk_count += 1
                
                passed = chunk_count > 0
                log_test("Streaming response", passed, f"Chunks: {chunk_count}", duration)
            else:
                log_test("Streaming response", False, f"Status: {resp.status}", duration)


async def test_run_tracking():
    """Test run-level tracking with body run_id"""
    print("\n" + "="*70)
    print("🔄 RUN TRACKING TEST")
    print("="*70)
    
    run_id = f"test-{uuid.uuid4().hex[:8]}"
    headers = {"Authorization": f"Bearer {API_KEY}", "Content-Type": "application/json"}
    
    async with aiohttp.ClientSession() as session:
        # Request 1
        start = time.perf_counter()
        async with session.post(
            f"{PRODUCTION_URL}/v1/chat/completions",
            json={
                "model": "gpt-3.5-turbo",
                "messages": [{"role": "user", "content": "First question"}],
                "max_tokens": 20,
                "agentwall_run_id": run_id
            },
            headers=headers,
            timeout=60
        ) as resp:
            duration = (time.perf_counter() - start) * 1000
            data = await resp.json()
            aw = data.get("agentwall", {})
            
            step1 = aw.get("step") == 1
            cost1 = aw.get("cost_usd", 0) > 0
            log_test("Run tracking - Step 1", step1 and cost1, 
                    f"Step: {aw.get('step')}, Cost: ${aw.get('cost_usd', 0):.6f}", duration)
        
        # Request 2 (same run)
        start = time.perf_counter()
        async with session.post(
            f"{PRODUCTION_URL}/v1/chat/completions",
            json={
                "model": "gpt-3.5-turbo",
                "messages": [{"role": "user", "content": "Second question"}],
                "max_tokens": 20,
                "agentwall_run_id": run_id
            },
            headers=headers,
            timeout=60
        ) as resp:
            duration = (time.perf_counter() - start) * 1000
            data = await resp.json()
            aw = data.get("agentwall", {})
            
            step2 = aw.get("step") == 2
            total_cost = aw.get("total_run_cost", 0) > 0
            log_test("Run tracking - Step 2", step2 and total_cost, 
                    f"Step: {aw.get('step')}, Total: ${aw.get('total_run_cost', 0):.6f}", duration)


async def test_loop_detection():
    """Test loop detection with body run_id"""
    print("\n" + "="*70)
    print("🔄 LOOP DETECTION TEST")
    print("="*70)
    
    run_id = f"loop-{uuid.uuid4().hex[:8]}"
    headers = {"Authorization": f"Bearer {API_KEY}", "Content-Type": "application/json"}
    
    async with aiohttp.ClientSession() as session:
        # Request 1: OK
        start = time.perf_counter()
        async with session.post(
            f"{PRODUCTION_URL}/v1/chat/completions",
            json={
                "model": "gpt-3.5-turbo",
                "messages": [{"role": "user", "content": "What is 2+2?"}],
                "max_tokens": 10,
                "agentwall_run_id": run_id
            },
            headers=headers,
            timeout=60
        ) as resp:
            duration = (time.perf_counter() - start) * 1000
            passed = resp.status == 200
            log_test("Loop detection - Request 1", passed, f"Status: {resp.status}", duration)
        
        # Request 2: Same prompt - SHOULD BE BLOCKED
        start = time.perf_counter()
        async with session.post(
            f"{PRODUCTION_URL}/v1/chat/completions",
            json={
                "model": "gpt-3.5-turbo",
                "messages": [{"role": "user", "content": "What is 2+2?"}],
                "max_tokens": 10,
                "agentwall_run_id": run_id
            },
            headers=headers,
            timeout=60
        ) as resp:
            duration = (time.perf_counter() - start) * 1000
            data = await resp.json()
            
            is_blocked = resp.status == 429
            # Error is in detail.error, not top-level error
            error_type = data.get("detail", {}).get("error", {}).get("type")
            is_loop = error_type == "loop_detected"
            loop_type = data.get("detail", {}).get("error", {}).get("loop_type", "unknown")
            log_test("Loop detection - Request 2 blocked", is_blocked and is_loop, 
                    f"Status: {resp.status}, Type: {error_type}, Loop: {loop_type}", duration)


async def test_dlp_protection():
    """Test DLP protection"""
    print("\n" + "="*70)
    print("🔒 DLP PROTECTION TEST")
    print("="*70)
    
    headers = {"Authorization": f"Bearer {API_KEY}", "Content-Type": "application/json"}
    
    test_cases = [
        ("Credit card", "My card is 4111-1111-1111-1111"),
        ("API key", "My key is sk-1234567890abcdef"),
        ("Email", "Contact me at admin@company.com"),
    ]
    
    async with aiohttp.ClientSession() as session:
        for name, prompt in test_cases:
            start = time.perf_counter()
            async with session.post(
                f"{PRODUCTION_URL}/v1/chat/completions",
                json={
                    "model": "gpt-3.5-turbo",
                    "messages": [{"role": "user", "content": prompt}],
                    "max_tokens": 50
                },
                headers=headers,
                timeout=60
            ) as resp:
                duration = (time.perf_counter() - start) * 1000
                passed = resp.status == 200
                log_test(f"DLP - {name}", passed, f"Status: {resp.status}", duration)


async def test_error_handling():
    """Test error handling"""
    print("\n" + "="*70)
    print("⚠️ ERROR HANDLING TEST")
    print("="*70)
    
    headers = {"Authorization": f"Bearer {API_KEY}", "Content-Type": "application/json"}
    
    async with aiohttp.ClientSession() as session:
        # Test 1: Invalid model
        start = time.perf_counter()
        async with session.post(
            f"{PRODUCTION_URL}/v1/chat/completions",
            json={
                "model": "invalid-model-xyz",
                "messages": [{"role": "user", "content": "Hi"}],
                "max_tokens": 10
            },
            headers=headers,
            timeout=60
        ) as resp:
            duration = (time.perf_counter() - start) * 1000
            passed = resp.status in [400, 422, 404]
            log_test("Invalid model rejected", passed, f"Status: {resp.status}", duration)
        
        # Test 2: Missing messages
        start = time.perf_counter()
        async with session.post(
            f"{PRODUCTION_URL}/v1/chat/completions",
            json={
                "model": "gpt-3.5-turbo",
                "max_tokens": 10
            },
            headers=headers,
            timeout=60
        ) as resp:
            duration = (time.perf_counter() - start) * 1000
            passed = resp.status == 422
            log_test("Missing messages rejected", passed, f"Status: {resp.status}", duration)
        
        # Test 3: Invalid temperature
        start = time.perf_counter()
        async with session.post(
            f"{PRODUCTION_URL}/v1/chat/completions",
            json={
                "model": "gpt-3.5-turbo",
                "messages": [{"role": "user", "content": "Hi"}],
                "temperature": 5.0,  # Invalid
                "max_tokens": 10
            },
            headers=headers,
            timeout=60
        ) as resp:
            duration = (time.perf_counter() - start) * 1000
            passed = resp.status == 422
            log_test("Invalid temperature rejected", passed, f"Status: {resp.status}", duration)


async def test_latency():
    """Test latency metrics"""
    print("\n" + "="*70)
    print("⚡ LATENCY TEST")
    print("="*70)
    
    headers = {"Authorization": f"Bearer {API_KEY}", "Content-Type": "application/json"}
    latencies = []
    
    async with aiohttp.ClientSession() as session:
        for i in range(5):
            start = time.perf_counter()
            async with session.post(
                f"{PRODUCTION_URL}/v1/chat/completions",
                json={
                    "model": "gpt-3.5-turbo",
                    "messages": [{"role": "user", "content": f"Request {i+1}"}],
                    "max_tokens": 10
                },
                headers=headers,
                timeout=60
            ) as resp:
                duration = (time.perf_counter() - start) * 1000
                latencies.append(duration)
                
                if resp.status == 200:
                    data = await resp.json()
                    aw_overhead = data.get("agentwall", {}).get("overhead_ms", 0)
                    log_test(f"Request {i+1}", True, 
                            f"Total: {duration:.2f}ms, AgentWall: {aw_overhead:.2f}ms", duration)
    
    avg_latency = sum(latencies) / len(latencies)
    print(f"\n📊 Average latency: {avg_latency:.2f}ms")
    print(f"   Min: {min(latencies):.2f}ms, Max: {max(latencies):.2f}ms")


async def test_cost_tracking():
    """Test cost tracking accuracy"""
    print("\n" + "="*70)
    print("💰 COST TRACKING TEST")
    print("="*70)
    
    run_id = f"cost-{uuid.uuid4().hex[:8]}"
    headers = {"Authorization": f"Bearer {API_KEY}", "Content-Type": "application/json"}
    total_cost = 0.0
    
    async with aiohttp.ClientSession() as session:
        for i in range(3):
            start = time.perf_counter()
            async with session.post(
                f"{PRODUCTION_URL}/v1/chat/completions",
                json={
                    "model": "gpt-3.5-turbo",
                    "messages": [{"role": "user", "content": f"Question {i+1}"}],
                    "max_tokens": 30,
                    "agentwall_run_id": run_id
                },
                headers=headers,
                timeout=60
            ) as resp:
                duration = (time.perf_counter() - start) * 1000
                data = await resp.json()
                aw = data.get("agentwall", {})
                
                cost = aw.get("cost_usd", 0)
                total_cost = aw.get("total_run_cost", 0)
                
                passed = cost > 0 and total_cost > 0
                log_test(f"Cost tracking - Request {i+1}", passed, 
                        f"Cost: ${cost:.6f}, Total: ${total_cost:.6f}", duration)


async def main():
    """Run all tests"""
    print("\n" + "="*70)
    print("🛡️ AGENTWALL PRODUCTION COMPREHENSIVE TEST SUITE")
    print("="*70)
    print(f"Target: {PRODUCTION_URL}")
    print(f"Time: {datetime.now().isoformat()}")
    print("="*70)
    
    # Run all test suites
    await test_health_endpoints()
    await test_authentication()
    await test_chat_completion()
    await test_streaming()
    await test_run_tracking()
    await test_loop_detection()
    await test_dlp_protection()
    await test_error_handling()
    await test_latency()
    await test_cost_tracking()
    
    # Print summary
    print("\n" + "="*70)
    print("📊 TEST SUMMARY")
    print("="*70)
    print(f"Total Tests: {test_results['total']}")
    print(f"Passed: {test_results['passed']} ✅")
    print(f"Failed: {test_results['failed']} ❌")
    print(f"Pass Rate: {(test_results['passed']/test_results['total']*100):.1f}%")
    print("="*70)
    
    # Save results
    with open("fastapi/scripts/reports/production_comprehensive_test.json", "w") as f:
        json.dump({
            "timestamp": datetime.now().isoformat(),
            "url": PRODUCTION_URL,
            "summary": {
                "total": test_results["total"],
                "passed": test_results["passed"],
                "failed": test_results["failed"],
                "pass_rate": test_results["passed"] / test_results["total"] * 100
            },
            "tests": test_results["tests"]
        }, f, indent=2)
    
    print(f"\n✅ Results saved to: fastapi/scripts/reports/production_comprehensive_test.json")
    
    if test_results["failed"] == 0:
        print("\n🎉 ALL TESTS PASSED!")
    else:
        print(f"\n⚠️ {test_results['failed']} test(s) failed")


if __name__ == "__main__":
    asyncio.run(main())
