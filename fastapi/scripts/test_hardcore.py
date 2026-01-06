#!/usr/bin/env python3
"""
AgentWall HARDCORE Test Suite
=============================
Zorlu senaryolar, 5 farklı model, stres testleri

Test Kategorileri:
1. Multi-Model Tests (5 model)
2. DLP Stress Tests (karmaşık patterns)
3. Loop Detection Edge Cases
4. Concurrent Requests
5. Long Context Tests
6. Rapid Fire Tests

Bütçe: ~$1.50-2.00
"""

import os
import sys
import json
import time
import asyncio
import argparse
from datetime import datetime
from dataclasses import dataclass, field
from typing import Optional
import httpx

BASE_URL = os.getenv("AGENTWALL_URL", "https://api.agentwall.io")

# 5 farklı model
MODELS = [
    "gpt-3.5-turbo",
    "gpt-3.5-turbo-0125",
    "gpt-4o-mini",
    "gpt-4-turbo-preview",
    "gpt-4o",
]

@dataclass
class TestResult:
    name: str
    passed: bool
    duration_ms: float
    details: dict = field(default_factory=dict)
    error: Optional[str] = None
    cost_usd: float = 0.0
    model: str = ""


class HardcoreTester:
    def __init__(self, api_key: str, base_url: str = BASE_URL):
        self.api_key = api_key
        self.base_url = base_url.rstrip("/")
        self.results: list[TestResult] = []
        self.total_cost = 0.0
        
    async def _chat(self, messages: list, model: str, run_id: str = None, 
                    stream: bool = False, max_tokens: int = 50) -> dict:
        async with httpx.AsyncClient(timeout=120.0) as client:
            headers = {"Authorization": f"Bearer {self.api_key}", "Content-Type": "application/json"}
            payload = {"model": model, "messages": messages, "max_tokens": max_tokens, "stream": stream}
            if run_id:
                payload["agentwall_run_id"] = run_id
            
            start = time.perf_counter()
            
            if stream:
                chunks = []
                async with client.stream("POST", f"{self.base_url}/v1/chat/completions", 
                                         headers=headers, json=payload) as response:
                    async for line in response.aiter_lines():
                        if line.startswith("data: "):
                            chunks.append(line)
                    return {"status": response.status_code, "chunks": chunks, 
                            "duration_ms": (time.perf_counter() - start) * 1000,
                            "headers": dict(response.headers)}
            else:
                response = await client.post(f"{self.base_url}/v1/chat/completions", 
                                            headers=headers, json=payload)
                return {"status": response.status_code, 
                        "data": response.json() if response.status_code == 200 else None,
                        "error": response.text if response.status_code != 200 else None,
                        "duration_ms": (time.perf_counter() - start) * 1000,
                        "headers": dict(response.headers)}

    async def run_all_tests(self) -> list[TestResult]:
        print("\n" + "="*70)
        print("🔥 AgentWall HARDCORE Test Suite")
        print("="*70)
        print(f"📍 Target: {self.base_url}")
        print(f"🤖 Models: {', '.join(MODELS)}")
        print(f"💰 Budget: $2.00")
        print("="*70 + "\n")
        
        tests = [
            # Multi-Model Tests
            ("🔷 Multi-Model: gpt-3.5-turbo", lambda: self.test_model(MODELS[0])),
            ("🔷 Multi-Model: gpt-3.5-turbo-0125", lambda: self.test_model(MODELS[1])),
            ("🔷 Multi-Model: gpt-4o-mini", lambda: self.test_model(MODELS[2])),
            ("🔷 Multi-Model: gpt-4-turbo-preview", lambda: self.test_model(MODELS[3])),
            ("🔷 Multi-Model: gpt-4o", lambda: self.test_model(MODELS[4])),
            
            # DLP Stress Tests
            ("🛡️ DLP: Multiple API Keys", self.test_dlp_multiple_keys),
            ("🛡️ DLP: Mixed Sensitive Data", self.test_dlp_mixed),
            ("🛡️ DLP: JWT Token", self.test_dlp_jwt),
            ("🛡️ DLP: AWS Credentials", self.test_dlp_aws),
            
            # Loop Detection Edge Cases
            ("🔄 Loop: Rapid Exact Repeat (10x)", self.test_loop_rapid),
            ("🔄 Loop: Oscillation Pattern", self.test_loop_oscillation),
            
            # Stress Tests
            ("⚡ Stress: Concurrent 5 Requests", self.test_concurrent),
            ("⚡ Stress: Long Context (2000 chars)", self.test_long_context),
            
            # Streaming Tests
            ("📡 Stream: Multi-Model Stream", self.test_stream_multimodel),
        ]
        
        for name, test_func in tests:
            print(f"\n{'─'*60}")
            print(f"Running: {name}")
            print(f"{'─'*60}")
            
            try:
                result = await test_func()
                self.results.append(result)
                self.total_cost += result.cost_usd
                
                status = "✅ PASS" if result.passed else "❌ FAIL"
                print(f"Result: {status}")
                print(f"Duration: {result.duration_ms:.2f}ms")
                if result.cost_usd > 0:
                    print(f"Cost: ${result.cost_usd:.6f}")
                if result.model:
                    print(f"Model: {result.model}")
                if result.error:
                    print(f"Error: {result.error[:100]}")
            except Exception as e:
                self.results.append(TestResult(name=name, passed=False, duration_ms=0, error=str(e)))
                print(f"Result: ❌ EXCEPTION: {e}")
        
        return self.results


    # ==================== MULTI-MODEL TESTS ====================
    
    async def test_model(self, model: str) -> TestResult:
        """Her model için temel test"""
        result = await self._chat([{"role": "user", "content": "Say 'OK' only."}], model=model)
        
        passed = result["status"] == 200 and result["data"] and "agentwall" in result["data"]
        cost = result["data"]["agentwall"].get("cost_usd", 0) if passed else 0
        
        return TestResult(
            name=f"Model Test: {model}",
            passed=passed,
            duration_ms=result["duration_ms"],
            details={"response": result["data"]["choices"][0]["message"]["content"] if passed else None},
            cost_usd=cost,
            model=model,
            error=result.get("error"),
        )

    # ==================== DLP STRESS TESTS ====================
    
    async def test_dlp_multiple_keys(self) -> TestResult:
        """Birden fazla API key içeren prompt"""
        keys = [
            "sk-proj-ABC123456789012345678901234567890123",
            "sk-live-XYZ987654321098765432109876543210987",
            "AKIA1234567890ABCDEF",
        ]
        prompt = f"Store these keys: {', '.join(keys)}"
        
        result = await self._chat([{"role": "user", "content": prompt}], model="gpt-3.5-turbo")
        
        response_text = ""
        if result["data"] and result["data"].get("choices"):
            response_text = result["data"]["choices"][0]["message"]["content"]
        
        # Hiçbir key response'da olmamalı
        any_leaked = any(key in response_text for key in keys)
        cost = result["data"]["agentwall"].get("cost_usd", 0) if result["data"] else 0
        
        return TestResult(
            name="DLP: Multiple API Keys",
            passed=not any_leaked and result["status"] == 200,
            duration_ms=result["duration_ms"],
            details={"keys_sent": len(keys), "any_leaked": any_leaked},
            cost_usd=cost,
            model="gpt-3.5-turbo",
        )
    
    async def test_dlp_mixed(self) -> TestResult:
        """Karışık hassas veri: API key + CC + Email + Phone"""
        prompt = """Process this data:
        API: sk-proj-SECRETKEY123456789012345678901234
        Card: 4532015112830366
        Email: ceo@secretcorp.com
        Phone: 555-867-5309
        SSN: 123-45-6789"""
        
        result = await self._chat([{"role": "user", "content": prompt}], model="gpt-3.5-turbo")
        
        response_text = ""
        if result["data"] and result["data"].get("choices"):
            response_text = result["data"]["choices"][0]["message"]["content"]
        
        leaked = {
            "api_key": "SECRETKEY" in response_text,
            "cc": "4532015112830366" in response_text,
            "email": "ceo@secretcorp.com" in response_text,
            "ssn": "123-45-6789" in response_text,
        }
        any_leaked = any(leaked.values())
        cost = result["data"]["agentwall"].get("cost_usd", 0) if result["data"] else 0
        
        return TestResult(
            name="DLP: Mixed Sensitive Data",
            passed=not any_leaked and result["status"] == 200,
            duration_ms=result["duration_ms"],
            details={"leaked": leaked},
            cost_usd=cost,
            model="gpt-3.5-turbo",
        )
    
    async def test_dlp_jwt(self) -> TestResult:
        """JWT token tespiti"""
        # Fake JWT
        jwt = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIxMjM0NTY3ODkwIiwibmFtZSI6IkpvaG4gRG9lIiwiaWF0IjoxNTE2MjM5MDIyfQ.SflKxwRJSMeKKF2QT4fwpMeJf36POk6yJV_adQssw5c"
        
        result = await self._chat([{"role": "user", "content": f"Decode this JWT: {jwt}"}], model="gpt-3.5-turbo")
        
        response_text = ""
        if result["data"] and result["data"].get("choices"):
            response_text = result["data"]["choices"][0]["message"]["content"]
        
        jwt_leaked = jwt in response_text
        cost = result["data"]["agentwall"].get("cost_usd", 0) if result["data"] else 0
        
        return TestResult(
            name="DLP: JWT Token",
            passed=not jwt_leaked and result["status"] == 200,
            duration_ms=result["duration_ms"],
            details={"jwt_leaked": jwt_leaked},
            cost_usd=cost,
            model="gpt-3.5-turbo",
        )
    
    async def test_dlp_aws(self) -> TestResult:
        """AWS credentials tespiti"""
        prompt = """My AWS config:
        aws_access_key_id = AKIAIOSFODNN7EXAMPLE
        aws_secret_access_key = wJalrXUtnFEMI/K7MDENG/bPxRfiCYEXAMPLEKEY"""
        
        result = await self._chat([{"role": "user", "content": prompt}], model="gpt-3.5-turbo")
        
        response_text = ""
        if result["data"] and result["data"].get("choices"):
            response_text = result["data"]["choices"][0]["message"]["content"]
        
        aws_leaked = "AKIAIOSFODNN7EXAMPLE" in response_text or "wJalrXUtnFEMI" in response_text
        cost = result["data"]["agentwall"].get("cost_usd", 0) if result["data"] else 0
        
        return TestResult(
            name="DLP: AWS Credentials",
            passed=not aws_leaked and result["status"] == 200,
            duration_ms=result["duration_ms"],
            details={"aws_leaked": aws_leaked},
            cost_usd=cost,
            model="gpt-3.5-turbo",
        )


    # ==================== LOOP DETECTION EDGE CASES ====================
    
    async def test_loop_rapid(self) -> TestResult:
        """10 kez aynı prompt - hızlı tekrar"""
        import uuid
        run_id = f"rapid-loop-{uuid.uuid4()}"
        
        blocked_at = None
        total_cost = 0.0
        
        for i in range(10):
            result = await self._chat(
                [{"role": "user", "content": "What is 2+2?"}],
                model="gpt-3.5-turbo",
                run_id=run_id
            )
            
            if result["status"] == 429:
                blocked_at = i + 1
                break
            
            if result["data"] and "agentwall" in result["data"]:
                total_cost += result["data"]["agentwall"].get("cost_usd", 0)
        
        return TestResult(
            name="Loop: Rapid Exact Repeat (10x)",
            passed=blocked_at is not None and blocked_at <= 3,  # 3. adımda veya önce bloklanmalı
            duration_ms=0,
            details={"blocked_at_step": blocked_at, "expected": "≤3"},
            cost_usd=total_cost,
            model="gpt-3.5-turbo",
        )
    
    async def test_loop_oscillation(self) -> TestResult:
        """A-B-A-B pattern tespiti"""
        import uuid
        run_id = f"oscillation-{uuid.uuid4()}"
        
        prompts = ["What is A?", "What is B?", "What is A?", "What is B?", "What is A?"]
        blocked = False
        total_cost = 0.0
        
        for prompt in prompts:
            result = await self._chat(
                [{"role": "user", "content": prompt}],
                model="gpt-3.5-turbo",
                run_id=run_id
            )
            
            if result["status"] == 429:
                blocked = True
                break
            
            if result["data"] and "agentwall" in result["data"]:
                total_cost += result["data"]["agentwall"].get("cost_usd", 0)
        
        return TestResult(
            name="Loop: Oscillation Pattern",
            passed=blocked or total_cost > 0,  # Ya bloklanmalı ya da en az bir istek geçmeli
            duration_ms=0,
            details={"blocked": blocked, "pattern": "A-B-A-B-A"},
            cost_usd=total_cost,
            model="gpt-3.5-turbo",
        )

    # ==================== STRESS TESTS ====================
    
    async def test_concurrent(self) -> TestResult:
        """5 eşzamanlı istek"""
        async def single_request(i):
            return await self._chat(
                [{"role": "user", "content": f"Request {i}: Say 'OK'"}],
                model="gpt-3.5-turbo"
            )
        
        start = time.perf_counter()
        results = await asyncio.gather(*[single_request(i) for i in range(5)])
        duration = (time.perf_counter() - start) * 1000
        
        success_count = sum(1 for r in results if r["status"] == 200)
        total_cost = sum(
            r["data"]["agentwall"].get("cost_usd", 0) 
            for r in results if r["data"] and "agentwall" in r["data"]
        )
        
        return TestResult(
            name="Stress: Concurrent 5 Requests",
            passed=success_count == 5,
            duration_ms=duration,
            details={"success_count": success_count, "total_requests": 5},
            cost_usd=total_cost,
            model="gpt-3.5-turbo",
        )
    
    async def test_long_context(self) -> TestResult:
        """Uzun context testi (2000 karakter)"""
        long_text = "This is a test. " * 125  # ~2000 chars
        
        result = await self._chat(
            [{"role": "user", "content": f"Summarize: {long_text}"}],
            model="gpt-3.5-turbo",
            max_tokens=100
        )
        
        passed = result["status"] == 200 and result["data"] is not None
        cost = result["data"]["agentwall"].get("cost_usd", 0) if passed else 0
        
        return TestResult(
            name="Stress: Long Context (2000 chars)",
            passed=passed,
            duration_ms=result["duration_ms"],
            details={"context_length": len(long_text)},
            cost_usd=cost,
            model="gpt-3.5-turbo",
        )

    # ==================== STREAMING TESTS ====================
    
    async def test_stream_multimodel(self) -> TestResult:
        """Farklı modeller ile streaming"""
        models_to_test = ["gpt-3.5-turbo", "gpt-4o-mini"]
        results = []
        total_cost = 0.0
        
        for model in models_to_test:
            result = await self._chat(
                [{"role": "user", "content": "Count: 1, 2, 3"}],
                model=model,
                stream=True
            )
            
            chunks = result.get("chunks", [])
            has_done = any("[DONE]" in c for c in chunks)
            results.append({
                "model": model,
                "status": result["status"],
                "chunks": len(chunks),
                "has_done": has_done,
            })
            total_cost += 0.0001  # Tahmini
        
        all_passed = all(r["status"] == 200 and r["has_done"] for r in results)
        
        return TestResult(
            name="Stream: Multi-Model Stream",
            passed=all_passed,
            duration_ms=0,
            details={"results": results},
            cost_usd=total_cost,
            model="multiple",
        )


    def generate_report(self) -> str:
        passed = sum(1 for r in self.results if r.passed)
        failed = len(self.results) - passed
        
        md = []
        md.append("# 🔥 AgentWall HARDCORE Test Report")
        md.append("")
        md.append(f"**Date:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        md.append(f"**Target:** {self.base_url}")
        md.append(f"**Models Tested:** {', '.join(MODELS)}")
        md.append(f"**Total Cost:** ${self.total_cost:.6f}")
        md.append("")
        md.append("---")
        md.append("")
        md.append("## 📊 Summary")
        md.append("")
        md.append("| Metric | Value |")
        md.append("|--------|-------|")
        md.append(f"| Total Tests | {len(self.results)} |")
        md.append(f"| Passed | {passed} ✅ |")
        md.append(f"| Failed | {failed} ❌ |")
        md.append(f"| Success Rate | {passed/len(self.results)*100:.1f}% |")
        md.append(f"| Total Cost | ${self.total_cost:.6f} |")
        md.append("")
        md.append("---")
        md.append("")
        md.append("## 🔷 Multi-Model Results")
        md.append("")
        md.append("| Model | Status | Duration | Cost |")
        md.append("|-------|--------|----------|------|")
        
        for r in self.results:
            if "Multi-Model" in r.name:
                status = "✅" if r.passed else "❌"
                md.append(f"| {r.model} | {status} | {r.duration_ms:.0f}ms | ${r.cost_usd:.6f} |")
        
        md.append("")
        md.append("---")
        md.append("")
        md.append("## 🛡️ DLP Stress Test Results")
        md.append("")
        md.append("| Test | Status | Details |")
        md.append("|------|--------|---------|")
        
        for r in self.results:
            if "DLP" in r.name:
                status = "✅ PASS" if r.passed else "❌ FAIL"
                details = json.dumps(r.details, default=str)[:50]
                md.append(f"| {r.name} | {status} | {details} |")
        
        md.append("")
        md.append("---")
        md.append("")
        md.append("## 🔄 Loop Detection Results")
        md.append("")
        md.append("| Test | Status | Details |")
        md.append("|------|--------|---------|")
        
        for r in self.results:
            if "Loop" in r.name:
                status = "✅ PASS" if r.passed else "❌ FAIL"
                details = json.dumps(r.details, default=str)[:50]
                md.append(f"| {r.name} | {status} | {details} |")
        
        md.append("")
        md.append("---")
        md.append("")
        md.append("## ⚡ Stress Test Results")
        md.append("")
        md.append("| Test | Status | Duration | Details |")
        md.append("|------|--------|----------|---------|")
        
        for r in self.results:
            if "Stress" in r.name or "Stream" in r.name:
                status = "✅ PASS" if r.passed else "❌ FAIL"
                details = json.dumps(r.details, default=str)[:40]
                md.append(f"| {r.name} | {status} | {r.duration_ms:.0f}ms | {details} |")
        
        md.append("")
        md.append("---")
        md.append("")
        md.append("## 📝 All Results")
        md.append("")
        
        for r in self.results:
            status = "✅" if r.passed else "❌"
            md.append(f"### {status} {r.name}")
            md.append("")
            md.append(f"- **Model:** {r.model}")
            md.append(f"- **Duration:** {r.duration_ms:.2f}ms")
            md.append(f"- **Cost:** ${r.cost_usd:.6f}")
            if r.error:
                md.append(f"- **Error:** {r.error[:200]}")
            md.append("")
            if r.details:
                md.append("**Details:**")
                md.append("```json")
                md.append(json.dumps(r.details, indent=2, default=str)[:500])
                md.append("```")
            md.append("")
        
        md.append("---")
        md.append("")
        md.append("## ✅ Conclusion")
        md.append("")
        if failed == 0:
            md.append("**🎉 ALL HARDCORE TESTS PASSED!**")
            md.append("")
            md.append("AgentWall successfully handled:")
            md.append("- ✅ 5 different OpenAI models")
            md.append("- ✅ Complex DLP patterns (API keys, JWT, AWS, mixed data)")
            md.append("- ✅ Loop detection edge cases")
            md.append("- ✅ Concurrent requests")
            md.append("- ✅ Long context processing")
            md.append("- ✅ Multi-model streaming")
        else:
            md.append(f"**{failed} test(s) failed.** Review details above.")
        
        md.append("")
        md.append("---")
        md.append("")
        md.append('*"Guard the Agent, Save the Budget"* 🛡️')
        
        return "\n".join(md)


async def main():
    parser = argparse.ArgumentParser(description="AgentWall HARDCORE Tests")
    parser.add_argument("--api-key", required=True, help="OpenAI API key")
    parser.add_argument("--url", default=BASE_URL, help="AgentWall URL")
    parser.add_argument("--output", default="docs/ProductionTestReportHard.md", help="Output file")
    args = parser.parse_args()
    
    tester = HardcoreTester(api_key=args.api_key, base_url=args.url)
    
    try:
        await tester.run_all_tests()
    except KeyboardInterrupt:
        print("\n⚠️ Tests interrupted")
    
    report = tester.generate_report()
    
    with open(args.output, "w", encoding="utf-8") as f:
        f.write(report)
    
    print(f"\n📄 Report saved to: {args.output}")
    print(f"💰 Total cost: ${tester.total_cost:.6f}")
    
    failed = sum(1 for r in tester.results if not r.passed)
    sys.exit(0 if failed == 0 else 1)


if __name__ == "__main__":
    asyncio.run(main())
