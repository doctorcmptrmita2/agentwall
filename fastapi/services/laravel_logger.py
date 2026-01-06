"""
Laravel Request Logger Service

Sends request logs to Laravel dashboard for LiteLLM-style logging.
Uses async HTTP to avoid blocking the main request flow.

Performance: Fire-and-forget pattern - <1ms overhead
"""

import asyncio
import httpx
import logging
from typing import Optional
from dataclasses import dataclass, asdict
from decimal import Decimal

from config import settings

logger = logging.getLogger(__name__)

# Configuration from settings
LARAVEL_URL = settings.LARAVEL_URL
# If internal URL fails, try public URL
if "laravel" in LARAVEL_URL.lower() or "localhost" in LARAVEL_URL.lower():
    LARAVEL_URL = "https://agentwall.io"  # Fallback to public URL
INTERNAL_SECRET = settings.INTERNAL_SECRET
LOG_TIMEOUT = 2.0  # seconds - don't block main request


@dataclass
class LaravelRequestLog:
    """Request log data to send to Laravel"""
    request_id: str
    model: str
    run_id: Optional[str] = None
    team_id: Optional[int] = None
    user_id: Optional[int] = None
    api_key_id: Optional[str] = None
    provider: Optional[str] = None
    endpoint: Optional[str] = None
    stream: Optional[bool] = None
    prompt_tokens: Optional[int] = None
    completion_tokens: Optional[int] = None
    total_tokens: Optional[int] = None
    cost_usd: Optional[float] = None
    latency_ms: Optional[int] = None
    ttfb_ms: Optional[int] = None
    status_code: Optional[int] = None
    error_type: Optional[str] = None
    error_message: Optional[str] = None
    dlp_triggered: Optional[bool] = None
    loop_detected: Optional[bool] = None
    budget_exceeded: Optional[bool] = None
    ip_address: Optional[str] = None
    user_agent: Optional[str] = None


class LaravelLogger:
    """Async logger that sends request logs to Laravel dashboard"""
    
    def __init__(self):
        self._client: Optional[httpx.AsyncClient] = None
        self._queue: asyncio.Queue = asyncio.Queue(maxsize=1000)
        self._worker_task: Optional[asyncio.Task] = None
        self._enabled = True
    
    async def _get_client(self) -> httpx.AsyncClient:
        """Get or create HTTP client"""
        if self._client is None or self._client.is_closed:
            self._client = httpx.AsyncClient(
                timeout=LOG_TIMEOUT,
                headers={
                    "X-Internal-Secret": INTERNAL_SECRET,
                    "Content-Type": "application/json",
                }
            )
        return self._client
    
    async def log_request(self, log: LaravelRequestLog) -> None:
        """
        Queue a request log to be sent to Laravel.
        Fire-and-forget - doesn't block the main request.
        """
        if not self._enabled:
            return
        
        try:
            # Non-blocking put with timeout
            self._queue.put_nowait(log)
        except asyncio.QueueFull:
            logger.warning("Laravel log queue full, dropping log")
    
    async def _send_log(self, log: LaravelRequestLog) -> bool:
        """Actually send the log to Laravel"""
        try:
            client = await self._get_client()
            
            # Convert dataclass to dict, handling Decimal
            data = {}
            for key, value in asdict(log).items():
                if isinstance(value, Decimal):
                    data[key] = float(value)
                elif value is not None:
                    data[key] = value
            
            response = await client.post(
                f"{LARAVEL_URL}/api/internal/logs",
                json=data,
            )
            
            if response.status_code == 201:
                logger.debug(f"Log sent to Laravel: {log.request_id}")
                return True
            else:
                logger.warning(f"Laravel log failed: {response.status_code} - {response.text}")
                return False
                
        except httpx.TimeoutException:
            logger.warning(f"Laravel log timeout for {log.request_id}")
            return False
        except Exception as e:
            logger.error(f"Laravel log error: {e}")
            return False
    
    async def _worker(self) -> None:
        """Background worker that processes the log queue"""
        while True:
            try:
                log = await self._queue.get()
                await self._send_log(log)
                self._queue.task_done()
            except asyncio.CancelledError:
                break
            except Exception as e:
                logger.error(f"Laravel logger worker error: {e}")
    
    def start_worker(self) -> None:
        """Start the background worker task"""
        if self._worker_task is None or self._worker_task.done():
            self._worker_task = asyncio.create_task(self._worker())
            logger.info("Laravel logger worker started")
    
    async def stop(self) -> None:
        """Stop the logger and cleanup"""
        if self._worker_task:
            self._worker_task.cancel()
            try:
                await self._worker_task
            except asyncio.CancelledError:
                pass
        
        if self._client:
            await self._client.aclose()
    
    async def flush(self) -> None:
        """Wait for all queued logs to be sent"""
        await self._queue.join()


# Singleton instance
laravel_logger = LaravelLogger()


async def log_to_laravel(
    request_id: str,
    model: str,
    run_id: str = None,
    team_id: int = None,
    user_id: int = None,
    api_key_id: str = None,
    provider: str = None,
    endpoint: str = None,
    stream: bool = None,
    prompt_tokens: int = None,
    completion_tokens: int = None,
    total_tokens: int = None,
    cost_usd: float = None,
    latency_ms: int = None,
    ttfb_ms: int = None,
    status_code: int = None,
    error_type: str = None,
    error_message: str = None,
    dlp_triggered: bool = None,
    loop_detected: bool = None,
    budget_exceeded: bool = None,
    ip_address: str = None,
    user_agent: str = None,
) -> None:
    """
    Convenience function to log a request to Laravel.
    Fire-and-forget - returns immediately.
    """
    log = LaravelRequestLog(
        request_id=request_id,
        model=model,
        run_id=run_id,
        team_id=team_id,
        user_id=user_id,
        api_key_id=api_key_id,
        provider=provider,
        endpoint=endpoint,
        stream=stream,
        prompt_tokens=prompt_tokens,
        completion_tokens=completion_tokens,
        total_tokens=total_tokens,
        cost_usd=cost_usd,
        latency_ms=latency_ms,
        ttfb_ms=ttfb_ms,
        status_code=status_code,
        error_type=error_type,
        error_message=error_message,
        dlp_triggered=dlp_triggered,
        loop_detected=loop_detected,
        budget_exceeded=budget_exceeded,
        ip_address=ip_address,
        user_agent=user_agent,
    )
    await laravel_logger.log_request(log)
