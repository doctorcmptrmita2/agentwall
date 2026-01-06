#!/usr/bin/env python3
"""Quick OpenAI API Test"""

from openai import OpenAI
import time
import os
import argparse

parser = argparse.ArgumentParser()
parser.add_argument("--api-key", required=True, help="OpenAI API key")
args = parser.parse_args()

API_KEY = args.api_key

print("=" * 50)
print("🧪 OpenAI API Direct Test")
print("=" * 50)

client = OpenAI(api_key=API_KEY)

start = time.perf_counter()

try:
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": "Say hello in 3 words"}],
        max_tokens=20,
    )
    
    elapsed = (time.perf_counter() - start) * 1000
    
    print(f"✅ SUCCESS!")
    print(f"📝 Response: {response.choices[0].message.content}")
    print(f"🔢 Tokens: {response.usage.total_tokens}")
    print(f"⏱️  Latency: {elapsed:.0f}ms")
    
except Exception as e:
    elapsed = (time.perf_counter() - start) * 1000
    print(f"❌ FAILED!")
    print(f"🚨 Error: {e}")
    print(f"⏱️  Latency: {elapsed:.0f}ms")
