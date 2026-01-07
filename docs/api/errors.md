# Error Codes

Complete reference for AgentWall error responses.

## Error Response Format

All errors follow this structure:

```json
{
  "error": {
    "message": "Human-readable error message",
    "type": "error_type",
    "code": "error_code",
    ...additional fields
  }
}
```

## HTTP Status Codes

| Code | Meaning |
|------|---------|
| 400 | Bad Request - Invalid request format |
| 401 | Unauthorized - Invalid or missing API key |
| 403 | Forbidden - API key doesn't have permission |
| 404 | Not Found - Endpoint or resource not found |
| 422 | Validation Error - Request validation failed |
| 429 | Too Many Requests - Rate limit, loop, or budget exceeded |
| 500 | Internal Error - Server error |
| 502 | Bad Gateway - Upstream provider error |
| 503 | Service Unavailable - Service temporarily down |

## AgentWall-Specific Errors

### Loop Detected (429)

Triggered when AgentWall detects a repetitive pattern.

```json
{
  "error": {
    "message": "Loop detected: Exact prompt repetition detected",
    "type": "loop_detected",
    "code": "agentwall_loop",
    "run_id": "abc123",
    "loop_type": "exact_prompt",
    "confidence": 1.0
  }
}
```

**Loop Types:**

| Type | Description |
|------|-------------|
| `exact_prompt` | Same prompt sent twice |
| `similar_prompt` | Very similar prompts (>85% match) |
| `exact_response` | Same response received twice |
| `oscillation` | A→B→A→B pattern detected |
| `normalized_match` | Same prompt after normalization |

**How to Handle:**
- Check your agent logic for infinite loops
- Use different prompts for retries
- Add backoff/jitter to retry logic

### Budget Exceeded (429)

Triggered when spending exceeds configured limits.

```json
{
  "error": {
    "message": "Budget exceeded: Run cost limit ($1.00)",
    "type": "budget_exceeded",
    "code": "agentwall_budget",
    "run_id": "abc123",
    "exceeded_limit": "run",
    "current_cost": 0.70,
    "limit": 1.00
  }
}
```

**Exceeded Limit Types:**

| Type | Description |
|------|-------------|
| `run` | Per-run budget exceeded |
| `daily` | Daily budget exceeded |
| `monthly` | Monthly budget exceeded |

**How to Handle:**
- Increase budget limits in dashboard
- Optimize prompts to reduce token usage
- Use cheaper models for non-critical tasks

### Run Limit Exceeded (429)

Triggered when step count exceeds maximum.

```json
{
  "error": {
    "message": "Step limit exceeded (30 steps)",
    "type": "run_limit_exceeded",
    "code": "agentwall_limit",
    "run_id": "abc123",
    "step": 31
  }
}
```

**How to Handle:**
- Increase max_steps in budget policy
- Break large tasks into multiple runs
- Check for inefficient agent loops

### Run Killed (429)

Triggered when trying to use a killed run.

```json
{
  "error": {
    "message": "Run killed: loop_detected:exact_prompt",
    "type": "run_killed",
    "code": "agentwall_killed",
    "run_id": "abc123",
    "kill_reason": "loop_detected:exact_prompt"
  }
}
```

**How to Handle:**
- Start a new run with a different run_id
- Check dashboard for kill reason
- Fix the underlying issue before retrying

## Authentication Errors

### Invalid API Key (401)

```json
{
  "error": {
    "message": "Invalid API key",
    "type": "authentication_error",
    "code": "invalid_api_key"
  }
}
```

**How to Handle:**
- Verify API key starts with `aw-`
- Check key is active in dashboard
- Ensure no extra whitespace

### Missing API Key (401)

```json
{
  "error": {
    "message": "Missing API key",
    "type": "authentication_error",
    "code": "missing_api_key"
  }
}
```

**How to Handle:**
- Add `Authorization: Bearer aw-xxx` header

## Validation Errors

### Invalid Request (422)

```json
{
  "error": {
    "message": "Invalid request: messages is required",
    "type": "validation_error",
    "code": "invalid_request",
    "details": [
      {
        "field": "messages",
        "message": "Field required"
      }
    ]
  }
}
```

**Common Validation Errors:**

| Field | Error |
|-------|-------|
| `messages` | Required, must be array |
| `model` | Required, must be valid model ID |
| `max_tokens` | Must be positive integer |
| `temperature` | Must be between 0 and 2 |

## Upstream Errors

### Provider Error (502)

```json
{
  "error": {
    "message": "OpenAI API error: Rate limit exceeded",
    "type": "upstream_error",
    "code": "openai_error",
    "upstream_status": 429
  }
}
```

**How to Handle:**
- Retry with exponential backoff
- Check provider status page
- Consider using a different model

## Error Handling Best Practices

### Python

```python
from openai import OpenAI, APIError

client = OpenAI(
    base_url="https://api.agentwall.io/v1",
    api_key="aw-your-key"
)

try:
    response = client.chat.completions.create(
        model="gpt-4",
        messages=[{"role": "user", "content": "Hello"}],
        extra_body={"agentwall_run_id": "task-123"}
    )
except APIError as e:
    if e.status_code == 429:
        error = e.body.get("error", {})
        if error.get("type") == "loop_detected":
            print(f"Loop detected: {error.get('loop_type')}")
            # Start new run or fix agent logic
        elif error.get("type") == "budget_exceeded":
            print(f"Budget exceeded: {error.get('exceeded_limit')}")
            # Increase budget or stop
    else:
        raise
```

### JavaScript

```javascript
import OpenAI from 'openai';

const client = new OpenAI({
  baseURL: 'https://api.agentwall.io/v1',
  apiKey: 'aw-your-key'
});

try {
  const response = await client.chat.completions.create({
    model: 'gpt-4',
    messages: [{ role: 'user', content: 'Hello' }],
    agentwall_run_id: 'task-123'
  });
} catch (error) {
  if (error.status === 429) {
    const errorData = error.error;
    if (errorData.type === 'loop_detected') {
      console.log(`Loop detected: ${errorData.loop_type}`);
    } else if (errorData.type === 'budget_exceeded') {
      console.log(`Budget exceeded: ${errorData.exceeded_limit}`);
    }
  } else {
    throw error;
  }
}
```

---

**Next**: [Playground Examples](../playground/examples.md)
