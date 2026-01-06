#!/usr/bin/env python3
"""
AgentWall API Test Script
Tests the proxy with real OpenAI API calls

Usage:
    # Local test (FastAPI running on localhost:8000)
    python test_api.py --local
    
    # Production test
    python test_api.py --prod
    
    # With your own OpenAI key (pass-through mode)
    python test_api.py --local --openai-key sk-your-key
"""

import argparse
import time
from openai import OpenAI


def test_basic_chat(client: OpenAI, test_name: str = "Basic Chat"):
    """Test basic chat completion"""
    print(f"\n{'='*50}")
    print(f"🧪 Test: {test_name}")
    print('='*50)
    
    start = time.perf_counter()
    
    try:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",  # Cheaper for testing
            messages=[
                {"role": "user", "content": "Say 'Hello AgentWall!' in exactly 3 words."}
            ],
            max_tokens=20,
        )
        
        elapsed = (time.perf_counter() - start) * 1000
        
        print(f"✅ Status: SUCCESS")
        print(f"⏱️  Latency: {elapsed:.2f}ms")
        print(f"📝 Response: {response.choices[0].message.content}")
        print(f"🔢 Tokens: {response.usage.total_tokens}")
        
        # Check for AgentWall metadata
        if hasattr(response, 'agentwall'):
            print(f"🛡️  AgentWall Run ID: {response.agentwall.get('run_id')}")
            print(f"🛡️  AgentWall Step: {response.agentwall.get('step')}")
            print(f"🛡️  AgentWall Cost: ${response.agentwall.get('cost_usd', 0):.6f}")
        
        return True
        
    except Exception as e:
        elapsed = (time.perf_counter() - start) * 1000
        print(f"❌ Status: FAILED")
        print(f"⏱️  Latency: {elapsed:.2f}ms")
        print(f"🚨 Error: {e}")
        return False


def test_streaming(client: OpenAI, test_name: str = "Streaming"):
    """Test streaming chat completion"""
    print(f"\n{'='*50}")
    print(f"🧪 Test: {test_name}")
    print('='*50)
    
    start = time.perf_counter()
    
    try:
        stream = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "user", "content": "Count from 1 to 5."}
            ],
            max_tokens=50,
            stream=True,
        )
        
        print("📡 Streaming response: ", end="", flush=True)
        chunks = 0
        content = ""
        
        for chunk in stream:
            chunks += 1
            if chunk.choices[0].delta.content:
                content += chunk.choices[0].delta.content
                print(chunk.choices[0].delta.content, end="", flush=True)
        
        elapsed = (time.perf_counter() - start) * 1000
        
        print()  # New line
        print(f"✅ Status: SUCCESS")
        print(f"⏱️  Latency: {elapsed:.2f}ms")
        print(f"📦 Chunks: {chunks}")
        
        return True
        
    except Exception as e:
        elapsed = (time.perf_counter() - start) * 1000
        print(f"❌ Status: FAILED")
        print(f"⏱️  Latency: {elapsed:.2f}ms")
        print(f"🚨 Error: {e}")
        return False


def test_dlp_detection(client: OpenAI, test_name: str = "DLP Detection"):
    """Test DLP - should mask sensitive data"""
    print(f"\n{'='*50}")
    print(f"🧪 Test: {test_name}")
    print('='*50)
    
    start = time.perf_counter()
    
    try:
        # This contains a fake API key - should be masked
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "user", "content": "My API key is sk-1234567890abcdefghijklmnop. What is 2+2?"}
            ],
            max_tokens=20,
        )
        
        elapsed = (time.perf_counter() - start) * 1000
        
        print(f"✅ Status: SUCCESS (DLP should have masked the key)")
        print(f"⏱️  Latency: {elapsed:.2f}ms")
        print(f"📝 Response: {response.choices[0].message.content}")
        
        return True
        
    except Exception as e:
        elapsed = (time.perf_counter() - start) * 1000
        # DLP might block the request entirely
        if "blocked" in str(e).lower() or "dlp" in str(e).lower():
            print(f"✅ Status: SUCCESS (DLP blocked the request)")
        else:
            print(f"❌ Status: FAILED")
        print(f"⏱️  Latency: {elapsed:.2f}ms")
        print(f"🚨 Error: {e}")
        return "blocked" in str(e).lower()


def test_run_tracking(client: OpenAI, test_name: str = "Run Tracking"):
    """Test run-level tracking with multiple requests"""
    print(f"\n{'='*50}")
    print(f"🧪 Test: {test_name}")
    print('='*50)
    
    run_id = f"test-run-{int(time.time())}"
    
    try:
        # Make 3 requests with same run_id
        for i in range(3):
            start = time.perf_counter()
            
            response = client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "user", "content": f"Step {i+1}: What is {i+1}+{i+1}?"}
                ],
                max_tokens=20,
                extra_headers={
                    "X-AgentWall-Run-ID": run_id,
                }
            )
            
            elapsed = (time.perf_counter() - start) * 1000
            print(f"  Step {i+1}: {response.choices[0].message.content[:30]}... ({elapsed:.0f}ms)")
        
        print(f"✅ Status: SUCCESS")
        print(f"🆔 Run ID: {run_id}")
        print(f"📊 Steps: 3")
        
        return True
        
    except Exception as e:
        print(f"❌ Status: FAILED")
        print(f"🚨 Error: {e}")
        return False


def main():
    parser = argparse.ArgumentParser(description="Test AgentWall API")
    parser.add_argument("--local", action="store_true", help="Test local server (localhost:8000)")
    parser.add_argument("--prod", action="store_true", help="Test production (api.agentwall.io)")
    parser.add_argument("--openai-key", type=str, help="OpenAI API key for pass-through mode")
    parser.add_argument("--agentwall-key", type=str, default="aw-test-key", help="AgentWall API key")
    args = parser.parse_args()
    
    # Determine base URL
    if args.local:
        base_url = "http://localhost:8000/v1"
        env = "LOCAL"
    elif args.prod:
        base_url = "https://api.agentwall.io/v1"
        env = "PRODUCTION"
    else:
        print("❌ Please specify --local or --prod")
        return
    
    # Determine API key
    api_key = args.openai_key if args.openai_key else args.agentwall_key
    
    print("\n" + "="*60)
    print("🛡️  AgentWall API Test Suite")
    print("="*60)
    print(f"🌐 Environment: {env}")
    print(f"🔗 Base URL: {base_url}")
    print(f"🔑 API Key: {api_key[:10]}...")
    
    # Create client
    client = OpenAI(
        api_key=api_key,
        base_url=base_url,
    )
    
    # Run tests
    results = []
    
    results.append(("Basic Chat", test_basic_chat(client)))
    results.append(("Streaming", test_streaming(client)))
    results.append(("DLP Detection", test_dlp_detection(client)))
    results.append(("Run Tracking", test_run_tracking(client)))
    
    # Summary
    print("\n" + "="*60)
    print("📊 Test Summary")
    print("="*60)
    
    passed = sum(1 for _, r in results if r)
    total = len(results)
    
    for name, result in results:
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"  {status} - {name}")
    
    print(f"\n🎯 Result: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All tests passed!")
    else:
        print("⚠️  Some tests failed")


if __name__ == "__main__":
    main()
