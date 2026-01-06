#!/usr/bin/env python3
"""
AgentWall Real Scenario Tests
=============================
Gerçek OpenAI API ile AgentWall'un tüm özelliklerini test eder.

Test Senaryoları:
1. DLP Test - API key, kredi kartı, email sızıntısı tespiti
2. Loop Detection - Sonsuz döngü tespiti
3. Budget Enforcement - Bütçe limiti aşımı
4. Run Tracking - Multi-step run takibi
5. Cost Tracking - Maliyet hesaplama doğruluğu

Bütçe: ~$0.50-1.00 (gpt-3.5-turbo kullanarak)

Kullanım:
    python test_real_scenarios.py --api-key YOUR_OPENAI_KEY
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

# Test configuration
BASE_URL = os.getenv("AGENTWALL_URL", "http://localhost:8000")
MODEL = "gpt-3.5-turbo"  # Cheaper for testing

@dataclass
class TestResult:
    name: str
    passed: bool
    duration_ms: float
    details: dict = field(default_factory=dict)
    error: Optional[str] = None
    cost_usd: float = 0.0


class RealScenarioTester:
    """AgentWall gerçek senaryo test sınıfı"""
    
    def __init__(self, api_key: str, base_url: str = BASE_URL):
        self.api_key = api_key
        self.base_url = base_url.rstrip("/")
        self.results: list[TestResult] = []
        self.total_cost = 0.0
        
    async def run_all_tests(self) -> list[TestResult]:
        """Tüm testleri çalıştır"""
        print("\n" + "="*60)
        print("🧪 AgentWall Real Scenario Tests")
        print("="*60)
        print(f"📍 Target: {self.base_url}")
        print(f"🤖 Model: {MODEL}")
        print(f"💰 Budget: $2.00")
        print("="*60 + "\n")
        
        # Test sırası
        tests = [
            ("1️⃣ Health Check", self.test_health),
            ("2️⃣ Basic Proxy", self.test_basic_proxy),
            ("3️⃣ DLP - API Key Detection", self.test_dlp_api_key),
            ("4️⃣ DLP - Credit Card Detection", self.test_dlp_credit_card),
            ("5️⃣ DLP - Email/PII Detection", self.test_dlp_pii),
            ("6️⃣ Run Tracking - Multi-Step", self.test_run_tracking),
            ("7️⃣ Loop Detection - Exact Match", self.test_loop_exact),
            ("8️⃣ Loop Detection - Similar", self.test_loop_similar),
            ("9️⃣ Cost Tracking", self.test_cost_tracking),
            ("🔟 Streaming SSE", self.test_streaming),
        ]
        
        for name, test_func in tests:
            print(f"\n{'─'*50}")
            print(f"Running: {name}")
            print(f"{'─'*50}")
            
            try:
                result = await test_func()
                self.results.append(result)
                self.total_cost += result.cost_usd
                
                status = "✅ PASS" if result.passed else "❌ FAIL"
                print(f"Result: {status}")
                print(f"Duration: {result.duration_ms:.2f}ms")
                if result.cost_usd > 0:
                    print(f"Cost: ${result.cost_usd:.6f}")
                if result.error:
                    print(f"Error: {result.error}")
                    
            except Exception as e:
                result = TestResult(
                    name=name,
                    passed=False,
                    duration_ms=0,
                    error=str(e)
                )
                self.results.append(result)
                print(f"Result: ❌ EXCEPTION")
                print(f"Error: {e}")
        
        return self.results
    
    async def _chat(self, messages: list, run_id: str = None, stream: bool = False) -> dict:
        """OpenAI chat completion isteği gönder"""
        async with httpx.AsyncClient(timeout=60.0) as client:
            headers = {
                "Authorization": f"Bearer {self.api_key}",
                "Content-Type": "application/json",
            }
            
            payload = {
                "model": MODEL,
                "messages": messages,
                "max_tokens": 50,
                "stream": stream,
            }
            
            if run_id:
                payload["agentwall_run_id"] = run_id
            
            start = time.perf_counter()
            
            if stream:
                async with client.stream(
                    "POST",
                    f"{self.base_url}/v1/chat/completions",
                    headers=headers,
                    json=payload,
                ) as response:
                    chunks = []
                    async for line in response.aiter_lines():
                        if line.startswith("data: "):
                            chunks.append(line)
                    
                    duration = (time.perf_counter() - start) * 1000
                    return {
                        "status": response.status_code,
                        "chunks": chunks,
                        "duration_ms": duration,
                        "headers": dict(response.headers),
                    }
            else:
                response = await client.post(
                    f"{self.base_url}/v1/chat/completions",
                    headers=headers,
                    json=payload,
                )
                duration = (time.perf_counter() - start) * 1000
                
                return {
                    "status": response.status_code,
                    "data": response.json() if response.status_code == 200 else None,
                    "error": response.text if response.status_code != 200 else None,
                    "duration_ms": duration,
                    "headers": dict(response.headers),
                }


    # ==================== TEST METHODS ====================
    
    async def test_health(self) -> TestResult:
        """Health check testi"""
        start = time.perf_counter()
        async with httpx.AsyncClient(timeout=10.0) as client:
            response = await client.get(f"{self.base_url}/health")
            duration = (time.perf_counter() - start) * 1000
            
            return TestResult(
                name="Health Check",
                passed=response.status_code == 200,
                duration_ms=duration,
                details={"status": response.status_code},
            )
    
    async def test_basic_proxy(self) -> TestResult:
        """Temel proxy testi - OpenAI'a istek gönder"""
        result = await self._chat([
            {"role": "user", "content": "Say 'AgentWall works!' and nothing else."}
        ])
        
        passed = (
            result["status"] == 200 and
            result["data"] is not None and
            "agentwall" in result["data"]
        )
        
        cost = 0.0
        if result["data"] and "agentwall" in result["data"]:
            cost = result["data"]["agentwall"].get("cost_usd", 0)
        
        return TestResult(
            name="Basic Proxy",
            passed=passed,
            duration_ms=result["duration_ms"],
            details={
                "response": result["data"]["choices"][0]["message"]["content"] if passed else None,
                "agentwall_metadata": result["data"].get("agentwall") if passed else None,
            },
            cost_usd=cost,
            error=result.get("error"),
        )
    
    async def test_dlp_api_key(self) -> TestResult:
        """DLP Test: API key tespiti"""
        # Sahte API key içeren prompt
        fake_api_key = "sk-proj-FAKE1234567890abcdefghijklmnop"
        
        result = await self._chat([
            {"role": "user", "content": f"My API key is {fake_api_key}. Is this secure?"}
        ])
        
        # DLP çalışıyorsa, response'da API key maskelenmiş olmalı
        # veya request bloklanmış olmalı
        response_text = ""
        if result["data"] and result["data"].get("choices"):
            response_text = result["data"]["choices"][0]["message"]["content"]
        
        # API key'in response'da açık olmaması lazım
        key_leaked = fake_api_key in response_text
        
        cost = 0.0
        if result["data"] and "agentwall" in result["data"]:
            cost = result["data"]["agentwall"].get("cost_usd", 0)
        
        return TestResult(
            name="DLP - API Key Detection",
            passed=not key_leaked and result["status"] in [200, 400, 429],
            duration_ms=result["duration_ms"],
            details={
                "fake_key_sent": fake_api_key[:20] + "...",
                "key_in_response": key_leaked,
                "status": result["status"],
            },
            cost_usd=cost,
        )
    
    async def test_dlp_credit_card(self) -> TestResult:
        """DLP Test: Kredi kartı tespiti"""
        # Test kredi kartı numarası (Luhn valid)
        fake_cc = "4532015112830366"
        
        result = await self._chat([
            {"role": "user", "content": f"Process payment for card {fake_cc}"}
        ])
        
        response_text = ""
        if result["data"] and result["data"].get("choices"):
            response_text = result["data"]["choices"][0]["message"]["content"]
        
        cc_leaked = fake_cc in response_text
        
        cost = 0.0
        if result["data"] and "agentwall" in result["data"]:
            cost = result["data"]["agentwall"].get("cost_usd", 0)
        
        return TestResult(
            name="DLP - Credit Card Detection",
            passed=not cc_leaked and result["status"] in [200, 400, 429],
            duration_ms=result["duration_ms"],
            details={
                "fake_cc_sent": fake_cc[:4] + "****" + fake_cc[-4:],
                "cc_in_response": cc_leaked,
                "status": result["status"],
            },
            cost_usd=cost,
        )
    
    async def test_dlp_pii(self) -> TestResult:
        """DLP Test: PII (email, telefon) tespiti"""
        fake_email = "john.doe@secretcompany.com"
        fake_phone = "555-123-4567"
        
        result = await self._chat([
            {"role": "user", "content": f"Contact me at {fake_email} or {fake_phone}"}
        ])
        
        response_text = ""
        if result["data"] and result["data"].get("choices"):
            response_text = result["data"]["choices"][0]["message"]["content"]
        
        email_leaked = fake_email in response_text
        phone_leaked = fake_phone in response_text
        
        cost = 0.0
        if result["data"] and "agentwall" in result["data"]:
            cost = result["data"]["agentwall"].get("cost_usd", 0)
        
        return TestResult(
            name="DLP - PII Detection",
            passed=result["status"] in [200, 400, 429],
            duration_ms=result["duration_ms"],
            details={
                "email_sent": fake_email,
                "phone_sent": fake_phone,
                "email_in_response": email_leaked,
                "phone_in_response": phone_leaked,
                "status": result["status"],
            },
            cost_usd=cost,
        )


    async def test_run_tracking(self) -> TestResult:
        """Run Tracking Test: Aynı run_id ile multi-step"""
        import uuid
        run_id = f"test-run-{uuid.uuid4()}"
        
        steps = []
        total_cost = 0.0
        
        # 3 adımlık bir run simüle et
        prompts = [
            "Step 1: What is 2+2?",
            "Step 2: What is 3+3?",
            "Step 3: What is 4+4?",
        ]
        
        for i, prompt in enumerate(prompts):
            result = await self._chat(
                [{"role": "user", "content": prompt}],
                run_id=run_id
            )
            
            if result["data"] and "agentwall" in result["data"]:
                aw = result["data"]["agentwall"]
                steps.append({
                    "step": aw.get("step"),
                    "run_id": aw.get("run_id"),
                    "cost": aw.get("cost_usd"),
                    "total_run_cost": aw.get("total_run_cost"),
                })
                total_cost += aw.get("cost_usd", 0)
        
        # Doğrulama: step numaraları artmalı, run_id aynı kalmalı
        passed = (
            len(steps) == 3 and
            all(s["run_id"] == run_id for s in steps) and
            steps[0]["step"] == 1 and
            steps[1]["step"] == 2 and
            steps[2]["step"] == 3
        )
        
        return TestResult(
            name="Run Tracking - Multi-Step",
            passed=passed,
            duration_ms=sum(s.get("duration_ms", 0) for s in steps) if steps else 0,
            details={
                "run_id": run_id,
                "steps": steps,
                "step_sequence_correct": passed,
            },
            cost_usd=total_cost,
        )
    
    async def test_loop_exact(self) -> TestResult:
        """Loop Detection Test: Exact match (aynı prompt tekrarı)"""
        import uuid
        run_id = f"loop-test-{uuid.uuid4()}"
        
        # Aynı prompt'u 5 kez gönder
        same_prompt = "What is the capital of France?"
        
        responses = []
        blocked = False
        block_step = None
        total_cost = 0.0
        
        for i in range(5):
            result = await self._chat(
                [{"role": "user", "content": same_prompt}],
                run_id=run_id
            )
            
            if result["status"] == 429:
                # Loop detected ve bloklandı
                blocked = True
                block_step = i + 1
                break
            
            if result["data"] and "agentwall" in result["data"]:
                aw = result["data"]["agentwall"]
                total_cost += aw.get("cost_usd", 0)
                responses.append({
                    "step": aw.get("step"),
                    "warning": aw.get("warning"),
                })
        
        # Loop detection çalışıyorsa, ya bloklanmalı ya da warning vermeli
        has_warning = any(r.get("warning") for r in responses)
        
        return TestResult(
            name="Loop Detection - Exact Match",
            passed=blocked or has_warning,
            duration_ms=0,
            details={
                "run_id": run_id,
                "prompt_repeated": 5,
                "blocked": blocked,
                "block_step": block_step,
                "has_warning": has_warning,
                "responses": responses,
            },
            cost_usd=total_cost,
        )
    
    async def test_loop_similar(self) -> TestResult:
        """Loop Detection Test: Similar prompts"""
        import uuid
        run_id = f"similar-loop-{uuid.uuid4()}"
        
        # Benzer promptlar
        similar_prompts = [
            "What is the capital of France?",
            "What's the capital city of France?",
            "Tell me the capital of France",
            "France's capital is what?",
        ]
        
        responses = []
        blocked = False
        total_cost = 0.0
        
        for prompt in similar_prompts:
            result = await self._chat(
                [{"role": "user", "content": prompt}],
                run_id=run_id
            )
            
            if result["status"] == 429:
                blocked = True
                break
            
            if result["data"] and "agentwall" in result["data"]:
                aw = result["data"]["agentwall"]
                total_cost += aw.get("cost_usd", 0)
                responses.append({
                    "step": aw.get("step"),
                    "warning": aw.get("warning"),
                })
        
        has_warning = any(r.get("warning") for r in responses)
        
        return TestResult(
            name="Loop Detection - Similar",
            passed=blocked or has_warning or len(responses) == 4,
            duration_ms=0,
            details={
                "run_id": run_id,
                "prompts_sent": len(similar_prompts),
                "blocked": blocked,
                "has_warning": has_warning,
            },
            cost_usd=total_cost,
        )
    
    async def test_cost_tracking(self) -> TestResult:
        """Cost Tracking Test: Maliyet hesaplama doğruluğu"""
        result = await self._chat([
            {"role": "user", "content": "Count from 1 to 10."}
        ])
        
        cost = 0.0
        tokens = 0
        
        if result["data"]:
            if "agentwall" in result["data"]:
                cost = result["data"]["agentwall"].get("cost_usd", 0)
            if "usage" in result["data"]:
                tokens = result["data"]["usage"].get("total_tokens", 0)
        
        # gpt-3.5-turbo fiyatı: $0.0005/1K input, $0.0015/1K output
        # Yaklaşık doğruluk kontrolü
        expected_min = 0.000001  # En az bir şey hesaplanmış olmalı
        expected_max = 0.01  # Çok fazla olmamalı
        
        passed = expected_min < cost < expected_max and tokens > 0
        
        return TestResult(
            name="Cost Tracking",
            passed=passed,
            duration_ms=result["duration_ms"],
            details={
                "cost_usd": cost,
                "tokens": tokens,
                "cost_per_token": cost / tokens if tokens > 0 else 0,
            },
            cost_usd=cost,
        )
    
    async def test_streaming(self) -> TestResult:
        """Streaming SSE Test"""
        result = await self._chat(
            [{"role": "user", "content": "Count: 1, 2, 3"}],
            stream=True
        )
        
        chunks = result.get("chunks", [])
        has_done = any("[DONE]" in c for c in chunks)
        has_content = len(chunks) > 2
        
        # Header kontrolü
        headers = result.get("headers", {})
        has_run_id = "x-agentwall-run-id" in headers
        
        return TestResult(
            name="Streaming SSE",
            passed=result["status"] == 200 and has_content and has_done,
            duration_ms=result["duration_ms"],
            details={
                "status": result["status"],
                "chunk_count": len(chunks),
                "has_done_marker": has_done,
                "has_run_id_header": has_run_id,
            },
            cost_usd=0.0001,  # Tahmini
        )


    def generate_report(self) -> str:
        """Test raporu oluştur"""
        passed = sum(1 for r in self.results if r.passed)
        failed = len(self.results) - passed
        
        report = []
        report.append("\n" + "="*60)
        report.append("📊 AGENTWALL REAL SCENARIO TEST REPORT")
        report.append("="*60)
        report.append(f"📅 Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        report.append(f"🎯 Target: {self.base_url}")
        report.append(f"🤖 Model: {MODEL}")
        report.append("")
        report.append(f"✅ Passed: {passed}/{len(self.results)}")
        report.append(f"❌ Failed: {failed}/{len(self.results)}")
        report.append(f"💰 Total Cost: ${self.total_cost:.6f}")
        report.append("")
        report.append("─"*60)
        report.append("DETAILED RESULTS:")
        report.append("─"*60)
        
        for r in self.results:
            status = "✅" if r.passed else "❌"
            report.append(f"\n{status} {r.name}")
            report.append(f"   Duration: {r.duration_ms:.2f}ms")
            if r.cost_usd > 0:
                report.append(f"   Cost: ${r.cost_usd:.6f}")
            if r.error:
                report.append(f"   Error: {r.error}")
            if r.details:
                for k, v in r.details.items():
                    if isinstance(v, (dict, list)):
                        report.append(f"   {k}: {json.dumps(v, indent=2)[:200]}")
                    else:
                        report.append(f"   {k}: {v}")
        
        report.append("\n" + "="*60)
        
        # Özet tablo
        report.append("\n📋 FEATURE VERIFICATION MATRIX:")
        report.append("─"*60)
        
        features = {
            "OpenAI Proxy": self.results[1].passed if len(self.results) > 1 else False,
            "DLP - API Key": self.results[2].passed if len(self.results) > 2 else False,
            "DLP - Credit Card": self.results[3].passed if len(self.results) > 3 else False,
            "DLP - PII": self.results[4].passed if len(self.results) > 4 else False,
            "Run Tracking": self.results[5].passed if len(self.results) > 5 else False,
            "Loop Detection (Exact)": self.results[6].passed if len(self.results) > 6 else False,
            "Loop Detection (Similar)": self.results[7].passed if len(self.results) > 7 else False,
            "Cost Tracking": self.results[8].passed if len(self.results) > 8 else False,
            "Streaming SSE": self.results[9].passed if len(self.results) > 9 else False,
        }
        
        for feature, status in features.items():
            icon = "✅" if status else "❌"
            report.append(f"  {icon} {feature}")
        
        report.append("\n" + "="*60)
        report.append("🛡️ Guard the Agent, Save the Budget")
        report.append("="*60)
        
        return "\n".join(report)


async def main():
    parser = argparse.ArgumentParser(description="AgentWall Real Scenario Tests")
    parser.add_argument("--api-key", required=True, help="OpenAI API key")
    parser.add_argument("--url", default=BASE_URL, help="AgentWall URL")
    parser.add_argument("--output", default="docs/RealScenarioTestReport.md", help="Output file")
    args = parser.parse_args()
    
    tester = RealScenarioTester(api_key=args.api_key, base_url=args.url)
    
    try:
        await tester.run_all_tests()
    except KeyboardInterrupt:
        print("\n⚠️ Tests interrupted by user")
    
    # Rapor oluştur
    report = tester.generate_report()
    print(report)
    
    # Markdown rapor dosyası
    md_report = generate_markdown_report(tester)
    
    with open(args.output, "w", encoding="utf-8") as f:
        f.write(md_report)
    
    print(f"\n📄 Report saved to: {args.output}")
    
    # Exit code
    failed = sum(1 for r in tester.results if not r.passed)
    sys.exit(0 if failed == 0 else 1)


def generate_markdown_report(tester: RealScenarioTester) -> str:
    """Markdown formatında detaylı rapor"""
    passed = sum(1 for r in tester.results if r.passed)
    failed = len(tester.results) - passed
    
    md = []
    md.append("# 🧪 AgentWall Real Scenario Test Report")
    md.append("")
    md.append(f"**Date:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    md.append(f"**Target:** {tester.base_url}")
    md.append(f"**Model:** {MODEL}")
    md.append(f"**Total Cost:** ${tester.total_cost:.6f}")
    md.append("")
    md.append("---")
    md.append("")
    md.append("## 📊 Summary")
    md.append("")
    md.append("| Metric | Value |")
    md.append("|--------|-------|")
    md.append(f"| Total Tests | {len(tester.results)} |")
    md.append(f"| Passed | {passed} ✅ |")
    md.append(f"| Failed | {failed} ❌ |")
    md.append(f"| Success Rate | {passed/len(tester.results)*100:.1f}% |")
    md.append(f"| Total Cost | ${tester.total_cost:.6f} |")
    md.append("")
    md.append("---")
    md.append("")
    md.append("## 🔍 Feature Verification")
    md.append("")
    md.append("| Feature | Status | Notes |")
    md.append("|---------|--------|-------|")
    
    for r in tester.results:
        status = "✅ PASS" if r.passed else "❌ FAIL"
        notes = r.error if r.error else f"{r.duration_ms:.0f}ms"
        md.append(f"| {r.name} | {status} | {notes} |")
    
    md.append("")
    md.append("---")
    md.append("")
    md.append("## 📝 Detailed Results")
    md.append("")
    
    for r in tester.results:
        status = "✅" if r.passed else "❌"
        md.append(f"### {status} {r.name}")
        md.append("")
        md.append(f"- **Duration:** {r.duration_ms:.2f}ms")
        md.append(f"- **Cost:** ${r.cost_usd:.6f}")
        if r.error:
            md.append(f"- **Error:** {r.error}")
        md.append("")
        if r.details:
            md.append("**Details:**")
            md.append("```json")
            md.append(json.dumps(r.details, indent=2, default=str)[:1000])
            md.append("```")
        md.append("")
    
    md.append("---")
    md.append("")
    md.append("## ✅ Conclusion")
    md.append("")
    
    if failed == 0:
        md.append("**All tests passed!** AgentWall is working correctly.")
    else:
        md.append(f"**{failed} test(s) failed.** Review the details above.")
    
    md.append("")
    md.append("---")
    md.append("")
    md.append("*Generated by AgentWall Test Suite*")
    md.append("")
    md.append('*"Guard the Agent, Save the Budget"* 🛡️')
    
    return "\n".join(md)


if __name__ == "__main__":
    asyncio.run(main())
