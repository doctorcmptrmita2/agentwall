"""
Health check endpoints for monitoring and orchestration

Endpoints:
- /health - Basic health (for load balancers)
- /health/live - Liveness probe (K8s/Easypanel)
- /health/ready - Readiness probe (dependency checks)
- /health/detailed - Full system status (internal)
"""

from fastapi import APIRouter, Response
from datetime import datetime
import asyncio
import logging
import redis.asyncio as redis
import httpx

from config import settings

logger = logging.getLogger(__name__)
router = APIRouter()

# Cache for dependency status (avoid hammering on every request)
_health_cache = {
    "last_check": None,
    "results": {},
    "ttl_seconds": 10
}


@router.get("")
@router.get("/")
async def health_check():
    """
    Basic health check - for load balancers and uptime monitors
    Returns 200 if service is running
    """
    return {
        "status": "healthy",
        "service": "agentwall-proxy",
        "version": settings.APP_VERSION,
        "timestamp": datetime.utcnow().isoformat() + "Z"
    }


@router.get("/live")
async def liveness_check():
    """
    Liveness probe - is the process alive?
    Used by Kubernetes/Easypanel to restart unhealthy containers
    """
    return {"alive": True}


@router.get("/ready")
async def readiness_check(response: Response):
    """
    Readiness probe - can the service handle requests?
    Checks critical dependencies (Redis, ClickHouse)
    """
    checks = await _check_dependencies()
    
    # Service is ready if Redis is available (ClickHouse can be degraded)
    is_ready = checks.get("redis", {}).get("status") == "healthy"
    
    if not is_ready:
        response.status_code = 503
    
    return {
        "ready": is_ready,
        "checks": checks,
        "timestamp": datetime.utcnow().isoformat() + "Z"
    }


@router.get("/detailed")
async def detailed_health():
    """
    Detailed health check - full system status
    For internal monitoring and debugging
    """
    checks = await _check_dependencies(force=True)
    
    return {
        "status": "healthy" if all(
            c.get("status") == "healthy" for c in checks.values()
        ) else "degraded",
        "service": "agentwall-proxy",
        "version": settings.APP_VERSION,
        "environment": "development" if settings.DEBUG else "production",
        "checks": checks,
        "config": {
            "max_steps": settings.MAX_STEPS,
            "dlp_mode": settings.DLP_MODE,
            "dlp_enabled": settings.DLP_ENABLED,
        },
        "timestamp": datetime.utcnow().isoformat() + "Z"
    }


async def _check_dependencies(force: bool = False) -> dict:
    """
    Check all dependencies with caching
    
    Args:
        force: Bypass cache and check now
    """
    global _health_cache
    
    now = datetime.utcnow()
    
    # Return cached results if fresh
    if not force and _health_cache["last_check"]:
        age = (now - _health_cache["last_check"]).total_seconds()
        if age < _health_cache["ttl_seconds"]:
            return _health_cache["results"]
    
    # Run checks in parallel
    results = await asyncio.gather(
        _check_redis(),
        _check_clickhouse(),
        _check_openai(),
        return_exceptions=True
    )
    
    checks = {
        "redis": results[0] if not isinstance(results[0], Exception) else {
            "status": "unhealthy", "error": str(results[0])
        },
        "clickhouse": results[1] if not isinstance(results[1], Exception) else {
            "status": "unhealthy", "error": str(results[1])
        },
        "openai": results[2] if not isinstance(results[2], Exception) else {
            "status": "unhealthy", "error": str(results[2])
        },
    }
    
    # Update cache
    _health_cache["last_check"] = now
    _health_cache["results"] = checks
    
    return checks


async def _check_redis() -> dict:
    """Check Redis connectivity"""
    try:
        client = redis.from_url(
            settings.REDIS_URL,
            socket_connect_timeout=2.0
        )
        await client.ping()
        await client.aclose()
        return {"status": "healthy", "latency_ms": 0}
    except Exception as e:
        logger.warning(f"Redis health check failed: {e}")
        return {"status": "unhealthy", "error": str(e)}


async def _check_clickhouse() -> dict:
    """Check ClickHouse connectivity via HTTP interface"""
    try:
        async with httpx.AsyncClient(timeout=2.0) as client:
            response = await client.get(
                f"http://{settings.CLICKHOUSE_HOST}:8123/ping"
            )
            if response.status_code == 200:
                return {"status": "healthy"}
            return {"status": "unhealthy", "error": f"HTTP {response.status_code}"}
    except Exception as e:
        logger.warning(f"ClickHouse health check failed: {e}")
        return {"status": "unhealthy", "error": str(e)}


async def _check_openai() -> dict:
    """Check OpenAI API key validity (lightweight check)"""
    if not settings.OPENAI_API_KEY or settings.OPENAI_API_KEY.startswith("sk-your"):
        return {"status": "unconfigured", "error": "API key not set"}
    
    # Just verify key format, don't make actual API call
    if settings.OPENAI_API_KEY.startswith("sk-"):
        return {"status": "configured"}
    
    return {"status": "unhealthy", "error": "Invalid API key format"}
