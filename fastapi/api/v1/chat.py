"""
OpenAI-compatible chat completions endpoint
Core proxy functionality with agent firewall

Critical Requirements:
- <10ms overhead (non-streaming)
- <1ms overhead per chunk (streaming)
- SSE format must be preserved exactly

Week 2 Features:
- Run-level tracking (MOAT)
- Step counting & limits
- Loop detection
- Cost tracking
"""

from fastapi import APIRouter, HTTPException, Request
from fastapi.responses import StreamingResponse, JSONResponse
import time
import uuid
import json
import asyncio
import logging
from decimal import Decimal

from models.requests import ChatCompletionRequest
from services.openai_proxy import openai_proxy, OpenAIError
from services.multi_provider import multi_provider_proxy, MultiProviderError, detect_provider, resolve_model
from services.run_tracker import run_tracker, RunState
from services.loop_detector import loop_detector
from services.cost_calculator import calculate_cost
from services.clickhouse_client import clickhouse_client, RequestLog
from services.dlp import dlp_engine
from services.laravel_logger import log_to_laravel, laravel_logger
from middleware.budget_enforcer import budget_enforcer, BudgetPolicy

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
    
    AgentWall Features:
    - Run-level tracking (pass agentwall_run_id for multi-step tracking)
    - Step limits (auto-kill runaway agents)
    - Loop detection (detect infinite loops)
    - Cost tracking (per-run budget enforcement)
    """
    start_time = time.perf_counter()
    request_id = str(uuid.uuid4())
    
    # Generate or use provided run_id (check header first, then body)
    # Header takes precedence for SDK compatibility
    run_id = (
        http_request.headers.get("X-AgentWall-Run-ID") or
        http_request.headers.get("x-agentwall-run-id") or
        request.agentwall_run_id or
        str(uuid.uuid4())
    )
    
    # Get step from header if provided
    step_from_header = http_request.headers.get("X-AgentWall-Step") or http_request.headers.get("x-agentwall-step")
    
    agent_id = request.agentwall_agent_id or ""
    
    # Extract user info from auth middleware
    user_id = getattr(http_request.state, "user_id", "anonymous")
    team_id = getattr(http_request.state, "team_id", "default")
    api_key_id = getattr(http_request.state, "api_key_id", "unknown")
    is_passthrough = getattr(http_request.state, "passthrough", False)
    user_limits = getattr(http_request.state, "limits", None)
    
    # For pass-through mode, extract the original API key
    openai_api_key = None
    if is_passthrough:
        auth_header = http_request.headers.get("Authorization", "")
        if auth_header.startswith("Bearer "):
            openai_api_key = auth_header[7:]
    
    # Extract prompt for tracking
    prompt_text = ""
    if request.messages:
        last_user_msg = next(
            (m for m in reversed(request.messages) if m.role == "user"),
            None
        )
        if last_user_msg and last_user_msg.content:
            prompt_text = last_user_msg.content[:500]
    
    # === RUN-LEVEL GOVERNANCE ===
    run_state, step_result = await run_tracker.process_step(
        run_id=run_id,
        team_id=team_id,
        user_id=user_id,
        agent_id=agent_id,
        prompt=prompt_text,
        limits=user_limits,
    )
    
    # Check if step is allowed
    if not step_result.allowed:
        logger.warning(f"Step blocked: {step_result.reason} for run_id={run_id}")
        raise HTTPException(
            status_code=429,
            detail={
                "error": {
                    "message": step_result.reason,
                    "type": "run_limit_exceeded",
                    "code": "agentwall_limit",
                    "run_id": run_id,
                    "step": step_result.step_number,
                }
            }
        )
    
    # === LOOP DETECTION (pre-check) ===
    loop_result = loop_detector.check_loop(
        current_prompt=prompt_text,
        current_response="",  # Pre-check, no response yet
        recent_prompts=run_state.recent_prompts,
        recent_responses=run_state.recent_responses,
    )
    
    if loop_result.is_loop and loop_result.confidence >= 0.95:
        # High confidence loop - block request
        logger.warning(f"Loop blocked: {loop_result.message} for run_id={run_id}")
        await run_tracker.kill_run(run_id, f"loop_detected:{loop_result.loop_type}")
        raise HTTPException(
            status_code=429,
            detail={
                "error": {
                    "message": f"Loop detected: {loop_result.message}",
                    "type": "loop_detected",
                    "code": "agentwall_loop",
                    "run_id": run_id,
                    "loop_type": loop_result.loop_type,
                    "confidence": loop_result.confidence,
                }
            }
        )
    
    logger.info(
        f"Chat request: run_id={run_id}, step={step_result.step_number}, "
        f"user={user_id}, model={request.model}, stream={request.stream}"
    )
    
    # Prepare OpenAI request
    openai_request = request.model_dump(
        exclude={"agentwall_run_id", "agentwall_agent_id", "agentwall_metadata"},
        exclude_none=True
    )
    
    try:
        if request.stream:
            # === STREAMING MODE ===
            return await _handle_streaming(
                openai_request=openai_request,
                run_id=run_id,
                request_id=request_id,
                step_number=step_result.step_number,
                team_id=team_id,
                user_id=user_id,
                api_key_id=api_key_id,
                agent_id=agent_id,
                model=request.model,
                openai_api_key=openai_api_key,
                start_time=start_time,
                prompt_text=prompt_text,
                run_state=run_state,
                loop_warning=loop_result if loop_result.is_loop else None,
                http_request=http_request,
            )
        else:
            # === NON-STREAMING MODE ===
            return await _handle_non_streaming(
                openai_request=openai_request,
                run_id=run_id,
                request_id=request_id,
                step_number=step_result.step_number,
                team_id=team_id,
                user_id=user_id,
                api_key_id=api_key_id,
                agent_id=agent_id,
                model=request.model,
                openai_api_key=openai_api_key,
                start_time=start_time,
                prompt_text=prompt_text,
                run_state=run_state,
                loop_warning=loop_result if loop_result.is_loop else None,
                http_request=http_request,
            )
    
    except (OpenAIError, MultiProviderError) as e:
        # Log error to ClickHouse
        asyncio.create_task(_log_error(
            run_id=run_id,
            request_id=request_id,
            step_number=step_result.step_number,
            team_id=team_id,
            user_id=user_id,
            api_key_id=api_key_id,
            model=request.model,
            error_code=e.status_code,
            error_message=e.message,
            http_request=http_request,
        ))
        
        provider = getattr(e, 'provider', 'openai')
        logger.error(f"{provider} error: {e.status_code} - {e.message}")
        raise HTTPException(
            status_code=e.status_code,
            detail={
                "error": {
                    "message": e.message,
                    "type": "upstream_error",
                    "code": f"{provider}_error"
                }
            }
        )
    
    except HTTPException:
        raise
    
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


async def _handle_non_streaming(
    openai_request: dict,
    run_id: str,
    request_id: str,
    step_number: int,
    team_id: str,
    user_id: str,
    api_key_id: str,
    agent_id: str,
    model: str,
    openai_api_key: str | None,
    start_time: float,
    prompt_text: str,
    run_state: RunState,
    loop_warning,
    http_request: Request,
) -> JSONResponse:
    """Handle non-streaming chat completion"""
    
    # Use multi-provider proxy (supports OpenAI, OpenRouter, etc.)
    response_data = await multi_provider_proxy.chat_completion(
        request_data=openai_request,
        run_id=run_id,
        api_key=openai_api_key,
    )
    
    # Calculate metrics
    overhead_ms = (time.perf_counter() - start_time) * 1000
    usage = response_data.get("usage", {})
    prompt_tokens = usage.get("prompt_tokens", 0)
    completion_tokens = usage.get("completion_tokens", 0)
    total_tokens = usage.get("total_tokens", 0)
    
    # Calculate cost
    cost = calculate_cost(model, prompt_tokens, completion_tokens)
    
    # === BUDGET ENFORCEMENT ===
    # Get daily and monthly spending from run_state
    daily_spent = run_state.daily_cost
    monthly_spent = run_state.monthly_cost
    
    budget_check = budget_enforcer.check_run_budget(
        run_id=run_id,
        current_cost=cost,
        daily_spent=daily_spent,
        monthly_spent=monthly_spent,
    )
    
    if budget_check["should_kill"]:
        logger.warning(
            f"Budget exceeded for run_id={run_id}: {budget_check['reason']}"
        )
        await run_tracker.kill_run(
            run_id,
            f"budget_exceeded:{budget_check['exceeded_limit']}"
        )
        raise HTTPException(
            status_code=429,
            detail={
                "error": {
                    "message": budget_check["reason"],
                    "type": "budget_exceeded",
                    "code": "agentwall_budget",
                    "run_id": run_id,
                    "exceeded_limit": budget_check["exceeded_limit"],
                    "current_cost": budget_check["current_cost"],
                    "limit": budget_check["limit"],
                }
            }
        )
    
    # Extract response content
    response_content = ""
    if response_data.get("choices"):
        message = response_data["choices"][0].get("message", {})
        response_content = message.get("content", "") or ""
        
        # === DLP: Redact sensitive data from response ===
        redacted_content = dlp_engine.redact(response_content)
        if redacted_content != response_content:
            logger.info(f"DLP redacted response content for run_id={run_id}")
            response_data["choices"][0]["message"]["content"] = redacted_content
            response_content = redacted_content[:500]
        else:
            response_content = response_content[:500]
    
    # Post-response loop check
    loop_detected = False
    if response_content:
        post_loop = loop_detector.check_loop(
            current_prompt=prompt_text,
            current_response=response_content,
            recent_prompts=run_state.recent_prompts,
            recent_responses=run_state.recent_responses,
        )
        loop_detected = post_loop.is_loop
    
    # Update run state (fire-and-forget)
    asyncio.create_task(run_tracker.complete_step(
        run_id=run_id,
        tokens=total_tokens,
        cost=cost,
        response=response_content,
        prompt=prompt_text,
        loop_detected=loop_detected,
    ))
    
    # Log to ClickHouse (fire-and-forget)
    asyncio.create_task(clickhouse_client.log_request(RequestLog(
        run_id=run_id,
        step_number=step_number,
        request_id=request_id,
        team_id=team_id,
        user_id=user_id,
        api_key_id=api_key_id,
        model=model,
        endpoint="/v1/chat/completions",
        prompt_tokens=prompt_tokens,
        completion_tokens=completion_tokens,
        total_tokens=total_tokens,
        cost_usd=cost,
        latency_ms=int(overhead_ms),
        overhead_ms=int(overhead_ms),
        status_code=200,
        loop_detected=loop_detected,
        agent_id=agent_id,
        request_messages=json.dumps(openai_request.get("messages", []))[:1000],
        response_content=response_content,
        ip_address=http_request.client.host if http_request.client else "",
        user_agent=http_request.headers.get("user-agent", "")[:200],
    )))
    
    # Warn if overhead exceeds target
    if overhead_ms > 10:
        logger.warning(f"High overhead: {overhead_ms:.2f}ms for run_id={run_id}")
    
    # Add AgentWall metadata to response
    provider = response_data.pop("_agentwall_provider", "openai")
    
    # Log to Laravel Dashboard (fire-and-forget, <1ms overhead)
    asyncio.create_task(log_to_laravel(
        request_id=request_id,
        model=model,
        run_id=run_id,
        provider=provider,
        endpoint="/v1/chat/completions",
        stream=False,
        prompt_tokens=prompt_tokens,
        completion_tokens=completion_tokens,
        total_tokens=total_tokens,
        cost_usd=float(cost),
        latency_ms=int(overhead_ms),
        status_code=200,
        loop_detected=loop_detected,
        ip_address=http_request.client.host if http_request.client else None,
        user_agent=http_request.headers.get("user-agent", "")[:255] or None,
    ))
    
    response_data["agentwall"] = {
        "run_id": run_id,
        "step": step_number,
        "overhead_ms": round(overhead_ms, 2),
        "cost_usd": float(cost),
        "total_run_cost": float(run_state.total_cost + cost),
        "total_run_steps": run_state.step_count,
        "provider": provider,
    }
    
    # Add warnings if any
    if loop_warning:
        response_data["agentwall"]["warning"] = {
            "type": "potential_loop",
            "message": loop_warning.message,
            "confidence": loop_warning.confidence,
        }
    
    return JSONResponse(
        content=response_data,
        headers={
            "X-AgentWall-Run-ID": run_id,
            "X-AgentWall-Step": str(step_number),
            "X-AgentWall-Cost": str(float(cost)),
        }
    )


async def _handle_streaming(
    openai_request: dict,
    run_id: str,
    request_id: str,
    step_number: int,
    team_id: str,
    user_id: str,
    api_key_id: str,
    agent_id: str,
    model: str,
    openai_api_key: str | None,
    start_time: float,
    prompt_text: str,
    run_state: RunState,
    loop_warning,
    http_request: Request,
) -> StreamingResponse:
    """Handle streaming chat completion"""
    
    # Use multi-provider proxy (supports OpenAI, OpenRouter, etc.)
    stream_generator, metrics = await multi_provider_proxy.chat_completion_stream(
        request_data=openai_request,
        run_id=run_id,
        api_key=openai_api_key,
    )
    
    async def wrapped_generator():
        """Wrap generator to capture metrics after completion"""
        response_content = ""
        
        async for chunk in stream_generator:
            yield chunk
            
            # Try to extract content from chunk for logging
            try:
                chunk_str = chunk.decode() if isinstance(chunk, bytes) else chunk
                if chunk_str.startswith("data: ") and not chunk_str.strip().endswith("[DONE]"):
                    data = json.loads(chunk_str[6:])
                    if "choices" in data and data["choices"]:
                        delta = data["choices"][0].get("delta", {})
                        content = delta.get("content", "")
                        if content:
                            response_content += content
            except:
                pass
        
        # After stream completes, log metrics
        overhead_ms = (time.perf_counter() - start_time) * 1000
        
        # Estimate tokens for streaming (actual usage not always available)
        estimated_completion_tokens = len(response_content.split()) * 1.3
        cost = calculate_cost(model, 0, int(estimated_completion_tokens))
        
        # Update run state
        asyncio.create_task(run_tracker.complete_step(
            run_id=run_id,
            tokens=int(estimated_completion_tokens),
            cost=cost,
            response=response_content[:500],
            prompt=prompt_text,
            loop_detected=False,
        ))
        
        # Log to ClickHouse
        asyncio.create_task(clickhouse_client.log_request(RequestLog(
            run_id=run_id,
            step_number=step_number,
            request_id=request_id,
            team_id=team_id,
            user_id=user_id,
            api_key_id=api_key_id,
            model=model,
            endpoint="/v1/chat/completions",
            completion_tokens=int(estimated_completion_tokens),
            cost_usd=cost,
            latency_ms=int(overhead_ms),
            ttfb_ms=int(metrics.first_chunk_ms) if metrics.first_chunk_ms else 0,
            status_code=200,
            agent_id=agent_id,
            response_content=response_content[:500],
            ip_address=http_request.client.host if http_request.client else "",
            user_agent=http_request.headers.get("user-agent", "")[:200],
        )))
        
        # Log to Laravel Dashboard (fire-and-forget)
        asyncio.create_task(log_to_laravel(
            request_id=request_id,
            model=model,
            run_id=run_id,
            endpoint="/v1/chat/completions",
            stream=True,
            completion_tokens=int(estimated_completion_tokens),
            cost_usd=float(cost),
            latency_ms=int(overhead_ms),
            ttfb_ms=int(metrics.first_chunk_ms) if metrics.first_chunk_ms else None,
            status_code=200,
            ip_address=http_request.client.host if http_request.client else None,
            user_agent=http_request.headers.get("user-agent", "")[:255] or None,
        ))
    
    return StreamingResponse(
        wrapped_generator(),
        media_type="text/event-stream",
        headers={
            "Cache-Control": "no-cache",
            "Connection": "keep-alive",
            "X-Accel-Buffering": "no",
            "X-AgentWall-Run-ID": run_id,
            "X-AgentWall-Step": str(step_number),
        }
    )


async def _log_error(
    run_id: str,
    request_id: str,
    step_number: int,
    team_id: str,
    user_id: str,
    api_key_id: str,
    model: str,
    error_code: int,
    error_message: str,
    http_request: Request,
):
    """Log error to ClickHouse"""
    await clickhouse_client.log_request(RequestLog(
        run_id=run_id,
        step_number=step_number,
        request_id=request_id,
        team_id=team_id,
        user_id=user_id,
        api_key_id=api_key_id,
        model=model,
        endpoint="/v1/chat/completions",
        status_code=error_code,
        error_message=error_message[:500],
        ip_address=http_request.client.host if http_request.client else "",
        user_agent=http_request.headers.get("user-agent", "")[:200],
    ))
