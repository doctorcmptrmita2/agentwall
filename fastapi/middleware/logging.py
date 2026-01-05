"""
Logging middleware
Captures request/response for observability
"""

from fastapi import Request
from starlette.middleware.base import BaseHTTPMiddleware
import time
import logging

logger = logging.getLogger(__name__)


class LoggingMiddleware(BaseHTTPMiddleware):
    """
    Request/response logging middleware
    
    Logs:
    - Request method, path, headers
    - Response status, headers
    - Processing time
    - User/team info (if authenticated)
    """
    
    async def dispatch(self, request: Request, call_next):
        # Start timer
        start_time = time.perf_counter()
        
        # Log request
        logger.info(
            f"→ {request.method} {request.url.path} "
            f"from {request.client.host if request.client else 'unknown'}"
        )
        
        # Process request
        response = await call_next(request)
        
        # Calculate processing time
        process_time = (time.perf_counter() - start_time) * 1000  # ms
        
        # Extract user info (if authenticated)
        user_id = getattr(request.state, "user_id", "anonymous")
        team_id = getattr(request.state, "team_id", "unknown")
        
        # Log response
        logger.info(
            f"← {response.status_code} {request.method} {request.url.path} "
            f"[{process_time:.2f}ms] "
            f"user={user_id} team={team_id}"
        )
        
        # TODO: Async write to ClickHouse
        # asyncio.create_task(
        #     log_writer.write({
        #         "timestamp": datetime.utcnow(),
        #         "method": request.method,
        #         "path": request.url.path,
        #         "status_code": response.status_code,
        #         "process_time_ms": process_time,
        #         "user_id": user_id,
        #         "team_id": team_id,
        #     })
        # )
        
        return response
