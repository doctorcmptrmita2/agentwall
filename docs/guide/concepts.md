# Core Concepts

Understanding AgentWall's key features and how they protect your AI agents.

## Run-Level Tracking

### What is a Run?

A **run** is a complete agent task, which may involve multiple LLM requests.

```
Traditional API Gateway:
  Request 1 → Response 1
  Request 2 → Response 2  (no connection)
  Request 3 → Response 3  (no connection)

AgentWall:
  Run "task-123":
    Step 1 → Response 1
    Step 2 → Response 2  ← Same run!
    Step 3 → Response 3  ← Same run!
```

### Why It Matters

- **Budget per task**: Limit spending per agent task, not just per API key
- **Loop detection**: Detect when an agent is stuck across multiple requests
- **Debugging**: See the full journey of an agent task

### How to Use

Pass `agentwall_run_id` in your requests:

```python
# All requests with same run_id are tracked together
response = client.chat.completions.create(
    model="gpt-4",
    messages=[...],
    extra_body={"agentwall_run_id": "my-task-123"}
)
```

## Loop Detection

### The Problem

AI agents can get stuck in infinite loops:

```
Agent: "Search for weather"
Tool: Error - API unavailable
Agent: "Search for weather"  ← Retry
Tool: Error - API unavailable
Agent: "Search for weather"  ← Infinite loop!
...
```

This can cost thousands of dollars before anyone notices.

### How AgentWall Detects Loops

AgentWall detects three types of loops:

| Type | Description | Detection |
|------|-------------|-----------|
| **Exact** | Same prompt repeated | 2nd occurrence |
| **Similar** | Nearly identical prompts | Jaccard similarity >85% |
| **Oscillation** | A→B→A→B pattern | 4th occurrence |

### What Happens When a Loop is Detected

1. Request is blocked (HTTP 429)
2. Run is killed (no more requests allowed)
3. Alert sent to Slack (if configured)
4. Logged in dashboard

### Example Response

```json
{
  "error": {
    "message": "Loop detected: Exact prompt repetition detected",
    "type": "loop_detected",
    "code": "agentwall_loop",
    "run_id": "task-123",
    "loop_type": "exact_prompt",
    "confidence": 1.0
  }
}
```

## Budget Enforcement

### Three Levels of Budget

| Level | Scope | Use Case |
|-------|-------|----------|
| **Per-Run** | Single agent task | "This task can't cost more than $1" |
| **Daily** | All requests today | "Don't spend more than $100/day" |
| **Monthly** | All requests this month | "Monthly budget is $1000" |

### How It Works

```python
# Set budget in dashboard or via API
# Budget Policy:
#   - max_run_cost: $1.00
#   - daily_limit: $100.00
#   - monthly_limit: $1000.00

# Request 1: $0.30 ✅
# Request 2: $0.40 ✅
# Request 3: $0.50 ❌ Blocked! (would exceed $1 run limit)
```

### Budget Exceeded Response

```json
{
  "error": {
    "message": "Budget exceeded: Run cost limit ($1.00)",
    "type": "budget_exceeded",
    "code": "agentwall_budget",
    "run_id": "task-123",
    "exceeded_limit": "run",
    "current_cost": 0.70,
    "limit": 1.00
  }
}
```

## DLP (Data Loss Prevention)

### What is DLP?

DLP scans requests and responses for sensitive data and masks it automatically.

### Detected Patterns

| Category | Examples |
|----------|----------|
| **API Keys** | OpenAI, AWS, Stripe, GitHub, Slack |
| **Credentials** | Passwords, tokens, secrets |
| **Financial** | Credit cards (Visa, MC, Amex), IBANs |
| **PII** | Emails, phone numbers, SSNs |
| **Infrastructure** | Private IPs, internal URLs |

### How It Works

```
Input:  "My API key is sk-1234567890abcdef"
Output: "My API key is [REDACTED:OPENAI_KEY]"
```

### Configuration

DLP is enabled by default. You can configure sensitivity in the dashboard:

- **Strict**: Block requests with sensitive data
- **Redact**: Mask sensitive data and continue (default)
- **Log Only**: Log but don't modify

## Kill Switch

### Manual Kill

Stop a runaway agent immediately from the dashboard:

1. Go to **Agent Runs**
2. Find the run
3. Click **Kill Run**

All future requests with that `run_id` will be blocked.

### Automatic Kill

AgentWall automatically kills runs when:

- Loop detected
- Budget exceeded
- Step limit reached (default: 30 steps)
- Timeout exceeded (default: 120 seconds)

## Cost Tracking

### Per-Request Cost

Every response includes cost information:

```json
{
  "agentwall": {
    "cost_usd": 0.000123,
    "total_run_cost": 0.00456
  }
}
```

### Supported Models

| Model | Input (per 1K) | Output (per 1K) |
|-------|----------------|-----------------|
| gpt-4 | $0.03 | $0.06 |
| gpt-4-turbo | $0.01 | $0.03 |
| gpt-3.5-turbo | $0.0005 | $0.0015 |
| claude-3-opus | $0.015 | $0.075 |
| claude-3-sonnet | $0.003 | $0.015 |

## Architecture

```
┌─────────────┐     ┌─────────────┐     ┌─────────────┐
│   Your App  │────▶│  AgentWall  │────▶│   OpenAI    │
│   (Agent)   │◀────│   (Proxy)   │◀────│  Anthropic  │
└─────────────┘     └─────────────┘     └─────────────┘
                           │
                           ▼
                    ┌─────────────┐
                    │  Dashboard  │
                    │   Alerts    │
                    │   Logs      │
                    └─────────────┘
```

### Components

- **FastAPI Proxy**: Ultra-low latency (<10ms overhead)
- **Redis**: Run state and loop detection
- **ClickHouse**: High-performance logging
- **Laravel Dashboard**: Admin panel and alerts

---

**Next**: [API Reference](../api/chat-completions.md)
