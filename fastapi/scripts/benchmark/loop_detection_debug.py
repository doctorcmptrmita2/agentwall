#!/usr/bin/env python3
"""
Loop Detection Debug Test
Error response structure'ını incelemek için
"""

import asyncio
import aiohttp
import json
import uuid

PRODUCTION_URL = "https://api.agentwall.io"
API_KEY = "aw-bJDiC5gtDnYJjIag9jQTzQyJr4RMotPX"


async def debug_loop_detection():
    """Debug loop detection error response"""
    print("\n" + "="*70)
    print("🔍 LOOP DETECTION ERROR RESPONSE DEBUG")
    print("="*70)
    
    run_id = f"debug-loop-{uuid.uuid4().hex[:8]}"
    headers = {"Authorization": f"Bearer {API_KEY}", "Content-Type": "application/json"}
    
    async with aiohttp.ClientSession() as session:
        # Request 1: OK
        print(f"\n📤 Request 1 (different prompt):")
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
            print(f"   Status: {resp.status}")
            data = await resp.json()
            print(f"   Response keys: {list(data.keys())}")
            if "agentwall" in data:
                print(f"   AgentWall: {data['agentwall']}")
        
        # Request 2: Same prompt - SHOULD BE BLOCKED
        print(f"\n📤 Request 2 (same prompt - should be blocked):")
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
            print(f"   Status: {resp.status}")
            data = await resp.json()
            print(f"   Response keys: {list(data.keys())}")
            print(f"\n   Full response:")
            print(json.dumps(data, indent=2))
            
            # Try different ways to access error
            print(f"\n   Error access attempts:")
            print(f"   1. data.get('error'): {data.get('error')}")
            print(f"   2. data.get('error', {{}}).get('type'): {data.get('error', {}).get('type')}")
            
            if "detail" in data:
                print(f"   3. data.get('detail'): {data.get('detail')}")
                if isinstance(data.get("detail"), dict):
                    print(f"      detail keys: {list(data['detail'].keys())}")
                    if "error" in data["detail"]:
                        print(f"      detail['error']: {data['detail']['error']}")
                        print(f"      detail['error'].get('type'): {data['detail']['error'].get('type')}")


if __name__ == "__main__":
    asyncio.run(debug_loop_detection())
