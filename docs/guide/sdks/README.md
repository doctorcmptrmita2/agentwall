# AgentWall SDK Examples

Production-ready code examples for integrating AgentWall with your AI agent applications.

## 📚 Documentation

- **[SDK Overview](./index.md)** - Start here for quick reference
- **[Python SDK](./python.md)** - Complete Python integration guide
- **[JavaScript/TypeScript SDK](./javascript.md)** - Complete JavaScript guide

## 🚀 Quick Start

### Python

```python
import requests

API_KEY = "aw-your-api-key"
BASE_URL = "https://api.agentwall.io"

response = requests.post(
    f"{BASE_URL}/v1/chat/completions",
    headers={"Authorization": f"Bearer {API_KEY}"},
    json={
        "model": "gpt-4o-mini",
        "messages": [{"role": "user", "content": "What is 2+2?"}]
    }
)

print(response.json()["choices"][0]["message"]["content"])
```

### JavaScript

```javascript
const API_KEY = "aw-your-api-key";
const BASE_URL = "https://api.agentwall.io";

const response = await fetch(`${BASE_URL}/v1/chat/completions`, {
    method: "POST",
    headers: {
        "Authorization": `Bearer ${API_KEY}`,
        "Content-Type": "application/json"
    },
    body: JSON.stringify({
        model: "gpt-4o-mini",
        messages: [{ role: "user", content: "What is 2+2?" }]
    })
});

const data = await response.json();
console.log(data.choices[0].message.content);
```

## 🎯 Key Features

### Run-Level Tracking
Track multi-step agent tasks with a single run ID:

```python
# Python
run_id = "my-task-123"
result1 = client.chat(messages1, run_id=run_id)
result2 = client.chat(messages2, run_id=run_id)  # Same run
```

```typescript
// JavaScript
const runId = "my-task-123";
const result1 = await client.chat(messages1, { runId });
const result2 = await client.chat(messages2, { runId });  // Same run
```

### Loop Detection
Automatically blocks infinite loops:

```
Request 1: ✅ 200 OK
Request 2: 🛑 429 Loop Detected
```

### Streaming Responses
Real-time output for long-running tasks:

```python
# Python
for chunk in response.iter_lines():
    if chunk.startswith('data: '):
        print(chunk[6:], end='')
```

```typescript
// JavaScript
await client.stream(messages, {
    onChunk: (chunk) => process.stdout.write(chunk)
});
```

### Budget Tracking
Monitor costs in real-time:

```python
# Python
cost = tokens * 0.000001
total_spent += cost
print(f"Cost: ${cost:.6f} | Total: ${total_spent:.6f}")
```

## 🔗 Framework Integrations

### Python
- **LangChain** - Use AgentWall as OpenAI proxy
- **CrewAI** - Multi-agent orchestration
- **AutoGen** - Microsoft's agent framework

### JavaScript
- **LangChain.js** - TypeScript agent framework
- **React** - Real-time chat UI
- **Node.js** - Server-side agents

## 📖 Learning Path

1. **Start:** [SDK Overview](./index.md)
2. **Choose Language:** [Python](./python.md) or [JavaScript](./javascript.md)
3. **Pick Framework:** LangChain, CrewAI, React, etc.
4. **Explore:** [API Reference](../../api/chat-completions.md)
5. **Deploy:** [Getting Started](../getting-started.md)

## 🛡️ Security Best Practices

1. **Never hardcode API keys** - Use environment variables
2. **Use HTTPS only** - Always use secure connections
3. **Rotate keys regularly** - Change keys periodically
4. **Validate responses** - Check response structure
5. **Handle sensitive data** - Be careful with PII

## ⚡ Performance Tips

1. **Reuse client instances** - Don't create new clients per request
2. **Use streaming** - For long responses
3. **Implement caching** - Cache responses when appropriate
4. **Monitor latency** - Track response times
5. **Use connection pooling** - For high-volume apps

## 🐛 Troubleshooting

### Loop Detection (429)
- Check if sending same prompt repeatedly
- Use different run IDs for different tasks
- Verify agent logic isn't stuck in loop

### Authentication (401)
- Verify API key is correct
- Check key hasn't been revoked
- Ensure key in Authorization header

### Timeout Issues
- Increase timeout value
- Check network connection
- Verify API responding (`/health` endpoint)

## 📊 Example Projects

### Python: Multi-Step Analysis
```python
# Analyze → Generate → Refine
client = AgentWallClient(API_KEY)
run_id = client.create_run()

# Step 1: Analyze
analysis = client.chat(analyze_prompt, run_id=run_id)

# Step 2: Generate
solution = client.chat(generate_prompt, run_id=run_id)

# Step 3: Refine
refined = client.chat(refine_prompt, run_id=run_id)
```

### JavaScript: Real-Time Chat
```typescript
// React component with streaming
const [streaming, setStreaming] = useState("");

await client.stream(messages, {
    onChunk: (chunk) => {
        setStreaming(prev => prev + chunk);
    }
});
```

## 🔗 Related Resources

- **[API Reference](../../api/chat-completions.md)** - Complete API documentation
- **[Concepts](../concepts.md)** - Architectural concepts
- **[Getting Started](../getting-started.md)** - Setup guide
- **[FAQ](../faq.md)** - Common questions
- **[Integrations](../integrations/)** - Framework integrations

## 📞 Support

- **Documentation:** https://docs.agentwall.io
- **API Status:** https://api.agentwall.io/health
- **Dashboard:** https://agentwall.io/admin
- **GitHub:** https://github.com/agentwall/agentwall

## 📝 License

MIT License - See LICENSE file for details

---

**Motto:** Guard the Agent, Save the Budget 🛡️

**Version:** 1.0.0  
**Last Updated:** January 7, 2026
