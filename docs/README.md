# AgentWall Documentation

**Guard the Agent, Save the Budget** 🛡️

AgentWall is the world's first "Agent Firewall" for AI Agents. It provides run-level governance, loop detection, budget enforcement, and DLP protection for your AI agents.

## Quick Links

| Section | Description |
|---------|-------------|
| [Getting Started](./guide/getting-started.md) | 5-minute quickstart guide |
| [API Reference](./api/chat-completions.md) | OpenAI-compatible API docs |
| [Concepts](./guide/concepts.md) | Core concepts and architecture |
| [Playground](./playground/examples.md) | Interactive examples |

## Why AgentWall?

### The Problem

AI Agents are powerful but dangerous:
- **Runaway costs**: An agent can spend $50,000 overnight in an infinite loop
- **Data leaks**: Sensitive data (API keys, PII) can leak through prompts
- **No visibility**: You don't know what your agents are doing until it's too late

### The Solution

AgentWall sits between your agents and LLM providers:

```
Your Agent → AgentWall → OpenAI/Anthropic/etc.
                ↓
         Dashboard & Alerts
```

**Key Features:**
- 🔄 **Loop Detection** - Stops infinite loops at the 2nd request
- 💰 **Budget Enforcement** - Per-run, daily, monthly limits
- 🔒 **DLP Protection** - Masks API keys, credit cards, PII
- 📊 **Run Tracking** - See every step of your agent's journey
- ⚡ **<10ms Overhead** - Ultra-low latency proxy

## Quick Example

```python
from openai import OpenAI

# Just change the base_url - that's it!
client = OpenAI(
    base_url="https://api.agentwall.io/v1",
    api_key="aw-your-api-key"
)

response = client.chat.completions.create(
    model="gpt-4",
    messages=[{"role": "user", "content": "Hello!"}],
    extra_body={
        "agentwall_run_id": "my-agent-task-123"  # Track this run
    }
)

# Response includes AgentWall metadata
print(response.agentwall)
# {
#   "run_id": "my-agent-task-123",
#   "step": 1,
#   "cost_usd": 0.0003,
#   "loop_detected": false
# }
```

## Production Ready

AgentWall is battle-tested and production-ready:

| Metric | Value |
|--------|-------|
| Uptime | 99.9% |
| Latency Overhead | <10ms |
| Loop Detection | 100% accuracy |
| DLP Patterns | 15+ types |

## Get Started

1. [Sign up](https://agentwall.io) for an API key
2. Follow the [Getting Started Guide](./guide/getting-started.md)
3. Explore the [API Reference](./api/chat-completions.md)

---

**Need help?** [Contact us](https://agentwall.io/contact) or check our [FAQ](./guide/faq.md)
