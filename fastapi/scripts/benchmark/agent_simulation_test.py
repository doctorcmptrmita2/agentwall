#!/usr/bin/env python3
"""
AgentWall Agent Simulation Test
Gerçek bir AI Agent davranışını simüle eder:
1. Aynı run_id ile birden fazla request
2. Loop detection testi
3. Budget limit testi
4. Kill-switch testi

Bu test, AgentWall'un MOAT özelliklerini doğrular.
"""

import asyncio
import aiohttp
import json
import uuid
from datetime import datetime
from typing import Optional

PRODUCTION_URL = "https://api.agentwall.io"
API_KEY = "aw-bJDiC5gtDnYJjIag9jQTzQyJr4RMotPX"


class AgentSimulator:
    """Bir AI Agent'ın davranışını simüle eder"""
    
    def __init__(self, base_url: str = PRODUCTION_URL, api_key: str = API_KEY):
        self.base_url = base_url
        self.api_key = api_key
        self.run_id: Optional[str] = None
        self.step = 0
        self.total_cost = 0.0
        self.total_tokens = 0
    
    async def start_run(self, run_id: Optional[str] = None):
        """Yeni bir agent run başlat"""
        self.run_id = run_id or f"agent-sim-{uuid.uuid4().hex[:8]}"
        self.step = 0
        self.total_cost = 0.0
        self.total_tokens = 0
        print(f"\n🚀 Starting Agent Run: {self.run_id}")
        return self.run_id
    
    async def send_message(
        self, 
        session: aiohttp.ClientSession,
        content: str,
        model: str = "gpt-3.5-turbo",
        max_tokens: int = 100
    ) -> dict:
        """Agent olarak bir mesaj gönder"""
        self.step += 1
        
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
            "X-AgentWall-Run-ID": self.run_id,
            "X-AgentWall-Step": str(self.step)
        }
        
        payload = {
            "model": model,
            "messages": [{"role": "user", "content": content}],
            "max_tokens": max_tokens
        }
        
        try:
            async with session.post(
                f"{self.base_url}/v1/chat/completions",
                json=payload,
                headers=headers,
                timeout=60
            ) as resp:
                result = {
                    "status": resp.status,
                    "step": self.step,
                    "headers": dict(resp.headers)
                }
                
                if resp.status == 200:
                    data = await resp.json()
                    result["data"] = data
                    
                    # Track costs
                    if "agentwall" in data:
                        aw = data["agentwall"]
                        cost = aw.get("cost_usd", 0)
                        self.total_cost += cost
                        result["cost"] = cost
                        result["run_cost"] = self.total_cost
                        result["loop_detected"] = aw.get("loop_detected", False)
                    
                    if "usage" in data:
                        tokens = data["usage"].get("total_tokens", 0)
                        self.total_tokens += tokens
                        result["tokens"] = tokens
                    
                    # Get response content
                    if "choices" in data and data["choices"]:
                        result["response"] = data["choices"][0].get("message", {}).get("content", "")
                else:
                    result["error"] = await resp.text()
                
                return result
                
        except Exception as e:
            return {"status": 0, "error": str(e), "step": self.step}


async def test_normal_agent_flow():
    """Normal bir agent akışını test et"""
    print("\n" + "="*70)
    print("🤖 TEST 1: NORMAL AGENT FLOW")
    print("="*70)
    
    agent = AgentSimulator()
    await agent.start_run()
    
    # Farklı görevler - loop olmamalı
    tasks = [
        "What is the capital of France?",
        "What is 2 + 2?",
        "List 3 programming languages",
        "What color is the sky?",
        "Name a famous scientist"
    ]
    
    async with aiohttp.ClientSession() as session:
        for i, task in enumerate(tasks):
            print(f"\n📤 Step {i+1}: {task[:40]}...")
            result = await agent.send_message(session, task, max_tokens=50)
            
            if result["status"] == 200:
                print(f"   ✅ Status: {result['status']}")
                print(f"   💰 Cost: ${result.get('cost', 0):.6f}")
                print(f"   🔄 Loop: {result.get('loop_detected', False)}")
                print(f"   📝 Response: {result.get('response', '')[:50]}...")
            else:
                print(f"   ❌ Error: {result.get('error', 'Unknown')[:100]}")
            
            await asyncio.sleep(0.3)
    
    print(f"\n📊 Run Summary:")
    print(f"   Total Steps: {agent.step}")
    print(f"   Total Cost: ${agent.total_cost:.6f}")
    print(f"   Total Tokens: {agent.total_tokens}")
    
    return agent


async def test_loop_detection():
    """Loop detection'ı test et - aynı prompt'u tekrarla"""
    print("\n" + "="*70)
    print("🔄 TEST 2: LOOP DETECTION (Same Prompt Repetition)")
    print("="*70)
    
    agent = AgentSimulator()
    await agent.start_run()
    
    # Aynı prompt'u 10 kez gönder - loop tespit edilmeli
    repeated_prompt = "What is 2+2? Just give me the number."
    
    async with aiohttp.ClientSession() as session:
        for i in range(10):
            print(f"\n📤 Step {i+1}: Sending same prompt...")
            result = await agent.send_message(session, repeated_prompt, max_tokens=10)
            
            if result["status"] == 200:
                loop_detected = result.get("loop_detected", False)
                print(f"   Status: {result['status']}")
                print(f"   Loop Detected: {'⚠️ YES' if loop_detected else '❌ NO'}")
                print(f"   Response: {result.get('response', '')[:30]}...")
                
                if loop_detected:
                    print(f"\n   🛑 LOOP DETECTED at step {i+1}!")
                    break
            elif result["status"] == 429:
                print(f"   ⚠️ Rate limited or killed!")
                print(f"   Message: {result.get('error', '')[:100]}")
                break
            else:
                print(f"   ❌ Error: {result.get('error', 'Unknown')[:100]}")
            
            await asyncio.sleep(0.3)
    
    print(f"\n📊 Loop Test Summary:")
    print(f"   Steps before detection/limit: {agent.step}")
    print(f"   Total Cost: ${agent.total_cost:.6f}")


async def test_oscillation_pattern():
    """Oscillation pattern testi - A->B->A->B"""
    print("\n" + "="*70)
    print("🔄 TEST 3: OSCILLATION PATTERN (A->B->A->B)")
    print("="*70)
    
    agent = AgentSimulator()
    await agent.start_run()
    
    prompts = ["What is Python?", "What is JavaScript?"]
    
    async with aiohttp.ClientSession() as session:
        for i in range(8):
            prompt = prompts[i % 2]  # Alternate between two prompts
            print(f"\n📤 Step {i+1}: {prompt}")
            result = await agent.send_message(session, prompt, max_tokens=30)
            
            if result["status"] == 200:
                loop_detected = result.get("loop_detected", False)
                print(f"   Loop Detected: {'⚠️ YES' if loop_detected else '❌ NO'}")
                
                if loop_detected:
                    print(f"\n   🛑 OSCILLATION DETECTED at step {i+1}!")
                    break
            else:
                print(f"   ❌ Error: {result.get('error', 'Unknown')[:100]}")
                break
            
            await asyncio.sleep(0.3)
    
    print(f"\n📊 Oscillation Test Summary:")
    print(f"   Steps: {agent.step}")
    print(f"   Total Cost: ${agent.total_cost:.6f}")


async def test_budget_tracking():
    """Budget tracking ve limit testi"""
    print("\n" + "="*70)
    print("💰 TEST 4: BUDGET TRACKING")
    print("="*70)
    
    agent = AgentSimulator()
    await agent.start_run()
    
    # Birkaç request gönder ve cost'u takip et
    prompts = [
        "Write a short poem about AI",
        "Explain machine learning in 2 sentences",
        "What are the benefits of cloud computing?",
        "Describe the future of technology"
    ]
    
    async with aiohttp.ClientSession() as session:
        for i, prompt in enumerate(prompts):
            print(f"\n📤 Step {i+1}: {prompt[:40]}...")
            result = await agent.send_message(session, prompt, max_tokens=100)
            
            if result["status"] == 200:
                print(f"   ✅ Cost this request: ${result.get('cost', 0):.6f}")
                print(f"   💰 Running total: ${agent.total_cost:.6f}")
                print(f"   📊 Tokens: {result.get('tokens', 0)}")
            else:
                print(f"   ❌ Error: {result.get('error', 'Unknown')[:100]}")
            
            await asyncio.sleep(0.3)
    
    print(f"\n📊 Budget Summary:")
    print(f"   Total Steps: {agent.step}")
    print(f"   Total Cost: ${agent.total_cost:.6f}")
    print(f"   Total Tokens: {agent.total_tokens}")
    print(f"   Avg Cost/Request: ${agent.total_cost/agent.step:.6f}")


async def test_multi_step_task():
    """Çok adımlı bir görev simülasyonu"""
    print("\n" + "="*70)
    print("📋 TEST 5: MULTI-STEP TASK SIMULATION")
    print("="*70)
    
    agent = AgentSimulator()
    await agent.start_run()
    
    # Bir araştırma görevi simüle et
    task_steps = [
        "I need to research about renewable energy. First, what are the main types?",
        "Tell me more about solar energy specifically",
        "What are the advantages of solar energy?",
        "What are the disadvantages?",
        "How does solar energy compare to wind energy?",
        "What is the future outlook for solar energy?",
        "Summarize the key points about solar energy in 3 bullet points"
    ]
    
    async with aiohttp.ClientSession() as session:
        for i, step in enumerate(task_steps):
            print(f"\n📤 Step {i+1}: {step[:50]}...")
            result = await agent.send_message(session, step, max_tokens=150)
            
            if result["status"] == 200:
                print(f"   ✅ Completed")
                print(f"   💰 Cost: ${result.get('cost', 0):.6f} (Total: ${agent.total_cost:.6f})")
            else:
                print(f"   ❌ Error: {result.get('error', 'Unknown')[:100]}")
                break
            
            await asyncio.sleep(0.5)
    
    print(f"\n📊 Multi-Step Task Summary:")
    print(f"   Total Steps: {agent.step}")
    print(f"   Total Cost: ${agent.total_cost:.6f}")
    print(f"   Total Tokens: {agent.total_tokens}")


async def main():
    """Tüm agent simülasyon testlerini çalıştır"""
    print("\n" + "="*70)
    print("🛡️ AGENTWALL AGENT SIMULATION TEST SUITE")
    print("="*70)
    print(f"Target: {PRODUCTION_URL}")
    print(f"Time: {datetime.now().isoformat()}")
    print("="*70)
    
    # Test 1: Normal flow
    await test_normal_agent_flow()
    
    # Test 2: Loop detection
    await test_loop_detection()
    
    # Test 3: Oscillation
    await test_oscillation_pattern()
    
    # Test 4: Budget tracking
    await test_budget_tracking()
    
    # Test 5: Multi-step task
    await test_multi_step_task()
    
    print("\n" + "="*70)
    print("✅ ALL AGENT SIMULATION TESTS COMPLETE")
    print("="*70)


if __name__ == "__main__":
    asyncio.run(main())
