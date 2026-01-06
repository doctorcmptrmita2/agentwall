#!/usr/bin/env python3
"""
OpenRouter Multi-Provider Test
Tests Claude, Gemini, Llama via OpenRouter
"""

import asyncio
import httpx
import time
import json
from datetime import datetime

# OpenRouter models to test
MODELS = [
    ("anthropic/claude-3-haiku", "Claude 3 Haiku"),
    ("google/gemini-flash-1.5", "Gemini Flash"),
    ("meta-llama/llama-3.1-8b-instruct", "Llama 3.1 8B"),
    ("mistralai/mistral-7b-instruct", "Mistral 7B"),
    ("qwen/qwen-2-7b-instruct", "Qwen 2 7B"),
]

async def test_model(api_key: str, model: str, name: str, base_url: str):
    """Test a single model"""
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",
        "HTTP-Referer": "https://agentwall.io",
        "X-Title": "AgentWall Test",
    }
    
    payload = {
        "model": model,
        "messages": [{"role": "user", "content": "Say 'OK' only."}],
        "max_tokens": 10,
    }
    
    start = time.perf_counter()
    
    async with httpx.AsyncClient(timeout=60.0) as client:
        try:
            response = await client.post(
                f"{base_url}/v1/chat/completions",
                headers=headers,
                json=payload,
            )
            duration = (time.perf_counter() - start) * 1000
            
            if response.status_code == 200:
                data = response.json()
                content = data["choices"][0]["message"]["content"]
                usage = data.get("usage", {})
                return {
                    "model": model,
                    "name": name,
                    "status": "✅ PASS",
                    "response": content[:50],
                    "tokens": usage.get("total_tokens", 0),
                    "duration_ms": duration,
                }
            else:
                return {
                    "model": model,
                    "name": name,
                    "status": "❌ FAIL",
                    "error": response.text[:100],
                    "duration_ms": duration,
                }
        except Exception as e:
            return {
                "model": model,
                "name": name,
                "status": "❌ ERROR",
                "error": str(e)[:100],
                "duration_ms": 0,
            }

async def main():
    import sys
    
    if len(sys.argv) < 2:
        print("Usage: python test_openrouter.py <OPENROUTER_API_KEY>")
        sys.exit(1)
    
    api_key = sys.argv[1]
    base_url = "https://openrouter.ai/api"
    
    print("\n" + "="*60)
    print("🌐 OpenRouter Multi-Provider Test")
    print("="*60)
    print(f"📍 Target: {base_url}")
    print(f"🤖 Models: {len(MODELS)}")
    print("="*60 + "\n")
    
    results = []
    
    for model, name in MODELS:
        print(f"Testing: {name} ({model})...")
        result = await test_model(api_key, model, name, base_url)
        results.append(result)
        print(f"  {result['status']} - {result.get('duration_ms', 0):.0f}ms")
    
    # Summary
    print("\n" + "="*60)
    print("📊 RESULTS")
    print("="*60)
    
    passed = sum(1 for r in results if "PASS" in r["status"])
    
    print(f"\n✅ Passed: {passed}/{len(results)}")
    print(f"❌ Failed: {len(results) - passed}/{len(results)}")
    
    print("\n| Model | Status | Duration | Response |")
    print("|-------|--------|----------|----------|")
    for r in results:
        resp = r.get("response", r.get("error", ""))[:30]
        print(f"| {r['name']} | {r['status']} | {r.get('duration_ms', 0):.0f}ms | {resp} |")
    
    # Save report
    report = f"""# OpenRouter Multi-Provider Test Report

**Date:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
**Target:** {base_url}

## Results

| Model | Provider | Status | Duration |
|-------|----------|--------|----------|
"""
    for r in results:
        report += f"| {r['name']} | {r['model'].split('/')[0]} | {r['status']} | {r.get('duration_ms', 0):.0f}ms |\n"
    
    report += f"""
## Summary

- **Total Models:** {len(results)}
- **Passed:** {passed}
- **Failed:** {len(results) - passed}

*"Guard the Agent, Save the Budget"* 🛡️
"""
    
    with open("docs/OpenRouterTestReport.md", "w", encoding="utf-8") as f:
        f.write(report)
    
    print(f"\n📄 Report saved to: docs/OpenRouterTestReport.md")

if __name__ == "__main__":
    asyncio.run(main())
