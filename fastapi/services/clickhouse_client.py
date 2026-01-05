"""
ClickHouse Async Client
Fire-and-forget logging with batching for <10ms overhead

Design:
- Async inserts (don't block request)
- Batch writes (reduce DB round trips)
- Graceful degradation (if CH down, don't crash proxy)
"""

import asyncio
import json
import logging
from datetime import datetime
from typing import Optional
from dataclasses import dataclass, asdict
from decimal import Decimal

import httpx

from config import settings

logger = logging.getLogger(__name__)


@dataclass
class RequestLog:
    """Single request log entry"""
    run_id: str
    step_number: int
    request_id: str
    team_id: str
    user_id: str
    api_key_id: str
    model: str
    endpoint: str
    prompt_tokens: int = 0
    completion_tokens: int = 0
    total_tokens: int = 0
    cost_usd: Decimal = Decimal("0")
    latency_ms: int = 0
    overhead_ms: int = 0
    ttfb_ms: int = 0
    status_code: int = 200
    error_message: str = ""
    loop_detected: bool = False
    similarity_score: float = 0.0
    dlp_triggered: bool = False
    dlp_action: str = ""
    agent_id: str = ""
    agent_name: str = ""
    request_messages: str = ""  # JSON string
    response_content: str = ""
    ip_address: str = ""
    user_agent: str = ""
    metadata: str = "{}"


@dataclass 
class RunSummary:
    """Run-level summary for tracking"""
    run_id: str
    team_id: str
    user_id: str
    agent_id: str = ""
    started_at: Optional[datetime] = None
    total_steps: int = 0
    total_tokens: int = 0
    total_cost_usd: Decimal = Decimal("0")
    total_latency_ms: int = 0
    status: str = "running"
    kill_reason: str = ""
    loop_detected: bool = False
    dlp_triggered: bool = False
    budget_exceeded: bool = False


class ClickHouseClient:
    """
    Async ClickHouse client with batching
    
    Uses HTTP interface for simplicity and async support
    """
    
    def __init__(self):
        self.base_url = f"http://{settings.CLICKHOUSE_HOST}:8123"
        self.database = settings.CLICKHOUSE_DATABASE
        self.user = settings.CLICKHOUSE_USER
        self.password = settings.CLICKHOUSE_PASSWORD
        
        # Batch queue
        self._log_queue: list[RequestLog] = []
        self._queue_lock = asyncio.Lock()
        self._flush_task: Optional[asyncio.Task] = None
        
        # Health state
        self._healthy = True
        self._last_error: Optional[str] = None
    
    async def start(self):
        """Start background flush task"""
        self._flush_task = asyncio.create_task(self._flush_loop())
        logger.info("ClickHouse client started")
    
    async def stop(self):
        """Stop and flush remaining logs"""
        if self._flush_task:
            self._flush_task.cancel()
            try:
                await self._flush_task
            except asyncio.CancelledError:
                pass
        
        # Final flush
        await self._flush_batch()
        logger.info("ClickHouse client stopped")
    
    async def _flush_loop(self):
        """Background task to flush logs periodically"""
        while True:
            try:
                await asyncio.sleep(settings.LOG_FLUSH_INTERVAL)
                await self._flush_batch()
            except asyncio.CancelledError:
                break
            except Exception as e:
                logger.error(f"Flush loop error: {e}")
    
    async def _flush_batch(self):
        """Flush queued logs to ClickHouse"""
        async with self._queue_lock:
            if not self._log_queue:
                return
            
            batch = self._log_queue.copy()
            self._log_queue.clear()
        
        try:
            await self._insert_logs(batch)
            self._healthy = True
            self._last_error = None
        except Exception as e:
            logger.error(f"Failed to flush {len(batch)} logs: {e}")
            self._healthy = False
            self._last_error = str(e)
            # Re-queue failed logs (with limit to prevent memory issues)
            async with self._queue_lock:
                if len(self._log_queue) < 10000:
                    self._log_queue.extend(batch)

    async def _insert_logs(self, logs: list[RequestLog]):
        """Insert logs to ClickHouse via HTTP interface"""
        if not logs:
            return
        
        # Build INSERT query with JSONEachRow format
        rows = []
        for log in logs:
            row = {
                "run_id": log.run_id,
                "step_number": log.step_number,
                "request_id": log.request_id,
                "team_id": log.team_id,
                "user_id": log.user_id,
                "api_key_id": log.api_key_id,
                "model": log.model,
                "endpoint": log.endpoint,
                "prompt_tokens": log.prompt_tokens,
                "completion_tokens": log.completion_tokens,
                "total_tokens": log.total_tokens,
                "cost_usd": float(log.cost_usd),
                "latency_ms": log.latency_ms,
                "overhead_ms": log.overhead_ms,
                "ttfb_ms": log.ttfb_ms,
                "status_code": log.status_code,
                "error_message": log.error_message,
                "loop_detected": log.loop_detected,
                "similarity_score": log.similarity_score,
                "dlp_triggered": log.dlp_triggered,
                "dlp_action": log.dlp_action,
                "agent_id": log.agent_id,
                "agent_name": log.agent_name,
                "request_messages": log.request_messages,
                "response_content": log.response_content,
                "ip_address": log.ip_address,
                "user_agent": log.user_agent,
                "metadata": log.metadata,
            }
            rows.append(json.dumps(row))
        
        body = "\n".join(rows)
        
        async with httpx.AsyncClient(timeout=10.0) as client:
            response = await client.post(
                self.base_url,
                params={
                    "query": f"INSERT INTO {self.database}.request_logs FORMAT JSONEachRow",
                    "user": self.user,
                    "password": self.password,
                },
                content=body,
                headers={"Content-Type": "application/json"},
            )
            
            if response.status_code != 200:
                raise Exception(f"ClickHouse error: {response.text}")
        
        logger.debug(f"Inserted {len(logs)} logs to ClickHouse")
    
    async def log_request(self, log: RequestLog):
        """Queue a request log (non-blocking)"""
        async with self._queue_lock:
            self._log_queue.append(log)
            
            # Flush immediately if batch is full
            if len(self._log_queue) >= settings.LOG_BATCH_SIZE:
                asyncio.create_task(self._flush_batch())
    
    async def update_run_summary(self, summary: RunSummary):
        """Update run summary (upsert via ReplacingMergeTree)"""
        row = {
            "run_id": summary.run_id,
            "team_id": summary.team_id,
            "user_id": summary.user_id,
            "agent_id": summary.agent_id,
            "started_at": summary.started_at.isoformat() if summary.started_at else datetime.utcnow().isoformat(),
            "total_steps": summary.total_steps,
            "total_tokens": summary.total_tokens,
            "total_cost_usd": float(summary.total_cost_usd),
            "total_latency_ms": summary.total_latency_ms,
            "status": summary.status,
            "kill_reason": summary.kill_reason,
            "loop_detected": summary.loop_detected,
            "dlp_triggered": summary.dlp_triggered,
            "budget_exceeded": summary.budget_exceeded,
        }
        
        try:
            async with httpx.AsyncClient(timeout=5.0) as client:
                response = await client.post(
                    self.base_url,
                    params={
                        "query": f"INSERT INTO {self.database}.run_summary FORMAT JSONEachRow",
                        "user": self.user,
                        "password": self.password,
                    },
                    content=json.dumps(row),
                    headers={"Content-Type": "application/json"},
                )
                
                if response.status_code != 200:
                    logger.error(f"Failed to update run summary: {response.text}")
        except Exception as e:
            logger.error(f"Run summary update error: {e}")
    
    @property
    def is_healthy(self) -> bool:
        return self._healthy
    
    @property
    def last_error(self) -> Optional[str]:
        return self._last_error


# Singleton instance
clickhouse_client = ClickHouseClient()
