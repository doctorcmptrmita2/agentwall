"""
Authentication middleware
Validates API keys and attaches user/team info to request
"""

from fastapi import Request, HTTPException
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.responses import Response
import logging

from config import settings

logger = logging.getLogger(__name__)


class AuthMiddleware(BaseHTTPMiddleware):
    """
    API key authentication middleware
    
    Validates API key from:
    1. Authorization: Bearer <key>
    2. X-API-Key: <key>
    3. Query param: ?api_key=<key>
    """
    
    # Paths that don't require authentication
    PUBLIC_PATHS = {"/", "/health", "/health/", "/health/ready", "/health/live", "/docs", "/redoc", "/openapi.json"}
    
    async def dispatch(self, request: Request, call_next):
        # Skip auth for public paths
        if request.url.path in self.PUBLIC_PATHS:
            return await call_next(request)
        
        # Extract API key
        api_key = self._extract_api_key(request)
        
        if not api_key:
            logger.warning(f"Missing API key: {request.url.path}")
            return Response(
                content='{"error": {"message": "Missing API key", "type": "invalid_request_error"}}',
                status_code=401,
                media_type="application/json"
            )
        
        # Validate API key
        user_info = await self._validate_api_key(api_key)
        
        if not user_info:
            logger.warning(f"Invalid API key: {api_key[:10]}...")
            return Response(
                content='{"error": {"message": "Invalid API key", "type": "invalid_request_error"}}',
                status_code=401,
                media_type="application/json"
            )
        
        # Attach user info to request state
        request.state.user_id = user_info["user_id"]
        request.state.team_id = user_info["team_id"]
        request.state.api_key_id = user_info["api_key_id"]
        
        logger.debug(
            f"Authenticated: user_id={user_info['user_id']}, "
            f"team_id={user_info['team_id']}"
        )
        
        return await call_next(request)
    
    def _extract_api_key(self, request: Request) -> str | None:
        """Extract API key from request"""
        
        # 1. Authorization header (Bearer token)
        auth_header = request.headers.get("Authorization", "")
        if auth_header.startswith("Bearer "):
            return auth_header[7:]
        
        # 2. X-API-Key header
        api_key_header = request.headers.get("X-API-Key")
        if api_key_header:
            return api_key_header
        
        # 3. Query parameter
        api_key_query = request.query_params.get("api_key")
        if api_key_query:
            return api_key_query
        
        return None
    
    async def _validate_api_key(self, api_key: str) -> dict | None:
        """
        Validate API key against Laravel backend
        
        Returns user info if valid, None if invalid
        """
        
        # TODO: Implement Redis cache (avoid hitting Laravel every time)
        # cached = await redis_client.get(f"api_key:{api_key}")
        # if cached:
        #     return json.loads(cached)
        
        # TODO: Call Laravel API to validate
        # response = await http_client.post(
        #     f"{settings.LARAVEL_URL}/api/internal/validate-key",
        #     json={"api_key": api_key},
        #     headers={"X-Internal-Secret": settings.INTERNAL_SECRET}
        # )
        # 
        # if response.status_code == 200:
        #     user_info = response.json()
        #     # Cache for 5 minutes
        #     await redis_client.setex(f"api_key:{api_key}", 300, json.dumps(user_info))
        #     return user_info
        # 
        # return None
        
        # TEMPORARY: Mock validation for development
        if settings.DEBUG:
            return {
                "user_id": "dev-user-1",
                "team_id": "dev-team-1",
                "api_key_id": "dev-key-1",
                "limits": {
                    "max_steps": 30,
                    "daily_budget": 10.0,
                }
            }
        
        return None
