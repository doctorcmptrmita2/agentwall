#!/usr/bin/env python3
"""Test all Claude models via OpenRouter"""

import asyncio
import httpx
import time

CLAUDE_MODELS = [
    ("anthropic/claude-sonnet-4", "Claude Sonnet 4"),
    ("anthropic/claude-3.5-sonnet", "Claude 3.5 Sonnet"),
    ("anthropic/claude-3.5-sonnet-20241022", "Claude 3.5 Sonnet (Oct)"),
    ("anthropic/claude-3-opus", "Claude 3 Opus"),
    ("anthropic/claude-3-sonnet", "Claude 3 Sonnet"),
    ("anthropic/claude-3-haiku", "Claude 3 Haiku"),
    ("anthropic/claude-3.5-haiku", "Claude 3.5 Haiku"),
]

async def test_model(api_key: str, model: str, name: str):
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",
        "HTTP-Referer": "https://agentwall.io",
    }
    payload = {"model": model, "messages": [{"role": "user", "content": "Say OK"}], "max_tokens": 5}
    
    start = time.perf_counter()
    async with httpx.AsyncClient(timeout=60.0) as client:
        try:
            r = await client.post("https://openrouter.ai/api/v1/chat/completions", headers=headers, json=payload)
            ms = (time.perf_counter() - start) * 1000
            if r.status_code == 200:
                return f"✅ {name}: {ms:.0f}ms - {r.json()['choices'][0]['message']['content'][:20]}"
            else:
                err = r.json().get("error", {}).get("message", r.text[:50])
                return f"❌ {name}: {err[:40]}"
        except Exception as e:
            return f"❌ {name}: {str(e)[:40]}"

async def main():
    import sys
    api_key = sys.argv[1] if len(sys.argv) > 1 else ""
    
    print("\n🤖 Claude Models Test (OpenRouter)\n" + "="*50)
    
    for model, name in CLAUDE_MODELS:
        result = await test_model(api_key, model, name)
        print(result)
    
    print("="*50)

if __name__ == "__main__":
    asyncio.run(main())
