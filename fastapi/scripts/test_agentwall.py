#!/usr/bin/env python3
"""AgentWall Proxy Test - Real OpenAI API through AgentWall"""

import sys
import time
import argparse
sys.path.insert(0, "fastapi")

from fastapi.testclient import TestClient
from main import app

parser = argparse.ArgumentParser()
parser.add_argument("--api-key", required=True, help="OpenAI API key")
args = parser.parse_args()

API_KEY = args.api_key

client = TestClient(app)

print("=" * 60)
print("🛡️  AgentWall Proxy Test (Real OpenAI)")
print("=" * 60)

# Test 1: Health
print("\n1️⃣  Health Check...")
r = client.get("/health")
print(f"   Status: {r.status_code}")

# Test 2: Chat Completion through AgentWall
print("\n2️⃣  Chat Completion (AgentWall → OpenAI)...")
start = time.perf_counter()

r = client.post(
    "/v1/chat/completions",
    json={
        "model": "gpt-3.5-turbo",
        "messages": [{"role": "user", "content": "Say 'AgentWall works!' in 3 words"}],
        "max_tokens": 20,
    },
    headers={"Authorization": f"Bearer {API_KEY}"}
)

elapsed = (time.perf_counter() - start) * 1000

if r.status_code == 200:
    data = r.json()
    print(f"   ✅ SUCCESS!")
    print(f"   📝 Response: {data['choices'][0]['message']['content']}")
    print(f"   🔢 Tokens: {data['usage']['total_tokens']}")
    print(f"   ⏱️  Total Latency: {elapsed:.0f}ms")
    
    # AgentWall metadata
    if "agentwall" in data:
        aw = data["agentwall"]
        print(f"   🛡️  Run ID: {aw.get('run_id', 'N/A')}")
        print(f"   🛡️  Step: {aw.get('step', 'N/A')}")
        print(f"   🛡️  Overhead: {aw.get('overhead_ms', 'N/A')}ms")
        print(f"   🛡️  Cost: ${aw.get('cost_usd', 0):.6f}")
else:
    print(f"   ❌ FAILED! Status: {r.status_code}")
    print(f"   Error: {r.text[:500]}")

# Test 3: Streaming
print("\n3️⃣  Streaming Test...")
start = time.perf_counter()

with client.stream(
    "POST",
    "/v1/chat/completions",
    json={
        "model": "gpt-3.5-turbo",
        "messages": [{"role": "user", "content": "Count 1 to 3"}],
        "max_tokens": 30,
        "stream": True,
    },
    headers={"Authorization": f"Bearer {API_KEY}"}
) as response:
    if response.status_code == 200:
        print("   📡 Streaming: ", end="", flush=True)
        for line in response.iter_lines():
            if line and line.startswith("data: ") and "[DONE]" not in line:
                try:
                    import json
                    chunk = json.loads(line[6:])
                    content = chunk.get("choices", [{}])[0].get("delta", {}).get("content", "")
                    if content:
                        print(content, end="", flush=True)
                except:
                    pass
        print()
        elapsed = (time.perf_counter() - start) * 1000
        print(f"   ✅ Streaming SUCCESS! ({elapsed:.0f}ms)")
    else:
        print(f"   ❌ Streaming FAILED! Status: {response.status_code}")

print("\n" + "=" * 60)
print("🎉 AgentWall Proxy Test Complete!")
print("=" * 60)
