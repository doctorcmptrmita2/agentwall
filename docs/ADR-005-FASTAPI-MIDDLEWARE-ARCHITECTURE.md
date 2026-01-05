# ADR-005: FastAPI Middleware Architecture for Streaming Support

**Date:** 5 Ocak 2026  
**Status:** APPROVED  
**Decision Maker:** CTO & Lead Architect

---

## Context

AgentGuard must intercept OpenAI API calls without breaking streaming responses (SSE - Server-Sent Events). Streaming is critical for real-time agent interactions.

**Requirements:**
1. Drop-in replacement (change base_url, works immediately)
2. Support streaming (`stream=true`)
3. <10ms overhead (non-streaming)
4. Don't buffer entire response (memory efficient)
5. Apply DLP/loop detection on-the-fly

**Challenge:** Traditional middleware buffers entire response, breaking streaming.

---

## Decision

**Use ASGI Middleware with StreamingResponse passthrough.**

### Architecture

```
Client Request
    ↓
FastAPI Endpoint (/v1/chat/completions)
    ↓
Authentication Middleware (API key check)
    ↓
DLP Middleware (scan request)
    ↓
Loop Detection Middleware (check run state)
    ↓
Proxy to OpenAI (httpx.AsyncClient)
    ↓
StreamingResponse (if stream=true)
    ↓
DLP Middleware (scan response chunks)
    ↓
Logging Middleware (async write to ClickHouse)
    ↓
Client Response
```

### Key Pattern: Streaming Interceptor

```python
async def stream_with_interception(
    upstream_stream: AsyncIterator[bytes],
    run_id: str
) -> AsyncIterator[bytes]:
    """
    Intercept streaming response without buffering
    """
    async for chunk in upstream_stream:
        # 1. DLP scan (on-the-fly)
        is_sensitive, redacted_chunk = await dlp_engine.scan_chunk(chunk)
        
        # 2. Log chunk (async, non-blocking)
        asyncio.create_task(log_writer.write_chunk(run_id, chunk))
        
        # 3. Yield (don't buffer)
        yield redacted_chunk if is_sensitive else chunk
```

**Why this works:**
- No buffering (memory efficient)
- DLP applied per-chunk (real-time)
- Logging async (doesn't block stream)
- <1ms overhead per chunk

---

## Rationale

### Alternative 1: Buffer entire response ❌

**Pros:**
- Simple implementation
- Easy to apply DLP

**Cons:**
- Breaks streaming (client waits for entire response)
- High memory usage (large responses)
- High latency (defeats purpose of streaming)

**Verdict:** REJECTED

### Alternative 2: Proxy without interception ❌

**Pros:**
- Zero overhead
- Streaming works perfectly

**Cons:**
- No DLP (security risk)
- No logging (no observability)
- No loop detection (core feature missing)

**Verdict:** REJECTED

### Alternative 3: Streaming Interceptor ✅ (CHOSEN)

**Pros:**
- Streaming works (SSE preserved)
- DLP applied (per-chunk)
- Low overhead (<1ms per chunk)
- Memory efficient (no buffering)

**Cons:**
- More complex implementation
- Chunk-level DLP (may miss cross-chunk patterns)

**Verdict:** ACCEPTED

**Mitigation for cross-chunk patterns:**
- Keep sliding window (last 2 chunks)
- Detect patterns across boundaries
- Acceptable trade-off for streaming support

---

## Consequences

### Positive

✅ Streaming support (SSE works)  
✅ Real-time DLP (per-chunk)  
✅ Low memory usage (no buffering)  
✅ <10ms overhead (target met)

### Negative

⚠️ Complex implementation (streaming interceptor)  
⚠️ Cross-chunk pattern detection harder  
⚠️ More testing required (streaming edge cases)

### Mitigation

- Comprehensive streaming tests
- Sliding window for cross-chunk patterns
- Fallback to buffering (if pattern detected mid-stream)

---

## Implementation Plan

### Phase 1: Basic Proxy (Non-Streaming)

```python
@app.post("/v1/chat/completions")
async def chat_completions(request: ChatCompletionRequest):
    # 1. Auth
    user = await auth_middleware.verify(request.api_key)
    
    # 2. DLP scan request
    is_sensitive, redacted_request = await dlp_engine.scan(request.messages)
    if is_sensitive and dlp_mode == "block":
        raise HTTPException(403, "Sensitive data detected")
    
    # 3. Proxy to OpenAI
    response = await openai_client.post(
        "/v1/chat/completions",
        json=redacted_request.dict()
    )
    
    # 4. Log (async)
    asyncio.create_task(log_writer.write(run_id, request, response))
    
    return response.json()
```

### Phase 2: Streaming Support

```python
@app.post("/v1/chat/completions")
async def chat_completions(request: ChatCompletionRequest):
    # ... (auth, DLP scan request)
    
    if request.stream:
        # Streaming mode
        upstream = await openai_client.stream(
            "/v1/chat/completions",
            json=request.dict()
        )
        
        return StreamingResponse(
            stream_with_interception(upstream, run_id),
            media_type="text/event-stream"
        )
    else:
        # Non-streaming mode (Phase 1)
        # ...
```

### Phase 3: Loop Detection Integration

```python
async def stream_with_interception(
    upstream_stream: AsyncIterator[bytes],
    run_id: str
) -> AsyncIterator[bytes]:
    
    accumulated_text = ""
    
    async for chunk in upstream_stream:
        # Parse SSE chunk
        delta = parse_sse_chunk(chunk)
        accumulated_text += delta.content
        
        # Loop detection (every N chunks)
        if len(accumulated_text) > 500:  # Check every 500 chars
            should_continue = await loop_detector.check(run_id, accumulated_text)
            if not should_continue:
                # Kill stream
                yield create_sse_error("Loop detected, stream terminated")
                break
        
        # DLP + yield
        is_sensitive, redacted_chunk = await dlp_engine.scan_chunk(chunk)
        yield redacted_chunk if is_sensitive else chunk
```

---

## Testing Strategy

### Unit Tests

- ✅ Non-streaming proxy
- ✅ Streaming proxy (SSE format)
- ✅ DLP per-chunk
- ✅ Loop detection mid-stream
- ✅ Error handling (upstream failure)

### Integration Tests

- ✅ OpenAI streaming (real API)
- ✅ Large responses (>10MB)
- ✅ Slow streams (timeout handling)
- ✅ Concurrent streams (100+ simultaneous)

### Performance Tests

- ✅ Overhead <10ms (non-streaming)
- ✅ Overhead <1ms per chunk (streaming)
- ✅ Memory usage <100MB (10 concurrent streams)

---

## Success Metrics

- ✅ Streaming works (SSE format preserved)
- ✅ <10ms overhead (non-streaming)
- ✅ <1ms per chunk (streaming)
- ✅ DLP applied (real-time)
- ✅ Loop detection works (mid-stream kill)

---

**Status:** APPROVED - Ready for Implementation  
**Next:** Create FastAPI project skeleton
