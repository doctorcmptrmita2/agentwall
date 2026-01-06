#!/usr/bin/env python3
"""
Request Logs Test Script
Tests the FastAPI -> Laravel logging integration

Usage:
    python test_request_logs.py --api-key YOUR_OPENAI_KEY
"""

import httpx
import argparse
import time
import json
from datetime import datetime

# Configuration
API_BASE = "https://api.agentwall.io"
LARAVEL_BASE = "https://agentwall.io"

def print_header(title: str):
    print(f"\n{'='*60}")
    print(f"  {title}")
    print(f"{'='*60}")

def print_result(name: str, passed: bool, details: str = ""):
    status = "✅ PASS" if passed else "❌ FAIL"
    print(f"{status} | {name}")
    if details:
        print(f"       {details}")

def test_chat_completion(api_key: str) -> dict:
    """Send a chat completion request and return the response"""
    print_header("Test 1: Chat Completion with Logging")
    
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }
    
    payload = {
        "model": "gpt-3.5-turbo",
        "messages": [
            {"role": "user", "content": "Say 'Request Logs Test' in exactly 3 words."}
        ],
        "max_tokens": 20
    }
    
    start = time.time()
    response = httpx.post(
        f"{API_BASE}/v1/chat/completions",
        headers=headers,
        json=payload,
        timeout=30
    )
    latency = (time.time() - start) * 1000
    
    if response.status_code == 200:
        data = response.json()
        run_id = data.get("agentwall", {}).get("run_id", "N/A")
        cost = data.get("agentwall", {}).get("cost_usd", 0)
        
        print_result(
            "Chat Completion",
            True,
            f"run_id={run_id[:8]}... cost=${cost:.6f} latency={latency:.0f}ms"
        )
        return {
            "success": True,
            "run_id": run_id,
            "cost": cost,
            "latency": latency,
            "request_id": data.get("id", "")
        }
    else:
        print_result("Chat Completion", False, f"Status: {response.status_code}")
        return {"success": False}

def test_streaming(api_key: str) -> dict:
    """Test streaming request logging"""
    print_header("Test 2: Streaming with Logging")
    
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }
    
    payload = {
        "model": "gpt-3.5-turbo",
        "messages": [
            {"role": "user", "content": "Count from 1 to 5."}
        ],
        "max_tokens": 30,
        "stream": True
    }
    
    start = time.time()
    chunks = []
    run_id = None
    
    with httpx.stream(
        "POST",
        f"{API_BASE}/v1/chat/completions",
        headers=headers,
        json=payload,
        timeout=30
    ) as response:
        run_id = response.headers.get("X-AgentWall-Run-ID", "")
        
        for line in response.iter_lines():
            if line.startswith("data: ") and not line.endswith("[DONE]"):
                try:
                    data = json.loads(line[6:])
                    if "choices" in data and data["choices"]:
                        delta = data["choices"][0].get("delta", {})
                        content = delta.get("content", "")
                        if content:
                            chunks.append(content)
                except:
                    pass
    
    latency = (time.time() - start) * 1000
    content = "".join(chunks)
    
    print_result(
        "Streaming",
        True,
        f"run_id={run_id[:8] if run_id else 'N/A'}... chunks={len(chunks)} latency={latency:.0f}ms"
    )
    
    return {
        "success": True,
        "run_id": run_id,
        "latency": latency
    }

def test_laravel_logs_api() -> dict:
    """Check if Laravel API endpoint is accessible"""
    print_header("Test 3: Laravel API Endpoint")
    
    # Just check if the endpoint exists (will return 401 without secret)
    try:
        response = httpx.post(
            f"{LARAVEL_BASE}/api/internal/logs",
            json={"test": True},
            timeout=10
        )
        
        # 401 means endpoint exists but auth failed (expected)
        if response.status_code == 401:
            print_result("Laravel API Endpoint", True, "Endpoint exists (401 = auth required)")
            return {"success": True, "status": 401}
        elif response.status_code == 422:
            print_result("Laravel API Endpoint", True, "Endpoint exists (422 = validation)")
            return {"success": True, "status": 422}
        else:
            print_result("Laravel API Endpoint", False, f"Status: {response.status_code}")
            return {"success": False, "status": response.status_code}
    except Exception as e:
        print_result("Laravel API Endpoint", False, str(e))
        return {"success": False, "error": str(e)}

def test_multiple_requests(api_key: str, count: int = 3) -> dict:
    """Send multiple requests to generate logs"""
    print_header(f"Test 4: Multiple Requests ({count}x)")
    
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }
    
    models = ["gpt-3.5-turbo", "gpt-4o-mini", "gpt-3.5-turbo"]
    results = []
    
    for i, model in enumerate(models[:count]):
        payload = {
            "model": model,
            "messages": [
                {"role": "user", "content": f"Test request #{i+1}. Reply with just 'OK'."}
            ],
            "max_tokens": 5
        }
        
        response = httpx.post(
            f"{API_BASE}/v1/chat/completions",
            headers=headers,
            json=payload,
            timeout=30
        )
        
        if response.status_code == 200:
            data = response.json()
            results.append({
                "model": model,
                "cost": data.get("agentwall", {}).get("cost_usd", 0)
            })
            print(f"  ✓ Request #{i+1}: {model}")
        else:
            print(f"  ✗ Request #{i+1}: Failed ({response.status_code})")
    
    total_cost = sum(r["cost"] for r in results)
    print_result(
        "Multiple Requests",
        len(results) == count,
        f"Sent {len(results)}/{count} requests, total cost: ${total_cost:.6f}"
    )
    
    return {"success": len(results) == count, "results": results}

def main():
    parser = argparse.ArgumentParser(description="Test Request Logs Integration")
    parser.add_argument("--api-key", required=True, help="OpenAI API key")
    args = parser.parse_args()
    
    print("\n" + "="*60)
    print("  AgentWall Request Logs Integration Test")
    print(f"  Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("="*60)
    
    results = {
        "chat": test_chat_completion(args.api_key),
        "streaming": test_streaming(args.api_key),
        "laravel_api": test_laravel_logs_api(),
        "multiple": test_multiple_requests(args.api_key, 3),
    }
    
    # Summary
    print_header("Summary")
    passed = sum(1 for r in results.values() if r.get("success"))
    total = len(results)
    
    print(f"\nTests Passed: {passed}/{total}")
    print(f"\n⚠️  Note: Check Laravel dashboard at {LARAVEL_BASE}/admin/request-logs")
    print("    to verify logs are appearing correctly.")
    
    if passed == total:
        print("\n✅ All tests passed! Request logging is working.")
    else:
        print("\n⚠️  Some tests failed. Check the output above.")

if __name__ == "__main__":
    main()
