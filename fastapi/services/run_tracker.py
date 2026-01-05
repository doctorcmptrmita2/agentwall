"""
Run-Level Tracker - AgentWall's MOAT Feature

This is what differentiates us from LiteLLM/Portkey:
- They track individual requests
- We track entire agent runs (multiple steps)

Key capabilities:
- Step counting (detect infinite loops)
- Budget tracking per run
- Kill switch (stop runaway agents)
- Run replay (debug agent behavior)
"""

import asyncio
import json
import logging
from datetime import datetime, timedelta
from typing import Optional
from dataclasses import dataclass, field
from decimal import Decimal

import redis.asyncio as redis

from config import settings

logger = logging.getLogger(__name__)


@dataclass
class RunState:
    """Current state of an agent run"""
    run_id: str
    team_id: str
    user_id: str
    agent_id: str = ""
    
    # Counters
    step_count: int = 0
    total_tokens: int = 0
    total_cost: Decimal = Decimal("0")
    
    # Timing
    started_at: datetime = field(default_factory=datetime.utcnow)
    last_activity: datetime = field(default_factory=datetime.utcnow)
    
    # Status
    status: str = "running"  # running, completed, failed, killed
    kill_reason: str = ""
    
    # Flags
    loop_detected: bool = False
    budget_exceeded: bool = False
    
    # History for loop detection (last N prompts)
    recent_prompts: list[str] = field(default_factory=list)
    recent_responses: list[str] = field(default_factory=list)
    
    # Limits (from user's plan)
    max_steps: int = 30
    max_budget: Decimal = Decimal("10.0")
    timeout_seconds: int = 120


@dataclass
class StepResult:
    """Result of processing a step"""
    allowed: bool = True
    reason: str = ""
    step_number: int = 0
    warnings: list[str] = field(default_factory=list)


class RunTracker:
    """
    Manages run-level state using Redis
    
    Design decisions:
    - Redis for fast state access (<1ms)
    - TTL on keys to auto-cleanup old runs
    - Atomic operations for step counting
    """
    
    def __init__(self):
        self._redis: Optional[redis.Redis] = None
        self._connected = False
    
    async def connect(self):
        """Connect to Redis"""
        try:
            self._redis = redis.from_url(
                settings.REDIS_URL,
                encoding="utf-8",
                decode_responses=True,
                max_connections=settings.REDIS_MAX_CONNECTIONS,
            )
            await self._redis.ping()
            self._connected = True
            logger.info("Redis connected for run tracking")
        except Exception as e:
            logger.warning(f"Redis connection failed (run tracking will use in-memory fallback): {e}")
            self._connected = False
    
    async def disconnect(self):
        """Disconnect from Redis"""
        if self._redis:
            await self._redis.close()
            self._connected = False
    
    def _run_key(self, run_id: str) -> str:
        return f"agentwall:run:{run_id}"
    
    async def get_or_create_run(
        self,
        run_id: str,
        team_id: str,
        user_id: str,
        agent_id: str = "",
        limits: Optional[dict] = None,
    ) -> RunState:
        """Get existing run or create new one"""
        if not self._connected:
            # Fallback: return new state without persistence
            return RunState(
                run_id=run_id,
                team_id=team_id,
                user_id=user_id,
                agent_id=agent_id,
                max_steps=limits.get("max_steps", settings.MAX_STEPS) if limits else settings.MAX_STEPS,
                max_budget=Decimal(str(limits.get("daily_budget", 10.0))) if limits else Decimal("10.0"),
            )
        
        key = self._run_key(run_id)
        
        # Try to get existing run
        data = await self._redis.get(key)
        if data:
            state_dict = json.loads(data)
            return self._dict_to_state(state_dict)
        
        # Create new run
        state = RunState(
            run_id=run_id,
            team_id=team_id,
            user_id=user_id,
            agent_id=agent_id,
            max_steps=limits.get("max_steps", settings.MAX_STEPS) if limits else settings.MAX_STEPS,
            max_budget=Decimal(str(limits.get("daily_budget", 10.0))) if limits else Decimal("10.0"),
        )
        
        await self._save_state(state)
        return state

    async def _save_state(self, state: RunState):
        """Save run state to Redis"""
        if not self._connected:
            return
        
        key = self._run_key(state.run_id)
        data = self._state_to_dict(state)
        
        # TTL: 24 hours after last activity
        ttl = 86400  # 24 hours
        await self._redis.setex(key, ttl, json.dumps(data))
    
    def _state_to_dict(self, state: RunState) -> dict:
        return {
            "run_id": state.run_id,
            "team_id": state.team_id,
            "user_id": state.user_id,
            "agent_id": state.agent_id,
            "step_count": state.step_count,
            "total_tokens": state.total_tokens,
            "total_cost": str(state.total_cost),
            "started_at": state.started_at.isoformat(),
            "last_activity": state.last_activity.isoformat(),
            "status": state.status,
            "kill_reason": state.kill_reason,
            "loop_detected": state.loop_detected,
            "budget_exceeded": state.budget_exceeded,
            "recent_prompts": state.recent_prompts[-5:],  # Keep last 5
            "recent_responses": state.recent_responses[-5:],
            "max_steps": state.max_steps,
            "max_budget": str(state.max_budget),
            "timeout_seconds": state.timeout_seconds,
        }
    
    def _dict_to_state(self, data: dict) -> RunState:
        return RunState(
            run_id=data["run_id"],
            team_id=data["team_id"],
            user_id=data["user_id"],
            agent_id=data.get("agent_id", ""),
            step_count=data["step_count"],
            total_tokens=data["total_tokens"],
            total_cost=Decimal(data["total_cost"]),
            started_at=datetime.fromisoformat(data["started_at"]),
            last_activity=datetime.fromisoformat(data["last_activity"]),
            status=data["status"],
            kill_reason=data.get("kill_reason", ""),
            loop_detected=data.get("loop_detected", False),
            budget_exceeded=data.get("budget_exceeded", False),
            recent_prompts=data.get("recent_prompts", []),
            recent_responses=data.get("recent_responses", []),
            max_steps=data.get("max_steps", settings.MAX_STEPS),
            max_budget=Decimal(data.get("max_budget", "10.0")),
            timeout_seconds=data.get("timeout_seconds", 120),
        )
    
    async def process_step(
        self,
        run_id: str,
        team_id: str,
        user_id: str,
        agent_id: str = "",
        prompt: str = "",
        limits: Optional[dict] = None,
    ) -> tuple[RunState, StepResult]:
        """
        Process a new step in the run
        
        Returns: (updated state, step result with allowed/denied)
        
        This is the CORE governance logic:
        1. Check if run is killed
        2. Check step limit
        3. Check timeout
        4. Increment step counter
        """
        state = await self.get_or_create_run(run_id, team_id, user_id, agent_id, limits)
        result = StepResult(step_number=state.step_count + 1)
        
        # Check 1: Is run already killed?
        if state.status == "killed":
            result.allowed = False
            result.reason = f"Run killed: {state.kill_reason}"
            return state, result
        
        # Check 2: Step limit exceeded?
        if state.step_count >= state.max_steps:
            result.allowed = False
            result.reason = f"Step limit exceeded ({state.max_steps} steps)"
            state.status = "killed"
            state.kill_reason = "step_limit_exceeded"
            await self._save_state(state)
            return state, result
        
        # Check 3: Timeout exceeded?
        elapsed = datetime.utcnow() - state.started_at
        if elapsed.total_seconds() > state.timeout_seconds:
            result.allowed = False
            result.reason = f"Run timeout ({state.timeout_seconds}s)"
            state.status = "killed"
            state.kill_reason = "timeout"
            await self._save_state(state)
            return state, result
        
        # Check 4: Budget exceeded?
        if state.total_cost >= state.max_budget:
            result.allowed = False
            result.reason = f"Budget exceeded (${state.max_budget})"
            state.status = "killed"
            state.kill_reason = "budget_exceeded"
            state.budget_exceeded = True
            await self._save_state(state)
            return state, result
        
        # All checks passed - increment step
        state.step_count += 1
        state.last_activity = datetime.utcnow()
        
        # NOTE: Prompt is NOT added here - it's added in complete_step()
        # This allows loop detection to compare against PREVIOUS prompts only
        
        # Add warnings if approaching limits
        if state.step_count >= state.max_steps * 0.8:
            result.warnings.append(f"Approaching step limit: {state.step_count}/{state.max_steps}")
        
        await self._save_state(state)
        return state, result
    
    async def complete_step(
        self,
        run_id: str,
        tokens: int = 0,
        cost: Decimal = Decimal("0"),
        response: str = "",
        prompt: str = "",
        loop_detected: bool = False,
    ):
        """Update run after step completion"""
        if not self._connected:
            return
        
        key = self._run_key(run_id)
        data = await self._redis.get(key)
        if not data:
            return
        
        state = self._dict_to_state(json.loads(data))
        state.total_tokens += tokens
        state.total_cost += cost
        state.last_activity = datetime.utcnow()
        
        # Store prompt for future loop detection
        if prompt:
            state.recent_prompts.append(prompt[:500])
            state.recent_prompts = state.recent_prompts[-5:]
        
        if response:
            state.recent_responses.append(response[:500])
            state.recent_responses = state.recent_responses[-5:]
        
        if loop_detected:
            state.loop_detected = True
        
        await self._save_state(state)
    
    async def kill_run(self, run_id: str, reason: str):
        """Kill a run (stop all future requests)"""
        if not self._connected:
            return
        
        key = self._run_key(run_id)
        data = await self._redis.get(key)
        if not data:
            return
        
        state = self._dict_to_state(json.loads(data))
        state.status = "killed"
        state.kill_reason = reason
        await self._save_state(state)
        
        logger.warning(f"Run killed: {run_id} - {reason}")
    
    async def get_run_state(self, run_id: str) -> Optional[RunState]:
        """Get current run state"""
        if not self._connected:
            return None
        
        key = self._run_key(run_id)
        data = await self._redis.get(key)
        if not data:
            return None
        
        return self._dict_to_state(json.loads(data))


# Singleton instance
run_tracker = RunTracker()
