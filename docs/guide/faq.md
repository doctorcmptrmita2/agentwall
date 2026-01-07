# Frequently Asked Questions

## General

### What is AgentWall?

AgentWall is an "Agent Firewall" - a proxy that sits between your AI agents and LLM providers (OpenAI, Anthropic, etc.). It provides:

- **Loop Detection**: Stops infinite loops automatically
- **Budget Enforcement**: Per-run, daily, monthly limits
- **DLP Protection**: Masks sensitive data
- **Run Tracking**: See every step of your agent's journey

### How is AgentWall different from LiteLLM/Portkey?

| Feature | LiteLLM/Portkey | AgentWall |
|---------|-----------------|-----------|
| API Proxy | ✅ | ✅ |
| Multi-provider | ✅ | ✅ |
| **Run-level tracking** | ❌ | ✅ |
| **Loop detection** | ❌ | ✅ |
| **Per-run budgets** | ❌ | ✅ |
| **Kill switch** | ❌ | ✅ |

AgentWall tracks entire agent tasks (runs), not just individual requests.

### What's the latency overhead?

Less than 10ms for non-streaming requests. Streaming adds <1ms per chunk.

### Which LLM providers are supported?

- OpenAI (GPT-4, GPT-3.5, etc.)
- OpenRouter (100+ models)
- Anthropic (coming soon)
- Google (coming soon)

## Setup

### How do I get an API key?

1. Go to [agentwall.io/admin](https://agentwall.io/admin)
2. Create an account
3. Navigate to **API Keys** → **Create New Key**
4. Copy your key (starts with `aw-`)

### Do I need to change my code?

Minimal changes! Just update `base_url`:

```python
# Before
client = OpenAI(api_key="sk-...")

# After
client = OpenAI(
    base_url="https://api.agentwall.io/v1",
    api_key="aw-..."
)
```

### Can I use my own OpenAI key?

Yes! Configure your OpenAI key in the AgentWall dashboard, or use pass-through mode.

## Loop Detection

### How does loop detection work?

AgentWall tracks prompts within a run and detects:

1. **Exact repetition**: Same prompt sent twice
2. **Similar prompts**: >85% similarity (Jaccard)
3. **Oscillation**: A→B→A→B pattern

### When is a loop blocked?

By default, loops are blocked at:
- 2nd exact repetition
- 3rd similar prompt
- 4th oscillation step

### Can I disable loop detection?

Yes, in the dashboard under **Settings** → **Loop Detection**.

### What if I legitimately need to send the same prompt?

Use different `run_id` values for independent tasks:

```python
# Task 1
response1 = client.chat.completions.create(
    ...,
    extra_body={"agentwall_run_id": "task-001"}
)

# Task 2 (same prompt is OK - different run)
response2 = client.chat.completions.create(
    ...,
    extra_body={"agentwall_run_id": "task-002"}
)
```

## Budget & Costs

### How is cost calculated?

Based on token usage and model pricing:

| Model | Input (per 1K) | Output (per 1K) |
|-------|----------------|-----------------|
| gpt-4 | $0.03 | $0.06 |
| gpt-4-turbo | $0.01 | $0.03 |
| gpt-3.5-turbo | $0.0005 | $0.0015 |

### What happens when budget is exceeded?

The request is blocked with HTTP 429 and error type `budget_exceeded`. The run is killed.

### Can I set different budgets for different agents?

Yes! Create multiple API keys with different budget policies.

## DLP & Security

### What data is detected?

- API keys (OpenAI, AWS, Stripe, GitHub, etc.)
- Credit card numbers
- Email addresses
- Phone numbers
- SSNs
- Private IPs
- JWTs

### Is my data logged?

By default, prompts and responses are logged for debugging. You can:
- Enable "zero retention" mode
- Self-host AgentWall
- Use shadow logging (hashed only)

### Is AgentWall SOC 2 compliant?

We're working on SOC 2 certification. Contact us for enterprise security requirements.

## Troubleshooting

### "Invalid API Key" error

- Verify key starts with `aw-`
- Check key is active in dashboard
- Ensure no extra whitespace

### High latency

AgentWall adds <10ms. If you see high latency:
- Check your network
- LLM provider may be slow
- Use streaming for better UX

### Loop detected unexpectedly

Check if you're:
- Reusing the same `run_id` across tasks
- Sending very similar prompts
- Using retry logic without variation

### Budget exceeded too quickly

- Check model pricing (GPT-4 is 60x more expensive than GPT-3.5)
- Review token usage in dashboard
- Increase budget limits

## Pricing

### Is there a free tier?

Yes! Free tier includes:
- 100 requests/day
- Basic loop detection
- 7-day log retention

### What's included in Pro?

- 10,000 requests/day
- Advanced loop detection
- 30-day log retention
- Slack alerts
- Priority support

### Enterprise pricing?

Contact us at [enterprise@agentwall.io](mailto:enterprise@agentwall.io) for:
- Unlimited requests
- Self-hosting
- Custom SLAs
- Dedicated support

## Support

### How do I get help?

- **Documentation**: [docs.agentwall.io](https://docs.agentwall.io)
- **Email**: [support@agentwall.io](mailto:support@agentwall.io)
- **Discord**: [discord.gg/agentwall](https://discord.gg/agentwall)

### How do I report a bug?

Email [bugs@agentwall.io](mailto:bugs@agentwall.io) with:
- Your run_id
- Error message
- Steps to reproduce

---

**Still have questions?** [Contact us](https://agentwall.io/contact)
