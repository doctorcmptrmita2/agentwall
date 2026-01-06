#!/usr/bin/env python3
"""
Loop Detection Test - Using Body run_id
Production'da body-based run_id ile loop detection test
"""

import asyncio
import aiohttp
import json
import uuid
from datetime import datetime

PRODUCTION_URL = "https://api.agentwall.io"
API_KEY = "aw-bJDiC5gtDnYJjIag9jQTzQyJr4RMotPX"


async def test_loop_with_body_run_id():
    """Test loop detection using run_id in request body"""
    print("\n" + "="*70)
    print("🔄 LOOP DETECTION TEST (Body run_id)")
    print("="*70)
    
    run_id = f"loop-test-{uuid.uuid4().hex[:8]}"
    print(f"\n📌 Run ID: {run_id}")
    
    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json",
    }
    
    prompt = "What is 2+2? Answer with just the number."
    
    async with aiohttp.ClientSession() as session:
        for i in range(10):
            payload = {
                "model": "gpt-3.5-turbo",
                "messages": [{"role": "user", "content": prompt}],
                "max_tokens": 10,
                "agentwall_run_id": run_id,
            }
            
            print(f"\n📤 Request {i+1}:")
            
            try:
                async with session.post(
                    f"{PRODUCTION_URL}/v1/chat/completions",
                    json=payload,
                    headers=headers,
                    timeout=60
                ) as resp:
                    if resp.status == 200:
                        data = await resp.json()
                        aw = data.get("agentwall", {})
                        
                        print(f"   ✅ Status: 200")
                        print(f"   Step: {aw.get('step', 'N/A')}")
                        print(f"   Total steps: {aw.get('total_run_steps', 'N/A')}")
                        print(f"   Cost: ${aw.get('cost_usd', 0):.6f}")
                        print(f"   Total cost: ${aw.get('total_run_cost', 0):.6f}")
                        
                        if "warning" in aw:
                            print(f"   ⚠️ WARNING: {aw['warning']}")
                            
                    elif resp.status == 429:
                        data = await resp.json()
                        error = data.get("detail", {}).get("error", {})
                        
                        print(f"   🛑 BLOCKED (429)")
                        print(f"   Type: {error.get('type', 'N/A')}")
                        print(f"   Message: {error.get('message', 'N/A')}")
                        
                        if error.get('type') == 'loop_detected':
                            print(f"\n   ✅ LOOP DETECTION WORKING!")
                            print(f"   Loop type: {error.get('loop_type', 'N/A')}")
                            print(f"   Confidence: {error.get('confidence', 'N/A')}")
                            break
                        elif error.get('type') == 'run_limit_exceeded':
                            print(f"\n   ✅ STEP LIMIT WORKING!")
                            break
                    else:
                        print(f"   ❌ Error {resp.status}: {await resp.text()}")
                        
            except Exception as e:
                print(f"   ❌ Exception: {e}")
            
            await asyncio.sleep(0.3)
    
    print("\n" + "="*70)


async def test_oscillation_with_body_run_id():
    """Test oscillation detection using run_id in request body"""
    print("\n" + "="*70)
    print("🔄 OSCILLATION DETECTION TEST (Body run_id)")
    print("="*70)
    
    run_id = f"osc-test-{uuid.uuid4().hex[:8]}"
    print(f"\n📌 Run ID: {run_id}")
    
    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json",
    }
    
    prompts = ["What is Python?", "What is JavaScript?"]
    
    async with aiohttp.ClientSession() as session:
        for i in range(10):
            prompt = prompts[i % 2]
            payload = {
                "model": "gpt-3.5-turbo",
                "messages": [{"role": "user", "content": prompt}],
                "max_tokens": 30,
                "agentwall_run_id": run_id,
            }
            
            print(f"\n📤 Request {i+1}: {prompt}")
            
            try:
                async with session.post(
                    f"{PRODUCTION_URL}/v1/chat/completions",
                    json=payload,
                    headers=headers,
                    timeout=60
                ) as resp:
                    if resp.status == 200:
                        data = await resp.json()
                        aw = data.get("agentwall", {})
                        print(f"   ✅ Step: {aw.get('step')}")
                        
                        if "warning" in aw:
                            print(f"   ⚠️ WARNING: {aw['warning']}")
                            
                    elif resp.status == 429:
                        data = await resp.json()
                        error = data.get("detail", {}).get("error", {})
                        
                        print(f"   🛑 BLOCKED: {error.get('type')}")
                        if error.get('type') == 'loop_detected':
                            print(f"   ✅ OSCILLATION DETECTED!")
                            print(f"   Loop type: {error.get('loop_type')}")
                            break
                    else:
                        print(f"   ❌ Error {resp.status}")
                        
            except Exception as e:
                print(f"   ❌ Exception: {e}")
            
            await asyncio.sleep(0.3)


async def test_normal_flow_with_body_run_id():
    """Test normal flow (different prompts) - should NOT trigger loop"""
    print("\n" + "="*70)
    print("✅ NORMAL FLOW TEST (Body run_id)")
    print("="*70)
    
    run_id = f"normal-{uuid.uuid4().hex[:8]}"
    print(f"\n📌 Run ID: {run_id}")
    
    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json",
    }
    
    prompts = [
        "What is the capital of France?",
        "What is 2 + 2?",
        "Name a programming language",
        "What color is the sky?",
        "Name a planet",
    ]
    
    async with aiohttp.ClientSession() as session:
        for i, prompt in enumerate(prompts):
            payload = {
                "model": "gpt-3.5-turbo",
                "messages": [{"role": "user", "content": prompt}],
                "max_tokens": 20,
                "agentwall_run_id": run_id,
            }
            
            print(f"\n📤 Request {i+1}: {prompt[:40]}...")
            
            try:
                async with session.post(
                    f"{PRODUCTION_URL}/v1/chat/completions",
                    json=payload,
                    headers=headers,
                    timeout=60
                ) as resp:
                    if resp.status == 200:
                        data = await resp.json()
                        aw = data.get("agentwall", {})
                        response = data.get("choices", [{}])[0].get("message", {}).get("content", "")
                        print(f"   ✅ Step {aw.get('step')}: {response[:30]}...")
                    elif resp.status == 429:
                        print(f"   ❌ UNEXPECTED BLOCK!")
                        break
                    else:
                        print(f"   ❌ Error {resp.status}")
                        
            except Exception as e:
                print(f"   ❌ Exception: {e}")
            
            await asyncio.sleep(0.3)
    
    print("\n   ✅ Normal flow completed without false positives!")


async def main():
    print("\n" + "="*70)
    print("🛡️ AGENTWALL LOOP DETECTION - BODY RUN_ID TESTS")
    print("="*70)
    print(f"Target: {PRODUCTION_URL}")
    print(f"Time: {datetime.now().isoformat()}")
    
    # Test 1: Normal flow (should pass)
    await test_normal_flow_with_body_run_id()
    
    # Test 2: Loop detection (same prompt)
    await test_loop_with_body_run_id()
    
    # Test 3: Oscillation detection
    await test_oscillation_with_body_run_id()
    
    print("\n" + "="*70)
    print("✅ ALL TESTS COMPLETE")
    print("="*70)


if __name__ == "__main__":
    asyncio.run(main())
