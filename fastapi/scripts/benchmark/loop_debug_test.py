#!/usr/bin/env python3
"""
Loop Detection Debug Test
Redis'te run state'in persist edilip edilmediğini test eder.
"""

import asyncio
import aiohttp
import json
import uuid
from datetime import datetime

PRODUCTION_URL = "https://api.agentwall.io"
API_KEY = "aw-bJDiC5gtDnYJjIag9jQTzQyJr4RMotPX"


async def test_run_persistence():
    """Test if run_id persists across requests"""
    print("\n" + "="*70)
    print("🔍 LOOP DETECTION DEBUG TEST")
    print("="*70)
    
    run_id = f"debug-{uuid.uuid4().hex[:8]}"
    print(f"\n📌 Using fixed run_id: {run_id}")
    
    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json",
        "X-AgentWall-Run-ID": run_id,
    }
    
    # Same prompt for all requests
    prompt = "What is 2+2?"
    payload = {
        "model": "gpt-3.5-turbo",
        "messages": [{"role": "user", "content": prompt}],
        "max_tokens": 10
    }
    
    async with aiohttp.ClientSession() as session:
        for i in range(5):
            print(f"\n📤 Request {i+1}:")
            print(f"   Header X-AgentWall-Run-ID: {run_id}")
            
            async with session.post(
                f"{PRODUCTION_URL}/v1/chat/completions",
                json=payload,
                headers=headers,
                timeout=60
            ) as resp:
                if resp.status == 200:
                    data = await resp.json()
                    aw = data.get("agentwall", {})
                    
                    print(f"   Response run_id: {aw.get('run_id', 'N/A')}")
                    print(f"   Step: {aw.get('step', 'N/A')}")
                    print(f"   Total run steps: {aw.get('total_run_steps', 'N/A')}")
                    print(f"   Loop detected: {aw.get('loop_detected', 'N/A')}")
                    print(f"   Cost: ${aw.get('cost_usd', 0):.6f}")
                    print(f"   Total run cost: ${aw.get('total_run_cost', 0):.6f}")
                    
                    # Check if run_id matches
                    if aw.get('run_id') != run_id:
                        print(f"   ⚠️ RUN_ID MISMATCH! Expected: {run_id}")
                    
                    # Check if step is incrementing
                    expected_step = i + 1
                    if aw.get('step') != expected_step:
                        print(f"   ⚠️ STEP MISMATCH! Expected: {expected_step}, Got: {aw.get('step')}")
                    
                    # Check for warning
                    if "warning" in aw:
                        print(f"   ⚠️ Warning: {aw['warning']}")
                        
                elif resp.status == 429:
                    data = await resp.json()
                    print(f"   🛑 BLOCKED: {data.get('detail', {}).get('error', {}).get('message', 'Unknown')}")
                    break
                else:
                    print(f"   ❌ Error {resp.status}: {await resp.text()}")
            
            await asyncio.sleep(0.5)  # Wait for async tasks to complete
    
    print("\n" + "="*70)
    print("📊 ANALYSIS:")
    print("="*70)
    print("""
If run_id matches and steps increment correctly:
  → Redis is working, run state is persisting
  → Loop detection logic may have a bug

If run_id doesn't match or steps don't increment:
  → Header is not being read
  → Or Redis state is not persisting

If loop is never detected after 5 same prompts:
  → Loop detection threshold may be too high
  → Or recent_prompts list is not being populated
""")


async def test_body_run_id():
    """Test if run_id in body works"""
    print("\n" + "="*70)
    print("🔍 TEST: RUN_ID IN REQUEST BODY")
    print("="*70)
    
    run_id = f"body-{uuid.uuid4().hex[:8]}"
    print(f"\n📌 Using run_id in body: {run_id}")
    
    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json",
    }
    
    prompt = "What is 2+2?"
    
    async with aiohttp.ClientSession() as session:
        for i in range(3):
            payload = {
                "model": "gpt-3.5-turbo",
                "messages": [{"role": "user", "content": prompt}],
                "max_tokens": 10,
                "agentwall_run_id": run_id,  # In body instead of header
            }
            
            print(f"\n📤 Request {i+1}:")
            
            async with session.post(
                f"{PRODUCTION_URL}/v1/chat/completions",
                json=payload,
                headers=headers,
                timeout=60
            ) as resp:
                if resp.status == 200:
                    data = await resp.json()
                    aw = data.get("agentwall", {})
                    
                    print(f"   Response run_id: {aw.get('run_id', 'N/A')}")
                    print(f"   Step: {aw.get('step', 'N/A')}")
                    print(f"   Match: {'✅' if aw.get('run_id') == run_id else '❌'}")
                else:
                    print(f"   ❌ Error {resp.status}")
            
            await asyncio.sleep(0.5)


async def main():
    print("\n" + "="*70)
    print("🛡️ AGENTWALL LOOP DETECTION DEBUG")
    print("="*70)
    print(f"Target: {PRODUCTION_URL}")
    print(f"Time: {datetime.now().isoformat()}")
    
    # Test 1: Header-based run_id
    await test_run_persistence()
    
    # Test 2: Body-based run_id
    await test_body_run_id()
    
    print("\n✅ Debug tests complete")


if __name__ == "__main__":
    asyncio.run(main())
