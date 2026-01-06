#!/usr/bin/env python3
"""
AgentWall Production DLP Deep Test
DLP'nin gerçekten maskeleme yapıp yapmadığını test eder
"""

import asyncio
import aiohttp
import json
from datetime import datetime

PRODUCTION_URL = "https://api.agentwall.io"
API_KEY = "aw-bJDiC5gtDnYJjIag9jQTzQyJr4RMotPX"


async def test_dlp_masking():
    """DLP maskeleme testleri"""
    print("\n" + "="*70)
    print("🛡️ AGENTWALL DLP DEEP TEST")
    print("="*70)
    
    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json"
    }
    
    test_cases = [
        {
            "name": "Credit Card in Prompt",
            "prompt": "Remember my card: 4111-1111-1111-1111 for later",
            "sensitive_data": "4111-1111-1111-1111"
        },
        {
            "name": "OpenAI API Key",
            "prompt": "Use this API key: sk-1234567890abcdefghijklmnopqrstuvwxyz",
            "sensitive_data": "sk-1234567890abcdefghijklmnopqrstuvwxyz"
        },
        {
            "name": "Email Address",
            "prompt": "Send report to ceo@secretcompany.com please",
            "sensitive_data": "ceo@secretcompany.com"
        },
        {
            "name": "Phone Number",
            "prompt": "Call me at +1-555-123-4567 tomorrow",
            "sensitive_data": "555-123-4567"
        },
        {
            "name": "AWS Key",
            "prompt": "AWS key is AKIAIOSFODNN7EXAMPLE",
            "sensitive_data": "AKIAIOSFODNN7EXAMPLE"
        },
    ]
    
    async with aiohttp.ClientSession() as session:
        for test in test_cases:
            print(f"\n📋 Testing: {test['name']}")
            print(f"   Input: {test['prompt'][:50]}...")
            
            payload = {
                "model": "gpt-3.5-turbo",
                "messages": [
                    {"role": "user", "content": test["prompt"]}
                ],
                "max_tokens": 100
            }
            
            try:
                async with session.post(
                    f"{PRODUCTION_URL}/v1/chat/completions",
                    json=payload,
                    headers=headers,
                    timeout=60
                ) as resp:
                    if resp.status == 200:
                        data = await resp.json()
                        
                        # Check headers for DLP info
                        dlp_action = resp.headers.get("X-AgentWall-DLP-Action", "none")
                        dlp_matches = resp.headers.get("X-AgentWall-DLP-Matches", "0")
                        run_id = resp.headers.get("X-AgentWall-Run-ID", "N/A")
                        
                        # Check if sensitive data appears in response
                        response_content = json.dumps(data)
                        data_leaked = test["sensitive_data"] in response_content
                        
                        # Get the actual response
                        assistant_msg = data.get("choices", [{}])[0].get("message", {}).get("content", "")
                        
                        print(f"   Status: {resp.status}")
                        print(f"   DLP Action: {dlp_action}")
                        print(f"   DLP Matches: {dlp_matches}")
                        print(f"   Run ID: {run_id}")
                        print(f"   Data Leaked: {'❌ YES' if data_leaked else '✅ NO'}")
                        print(f"   Response: {assistant_msg[:100]}...")
                        
                        # Check AgentWall metadata
                        if "agentwall" in data:
                            aw = data["agentwall"]
                            print(f"   AgentWall Metadata:")
                            print(f"      - Run ID: {aw.get('run_id', 'N/A')}")
                            print(f"      - Step: {aw.get('step', 'N/A')}")
                            print(f"      - Cost: ${aw.get('cost_usd', 0):.6f}")
                            print(f"      - Overhead: {aw.get('overhead_ms', 'N/A')}ms")
                    else:
                        error = await resp.text()
                        print(f"   ❌ Error {resp.status}: {error[:200]}")
                        
            except Exception as e:
                print(f"   ❌ Exception: {e}")
    
    print("\n" + "="*70)
    print("✅ DLP Deep Test Complete")
    print("="*70)


async def test_loop_detection():
    """Loop detection testi - aynı prompt'u tekrar gönder"""
    print("\n" + "="*70)
    print("🔄 AGENTWALL LOOP DETECTION TEST")
    print("="*70)
    
    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json",
        "X-AgentWall-Run-ID": f"test-loop-{datetime.now().strftime('%H%M%S')}"
    }
    
    # Aynı prompt'u 5 kez gönder
    prompt = "What is 2+2? Give me just the number."
    
    async with aiohttp.ClientSession() as session:
        for i in range(5):
            print(f"\n📋 Request {i+1}/5")
            
            payload = {
                "model": "gpt-3.5-turbo",
                "messages": [{"role": "user", "content": prompt}],
                "max_tokens": 10
            }
            
            try:
                async with session.post(
                    f"{PRODUCTION_URL}/v1/chat/completions",
                    json=payload,
                    headers=headers,
                    timeout=30
                ) as resp:
                    # Check for loop detection headers
                    loop_detected = resp.headers.get("X-AgentWall-Loop-Detected", "false")
                    step = resp.headers.get("X-AgentWall-Step", "N/A")
                    
                    print(f"   Status: {resp.status}")
                    print(f"   Step: {step}")
                    print(f"   Loop Detected: {loop_detected}")
                    
                    if resp.status == 200:
                        data = await resp.json()
                        if "agentwall" in data:
                            aw = data["agentwall"]
                            print(f"   AgentWall Step: {aw.get('step', 'N/A')}")
                            if aw.get("loop_detected"):
                                print(f"   ⚠️ LOOP DETECTED!")
                    elif resp.status == 429:
                        print(f"   ⚠️ Rate limited or loop killed!")
                        error = await resp.text()
                        print(f"   Message: {error[:200]}")
                        
            except Exception as e:
                print(f"   ❌ Exception: {e}")
            
            await asyncio.sleep(0.5)  # Small delay between requests
    
    print("\n" + "="*70)


async def test_budget_tracking():
    """Budget tracking testi"""
    print("\n" + "="*70)
    print("💰 AGENTWALL BUDGET TRACKING TEST")
    print("="*70)
    
    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json"
    }
    
    # Birkaç request gönder ve cost'u takip et
    total_cost = 0.0
    
    async with aiohttp.ClientSession() as session:
        for i in range(3):
            payload = {
                "model": "gpt-3.5-turbo",
                "messages": [{"role": "user", "content": f"Say 'test {i+1}'"}],
                "max_tokens": 10
            }
            
            try:
                async with session.post(
                    f"{PRODUCTION_URL}/v1/chat/completions",
                    json=payload,
                    headers=headers,
                    timeout=30
                ) as resp:
                    if resp.status == 200:
                        data = await resp.json()
                        
                        if "agentwall" in data:
                            cost = data["agentwall"].get("cost_usd", 0)
                            total_cost += cost
                            print(f"   Request {i+1}: ${cost:.6f}")
                        
                        if "usage" in data:
                            usage = data["usage"]
                            print(f"      Tokens: {usage.get('total_tokens', 0)}")
                            
            except Exception as e:
                print(f"   ❌ Exception: {e}")
    
    print(f"\n   Total Cost: ${total_cost:.6f}")
    print("="*70)


async def main():
    await test_dlp_masking()
    await test_loop_detection()
    await test_budget_tracking()


if __name__ == "__main__":
    asyncio.run(main())
