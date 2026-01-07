# Getting Started

Get AgentWall running in 5 minutes.

## Prerequisites

- An AgentWall API key ([sign up here](https://agentwall.io))
- An OpenAI API key (or other LLM provider)
- Python 3.8+ or Node.js 16+

## Step 1: Get Your API Key

1. Go to [agentwall.io/admin](https://agentwall.io/admin)
2. Create an account or log in
3. Navigate to **API Keys** → **Create New Key**
4. Copy your key (starts with `aw-`)

## Step 2: Configure Your Client

### Python (OpenAI SDK)

```python
from openai import OpenAI

client = OpenAI(
    base_url="https://api.agentwall.io/v1",
    api_key="aw-your-api-key"
)
```

### Node.js (OpenAI SDK)

```javascript
import OpenAI from 'openai';

const client = new OpenAI({
  baseURL: 'https://api.agentwall.io/v1',
  apiKey: 'aw-your-api-key'
});
```

### cURL

```bash
curl https://api.agentwall.io/v1/chat/completions \
  -H "Authorization: Bearer aw-your-api-key" \
  -H "Content-Type: application/json" \
  -d '{
    "model": "gpt-4",
    "messages": [{"role": "user", "content": "Hello!"}]
  }'
```

## Step 3: Make Your First Request

```python
response = client.chat.completions.create(
    model="gpt-4",
    messages=[
        {"role": "user", "content": "What is 2+2?"}
    ]
)

print(response.choices[0].message.content)
# Output: 4
```

That's it! Your request is now protected by AgentWall.

## Step 4: Enable Run Tracking (Recommended)

For multi-step agent tasks, use `agentwall_run_id` to track the entire run:

```python
import uuid

run_id = f"task-{uuid.uuid4().hex[:8]}"

# Step 1
response1 = client.chat.completions.create(
    model="gpt-4",
    messages=[{"role": "user", "content": "Research topic: AI safety"}],
    extra_body={"agentwall_run_id": run_id}
)

# Step 2 (same run_id)
response2 = client.chat.completions.create(
    model="gpt-4",
    messages=[{"role": "user", "content": "Summarize the findings"}],
    extra_body={"agentwall_run_id": run_id}
)

# Check run metadata
print(response2.agentwall)
# {
#   "run_id": "task-abc12345",
#   "step": 2,
#   "total_run_cost": 0.0012,
#   "loop_detected": false
# }
```

## Step 5: View Your Dashboard

Go to [agentwall.io/admin](https://agentwall.io/admin) to see:

- **Agent Runs** - All your agent tasks with step-by-step details
- **Request Logs** - Every API request with costs and latency
- **Budget Usage** - Track spending against your limits
- **Alerts** - Loop detections, budget warnings, kills

## What's Next?

- [Concepts](./concepts.md) - Understand run tracking, loop detection, DLP
- [API Reference](../api/chat-completions.md) - Full API documentation
- [Examples](../playground/examples.md) - Real-world use cases
- [LangChain Integration](./integrations/langchain.md) - Use with LangChain

## Troubleshooting

### "Invalid API Key" (401)

Make sure your API key:
- Starts with `aw-`
- Is copied correctly (no extra spaces)
- Is active in the dashboard

### "Model not found" (404)

Check that:
- You're using a supported model (gpt-4, gpt-3.5-turbo, etc.)
- Your OpenAI API key is configured in AgentWall dashboard

### High Latency

AgentWall adds <10ms overhead. If you see high latency:
- Check your network connection
- The LLM provider (OpenAI) may be slow
- Use streaming for better perceived performance

---

**Need help?** [Contact support](https://agentwall.io/contact)
