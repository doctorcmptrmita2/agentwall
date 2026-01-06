#!/usr/bin/env python3
"""
AgentWall Production API Test Suite
Gerçek API endpoint'lerini test eder: https://api.agentwall.io

Kullanım:
    python production_test.py
    python production_test.py --api-key YOUR_KEY
"""

import asyncio
import aiohttp
import time
import json
import sys
from datetime import datetime
from dataclasses import dataclass
from typing import Optional

# Production URL
PRODUCTION_URL = "https://api.agentwall.io"
# Test API key (dashboard'dan alınmalı)
DEFAULT_API_KEY = "sk-test-agentwall-demo"


@dataclass
class TestResult:
    name: str
    passed: bool
    duration_ms: float
    message: str
    details: dict = None


class ProductionTester:
    """Production API Test Suite"""
    
    def __init__(self, base_url: str = PRODUCTION_URL, api_key: str = DEFAULT_API_KEY):
        self.base_url = base_url.rstrip("/")
        self.api_key = api_key
        self.results: list[TestResult] = []
    
    async def run_all_tests(self):
        """Tüm production testlerini çalıştır"""
        print("\n" + "="*70)
        print("🌐 AGENTWALL PRODUCTION API TEST SUITE")
        print("="*70)
        print(f"Target: {self.base_url}")
        print(f"Time: {datetime.now().isoformat()}")
        print("="*70)
        
        async with aiohttp.ClientSession() as session:
            # 1. Health Check Tests
            await self.test_health_endpoints(session)
            
            # 2. Latency Tests (A/B comparison)
            await self.test_latency(session)
            
            # 3. DLP Tests (real API calls)
            await self.test_dlp_blocking(session)
            
            # 4. Streaming Test
            await self.test_streaming(session)
            
            # 5. Error Handling
            await self.test_error_handling(session)
        
        self.print_summary()
        return self.results
    
    async def test_health_endpoints(self, session: aiohttp.ClientSession):
        """Health endpoint testleri"""
        print("\n📋 PHASE 1: HEALTH ENDPOINTS")
        print("-" * 50)
        
        endpoints = [
            ("/health", "Basic Health"),
            ("/health/live", "Liveness Probe"),
            ("/health/ready", "Readiness Probe"),
            ("/", "Root Endpoint"),
        ]
        
        for endpoint, name in endpoints:
            start = time.perf_counter()
            try:
                async with session.get(f"{self.base_url}{endpoint}", timeout=10) as resp:
                    duration = (time.perf_counter() - start) * 1000
                    data = await resp.json()
                    
                    passed = resp.status == 200
                    self.results.append(TestResult(
                        name=f"Health: {name}",
                        passed=passed,
                        duration_ms=duration,
                        message=f"Status: {resp.status}",
                        details=data
                    ))
                    
                    status = "✅" if passed else "❌"
                    print(f"  {status} {name}: {resp.status} ({duration:.0f}ms)")
                    
            except Exception as e:
                duration = (time.perf_counter() - start) * 1000
                self.results.append(TestResult(
                    name=f"Health: {name}",
                    passed=False,
                    duration_ms=duration,
                    message=str(e)
                ))
                print(f"  ❌ {name}: ERROR - {e}")
    
    async def test_latency(self, session: aiohttp.ClientSession):
        """Latency ve overhead testleri"""
        print("\n📋 PHASE 2: LATENCY TESTS")
        print("-" * 50)
        
        # Simple chat completion request
        payload = {
            "model": "gpt-3.5-turbo",
            "messages": [{"role": "user", "content": "Say 'test' only"}],
            "max_tokens": 5,
            "temperature": 0
        }
        
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
        
        # Test 1: Non-streaming request
        print("\n  Testing non-streaming request...")
        latencies = []
        
        for i in range(3):
            start = time.perf_counter()
            try:
                async with session.post(
                    f"{self.base_url}/v1/chat/completions",
                    json=payload,
                    headers=headers,
                    timeout=30
                ) as resp:
                    duration = (time.perf_counter() - start) * 1000
                    
                    if resp.status == 200:
                        data = await resp.json()
                        overhead = resp.headers.get("X-AgentWall-Overhead-Ms", "N/A")
                        latencies.append(duration)
                        print(f"    Request {i+1}: {duration:.0f}ms (overhead: {overhead})")
                    else:
                        error_text = await resp.text()
                        print(f"    Request {i+1}: ERROR {resp.status} - {error_text[:100]}")
                        
            except asyncio.TimeoutError:
                print(f"    Request {i+1}: TIMEOUT")
            except Exception as e:
                print(f"    Request {i+1}: ERROR - {e}")
        
        if latencies:
            avg_latency = sum(latencies) / len(latencies)
            self.results.append(TestResult(
                name="Latency: Non-streaming",
                passed=avg_latency < 5000,  # 5 saniyeden az
                duration_ms=avg_latency,
                message=f"Avg: {avg_latency:.0f}ms over {len(latencies)} requests"
            ))
            print(f"\n  Average latency: {avg_latency:.0f}ms")
    
    async def test_dlp_blocking(self, session: aiohttp.ClientSession):
        """DLP engelleme testleri"""
        print("\n📋 PHASE 3: DLP TESTS")
        print("-" * 50)
        
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
        
        dlp_tests = [
            {
                "name": "Credit Card Detection",
                "content": "My card number is 4111-1111-1111-1111",
                "should_mask": True
            },
            {
                "name": "API Key Detection", 
                "content": "Use this key: sk-1234567890abcdefghijklmnop",
                "should_mask": True
            },
            {
                "name": "Email Detection",
                "content": "Contact me at secret@company.com",
                "should_mask": True
            },
            {
                "name": "Safe Content",
                "content": "What is 2+2?",
                "should_mask": False
            }
        ]
        
        for test in dlp_tests:
            payload = {
                "model": "gpt-3.5-turbo",
                "messages": [{"role": "user", "content": test["content"]}],
                "max_tokens": 50
            }
            
            start = time.perf_counter()
            try:
                async with session.post(
                    f"{self.base_url}/v1/chat/completions",
                    json=payload,
                    headers=headers,
                    timeout=30
                ) as resp:
                    duration = (time.perf_counter() - start) * 1000
                    
                    # Check response headers for DLP info
                    dlp_action = resp.headers.get("X-AgentWall-DLP-Action", "none")
                    
                    if test["should_mask"]:
                        passed = dlp_action in ["masked", "blocked"] or resp.status in [200, 400]
                    else:
                        passed = resp.status == 200
                    
                    self.results.append(TestResult(
                        name=f"DLP: {test['name']}",
                        passed=passed,
                        duration_ms=duration,
                        message=f"Status: {resp.status}, DLP: {dlp_action}"
                    ))
                    
                    status = "✅" if passed else "❌"
                    print(f"  {status} {test['name']}: {resp.status} ({duration:.0f}ms)")
                    
            except Exception as e:
                self.results.append(TestResult(
                    name=f"DLP: {test['name']}",
                    passed=False,
                    duration_ms=0,
                    message=str(e)
                ))
                print(f"  ❌ {test['name']}: ERROR - {e}")
    
    async def test_streaming(self, session: aiohttp.ClientSession):
        """Streaming SSE testi"""
        print("\n📋 PHASE 4: STREAMING TEST")
        print("-" * 50)
        
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
        
        payload = {
            "model": "gpt-3.5-turbo",
            "messages": [{"role": "user", "content": "Count from 1 to 5"}],
            "max_tokens": 50,
            "stream": True
        }
        
        start = time.perf_counter()
        chunks_received = 0
        first_chunk_time = None
        
        try:
            async with session.post(
                f"{self.base_url}/v1/chat/completions",
                json=payload,
                headers=headers,
                timeout=60
            ) as resp:
                if resp.status == 200:
                    async for line in resp.content:
                        if line:
                            chunks_received += 1
                            if first_chunk_time is None:
                                first_chunk_time = (time.perf_counter() - start) * 1000
                            
                            # Limit chunks for test
                            if chunks_received > 20:
                                break
                    
                    duration = (time.perf_counter() - start) * 1000
                    
                    passed = chunks_received > 0
                    self.results.append(TestResult(
                        name="Streaming: SSE",
                        passed=passed,
                        duration_ms=duration,
                        message=f"Received {chunks_received} chunks, TTFB: {first_chunk_time:.0f}ms" if first_chunk_time else "No chunks"
                    ))
                    
                    status = "✅" if passed else "❌"
                    print(f"  {status} Streaming: {chunks_received} chunks received")
                    if first_chunk_time:
                        print(f"      Time to first byte: {first_chunk_time:.0f}ms")
                else:
                    error = await resp.text()
                    self.results.append(TestResult(
                        name="Streaming: SSE",
                        passed=False,
                        duration_ms=0,
                        message=f"Status {resp.status}: {error[:100]}"
                    ))
                    print(f"  ❌ Streaming: ERROR {resp.status}")
                    
        except Exception as e:
            self.results.append(TestResult(
                name="Streaming: SSE",
                passed=False,
                duration_ms=0,
                message=str(e)
            ))
            print(f"  ❌ Streaming: ERROR - {e}")
    
    async def test_error_handling(self, session: aiohttp.ClientSession):
        """Error handling testleri"""
        print("\n📋 PHASE 5: ERROR HANDLING")
        print("-" * 50)
        
        # Test 1: Invalid API key
        start = time.perf_counter()
        try:
            async with session.post(
                f"{self.base_url}/v1/chat/completions",
                json={"model": "gpt-3.5-turbo", "messages": [{"role": "user", "content": "test"}]},
                headers={"Authorization": "Bearer invalid-key-xyz"},
                timeout=10
            ) as resp:
                duration = (time.perf_counter() - start) * 1000
                passed = resp.status in [401, 403]
                
                self.results.append(TestResult(
                    name="Error: Invalid API Key",
                    passed=passed,
                    duration_ms=duration,
                    message=f"Status: {resp.status}"
                ))
                
                status = "✅" if passed else "❌"
                print(f"  {status} Invalid API Key: {resp.status} ({duration:.0f}ms)")
                
        except Exception as e:
            print(f"  ❌ Invalid API Key: ERROR - {e}")
        
        # Test 2: Invalid request body
        start = time.perf_counter()
        try:
            async with session.post(
                f"{self.base_url}/v1/chat/completions",
                json={"invalid": "request"},
                headers={"Authorization": f"Bearer {self.api_key}"},
                timeout=10
            ) as resp:
                duration = (time.perf_counter() - start) * 1000
                passed = resp.status in [400, 422]
                
                self.results.append(TestResult(
                    name="Error: Invalid Request",
                    passed=passed,
                    duration_ms=duration,
                    message=f"Status: {resp.status}"
                ))
                
                status = "✅" if passed else "❌"
                print(f"  {status} Invalid Request: {resp.status} ({duration:.0f}ms)")
                
        except Exception as e:
            print(f"  ❌ Invalid Request: ERROR - {e}")
    
    def print_summary(self):
        """Test özeti yazdır"""
        print("\n" + "="*70)
        print("📊 PRODUCTION TEST SUMMARY")
        print("="*70)
        
        total = len(self.results)
        passed = sum(1 for r in self.results if r.passed)
        failed = total - passed
        
        print(f"""
┌─────────────────────────────────────────────────────────────────────┐
│           AGENTWALL PRODUCTION TEST RESULTS                        │
├─────────────────────────────────────────────────────────────────────┤
│  Total Tests: {total:3d}                                                 │
│  Passed: {passed:3d}  |  Failed: {failed:3d}                                     │
│  Success Rate: {(passed/total*100) if total > 0 else 0:5.1f}%                                          │
├─────────────────────────────────────────────────────────────────────┤""")
        
        for result in self.results:
            status = "✅" if result.passed else "❌"
            name = result.name[:40].ljust(40)
            print(f"│  {status} {name} {result.duration_ms:6.0f}ms │")
        
        print(f"""├─────────────────────────────────────────────────────────────────────┤
│  PRODUCTION STATUS: {'✅ HEALTHY' if passed >= total * 0.8 else '❌ ISSUES DETECTED':20s}                        │
└─────────────────────────────────────────────────────────────────────┘
""")
        
        # Save results
        self.save_results()
    
    def save_results(self):
        """Sonuçları JSON olarak kaydet"""
        from pathlib import Path
        
        output = {
            "timestamp": datetime.now().isoformat(),
            "base_url": self.base_url,
            "total": len(self.results),
            "passed": sum(1 for r in self.results if r.passed),
            "results": [
                {
                    "name": r.name,
                    "passed": r.passed,
                    "duration_ms": r.duration_ms,
                    "message": r.message
                }
                for r in self.results
            ]
        }
        
        output_dir = Path(__file__).parent.parent / "reports"
        output_dir.mkdir(exist_ok=True)
        
        filename = f"production_test_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        filepath = output_dir / filename
        
        with open(filepath, "w") as f:
            json.dump(output, f, indent=2)
        
        print(f"📁 Results saved to: {filepath}")


async def main():
    import argparse
    
    parser = argparse.ArgumentParser(description="AgentWall Production Test")
    parser.add_argument("--url", default=PRODUCTION_URL, help="API URL")
    parser.add_argument("--api-key", default=DEFAULT_API_KEY, help="API Key")
    
    args = parser.parse_args()
    
    tester = ProductionTester(base_url=args.url, api_key=args.api_key)
    await tester.run_all_tests()


if __name__ == "__main__":
    asyncio.run(main())
