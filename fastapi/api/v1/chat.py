"""
OpenAI-compatible chat completions endpoint
Core proxy functionality with agent firewall

Critical Requirements:
- <10ms overhead (non-streaming)
- <1ms overhead per chunk (streaming)
- SSE format must be preserved exactly
"""

from fastapi import APIRouter, HTTPException, Request
from fastapi.responses import StreamingResponse, JSONResponse
import time
import uuid
import logging

from models.requests import ChatCompletionRequest
from services.openai_proxy import openai_proxy, OpenAIError

logger = logging.getLogger(__name__)

router = APIRouter()


@router.post("/chat/completions")
async def chat_completions(
    request: ChatCompletionRequest,
    http_request: Request
):
    """
    OpenAI-compatible chat completions endpoint
    
    Drop-in replacement: Just change base_url to AgentWall
    
    Example:
        client = OpenAI(base_url="https://api.agentwall.io/v1")
    """
    start_time = time.perf_counter()
    
    # Generate run_id (for tracking across steps)
    run_id = request.agentwall_run_id or str(uuid.uuid4())
    
    # Extract user info from auth middleware
    user_id = getattr(http_request.state, "user_id", "anonymous")
    team_id = getattr(http_request.state, "team_id", "default")
    api_key = getattr(http_request.state, "api_key", None)
    
    logger.info(
        f"Chat request: run_id={run_id}, "
        f"user={user_id}, model={request.model}, "
        f"stream={request.stream}"
    )
    
    # Prepare OpenAI request (exclude AgentWall-specific fields)
    openai_request = request.model_dump(
        exclude={"agentwall_run_id", "agentwall_agent_id", "agentwall_metadata"},
        exclude_none=True
    )
    
    try:
        if request.stream:
            # === STREAMING MODE ===
            stream_generator, metrics = await openai_proxy.chat_completion_stream(
                request_data=openai_request,
                run_id=run_id,
                api_key=api_key
            )
            
            return StreamingResponse(
                stream_generator,
                media_type="text/event-stream",
                headers={
                    "Cache-Control": "no-cache",
                    "Connection": "keep-alive",
                    "X-Accel-Buffering": "no",  # Disable nginx buffering
                    "X-AgentWall-Run-ID": run_id,
                }
            )
        
        else:
            # === NON-STREAMING MODE ===
            response_data = await openai_proxy.chat_completion(
                request_data=openai_request,
                run_id=run_id,
                api_key=api_key
            )
            
            # Calculate overhead
            overhead_ms = (time.perf_counter() - start_time) * 1000
            
            # Warn if overhead exceeds target
            if overhead_ms > 10:
                logger.warning(f"High overhead: {overhead_ms:.2f}ms for run_id={run_id}")
            
            # Add AgentWall metadata to response
            response_data["agentwall"] = {
                "run_id": run_id,
                "overhead_ms": round(overhead_ms, 2),
            }
            
            return JSONResponse(
                content=response_data,
                headers={"X-AgentWall-Run-ID": run_id}
            )
    
    except OpenAIError as e:
        logger.error(f"OpenAI error: {e.status_code} - {e.message}")
        raise HTTPException(
            status_code=e.status_code,
            detail={
                "error": {
                    "message": e.message,
                    "type": "upstream_error",
                    "code": "openai_error"
                }
            }
        )
    
    except Exception as e:
        logger.error(f"Unexpected error: {e}", exc_info=True)
        raise HTTPException(
            status_code=500,
            detail={
                "error": {
                    "message": "Internal server error",
                    "type": "internal_error",
                    "code": "internal_error"
                }
            }
        )
