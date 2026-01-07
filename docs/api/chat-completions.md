# Chat Completions API

OpenAI-compatible chat completions endpoint with AgentWall protection.

## Endpoint

```
POST https://api.agentwall.io/v1/chat/completions
```

## Authentication

Include your AgentWall API key in the Authorization header:

```
Authorization: Bearer aw-your-api-key
```

## Request

### Headers

| Header | Required | Description |
|--------|----------|-------------|
| `Authorization` | Yes | `Bearer aw-your-api-key` |
| `Content-Type` | Yes | `application/json` |
| `X-AgentWall-Run-ID` | No | Run ID for tracking (alternative to body) |

### Body Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `model` | string | Yes | Model ID (e.g., `gpt-4`, `gpt-3.5-turbo`) |
| `messages` | array | Yes | Array of message objects |
| `stream` | boolean | No | Enable streaming (default: false) |
| `max_tokens` | integer | No | Maximum tokens to generate |
| `temperature` | number | No | Sampling temperature (0-2) |
| `agentwall_run_id` | string | No | Run ID for multi-step tracking |
| `agentwall_agent_id` | string | No | Agent identifier |

### Message Object

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `role` | string | Yes | `system`, `user`, or `assistant` |
| `content` | string | Yes | Message content |

## Response

### Success (200)

```json
{
  "id": "chatcmpl-abc123",
  "object": "chat.completion",
  "created": 1704567890,
  "model": "gpt-4",
  "choices": [
    {
      "index": 0,
      "message": {
        "role": "assistant",
        "content": "Hello! How can I help you today?"
      },
      "finish_reason": "stop"
    }
  ],
  "usage": {
    "prompt_tokens": 10,
    "completion_tokens": 15,
    "total_tokens": 25
  },
  "agentwall": {
    "run_id": "abc123-def456",
    "step": 1,
    "cost_usd": 0.000125,
    "total_run_cost": 0.000125,
    "total_run_steps": 1,
    "overhead_ms": 8.5,
    "provider": "openai"
  }
}
```

### AgentWall Metadata

| Field | Type | Description |
|-------|------|-------------|
| `run_id` | string | Unique run identifier |
| `step` | integer | Current step number in this run |
| `cost_usd` | number | Cost of this request in USD |
| `total_run_cost` | number | Total cost of the run so far |
| `total_run_steps` | integer | Total steps in this run |
| `overhead_ms` | number | AgentWall processing time |
| `provider` | string | LLM provider used |
| `warning` | object | Warning if potential loop detected |

## Error Responses

### Loop Detected (429)

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

### Budget Exceeded (429)

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

### Validation Error (422)

```json
{
  "error": {
    "message": "Invalid request: messages is required",
    "type": "validation_error",
    "code": "invalid_request"
  }
}
```

## Examples

### Basic Request

```bash
curl https://api.agentwall.io/v1/chat/completions \
  -H "Authorization: Bearer aw-your-api-key" \
  -H "Content-Type: application/json" \
  -d '{
    "model": "gpt-4",
    "messages": [
      {"role": "user", "content": "Hello!"}
    ]
  }'
```

### With Run Tracking

```bash
curl https://api.agentwall.io/v1/chat/completions \
  -H "Authorization: Bearer aw-your-api-key" \
  -H "Content-Type: application/json" \
  -d '{
    "model": "gpt-4",
    "messages": [
      {"role": "user", "content": "Research AI safety"}
    ],
    "agentwall_run_id": "research-task-001"
  }'
```

### Streaming

```bash
curl https://api.agentwall.io/v1/chat/completions \
  -H "Authorization: Bearer aw-your-api-key" \
  -H "Content-Type: application/json" \
  -d '{
    "model": "gpt-4",
    "messages": [
      {"role": "user", "content": "Write a poem"}
    ],
    "stream": true
  }'
```

### Python Example

```python
from openai import OpenAI

client = OpenAI(
    base_url="https://api.agentwall.io/v1",
    api_key="aw-your-api-key"
)

# Basic request
response = client.chat.completions.create(
    model="gpt-4",
    messages=[
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user", "content": "What is the capital of France?"}
    ]
)

print(response.choices[0].message.content)
# Paris

# With run tracking
response = client.chat.completions.create(
    model="gpt-4",
    messages=[{"role": "user", "content": "Hello"}],
    extra_body={"agentwall_run_id": "my-task-123"}
)

# Access AgentWall metadata
print(response.model_extra.get("agentwall"))
```

### Node.js Example

```javascript
import OpenAI from 'openai';

const client = new OpenAI({
  baseURL: 'https://api.agentwall.io/v1',
  apiKey: 'aw-your-api-key'
});

// Basic request
const response = await client.chat.completions.create({
  model: 'gpt-4',
  messages: [
    { role: 'user', content: 'Hello!' }
  ]
});

console.log(response.choices[0].message.content);

// With run tracking
const response2 = await client.chat.completions.create({
  model: 'gpt-4',
  messages: [{ role: 'user', content: 'Hello!' }],
  agentwall_run_id: 'my-task-123'
});
```

## Response Headers

| Header | Description |
|--------|-------------|
| `X-AgentWall-Run-ID` | Run identifier |
| `X-AgentWall-Step` | Step number |
| `X-AgentWall-Cost` | Request cost in USD |

## Rate Limits

| Plan | Requests/min | Requests/day |
|------|--------------|--------------|
| Free | 10 | 100 |
| Pro | 100 | 10,000 |
| Enterprise | Unlimited | Unlimited |

---

**Next**: [Health API](./health.md)
