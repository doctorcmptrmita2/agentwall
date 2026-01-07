# SDK Examples

Complete code examples for integrating AgentWall with your agent frameworks and applications.

## Quick Start

Choose your language and framework:

### Python
- **[Python SDK Guide](./python.md)** - Complete Python integration guide
  - Basic chat completions
  - Run-level tracking for multi-step tasks
  - Streaming responses
  - LangChain integration
  - CrewAI integration
  - Error handling
  - Budget tracking

### JavaScript/TypeScript
- **[JavaScript SDK Guide](./javascript.md)** - Complete JavaScript/TypeScript guide
  - Basic chat completions
  - TypeScript client class
  - Run-level tracking
  - Streaming with React
  - LangChain.js integration
  - Error handling
  - Budget tracking

## Framework Integrations

### Python Frameworks

#### LangChain
```python
from langchain.chat_models import ChatOpenAI

chat = ChatOpenAI(
    model="gpt-4o-mini",
    openai_api_base="https://api.agentwall.io/v1",
    openai_api_key="aw-your-api-key"
)
```

#### CrewAI
```python
from crewai import Agent, Task, Crew
from langchain.chat_models import ChatOpenAI

llm = ChatOpenAI(
    model="gpt-4o-mini",
    openai_api_base="https://api.agentwall.io/v1",
    openai_api_key="aw-your-api-key"
)

agent = Agent(role="Researcher", goal="Find information", llm=llm)
```

#### AutoGen
```python
import autogen

config_list = [
    {
        "model": "gpt-4o-mini",
        "api_key": "aw-your-api-key",
        "base_url": "https://api.agentwall.io/v1"
    }
]

assistant = autogen.AssistantAgent(
    name="assistant",
    llm_config={"config_list": config_list}
)
```

### JavaScript Frameworks

#### LangChain.js
```typescript
import { ChatOpenAI } from "langchain/chat_models/openai";

const chat = new ChatOpenAI({
    openAIApiKey: "aw-your-api-key",
    modelName: "gpt-4o-mini",
    configuration: {
        baseURL: "https://api.agentwall.io/v1"
    }
});
```

#### React
```typescript
import AgentWallClient from "./AgentWallClient";

const client = new AgentWallClient("aw-your-api-key");

await client.stream(messages, {
    onChunk: (chunk) => setStreaming(prev => prev + chunk)
});
```

## Common Patterns

### Multi-Step Task with Run Tracking

**Python:**
```python
client = AgentWallClient(API_KEY)
run_id = client.create_run()

# Step 1
result1 = client.chat(messages1, run_id=run_id)

# Step 2 (same run_id)
result2 = client.chat(messages2, run_id=run_id)
```

**JavaScript:**
```typescript
const client = new AgentWallClient("aw-your-api-key");
const runId = uuidv4();

// Step 1
const result1 = await client.chat(messages1, { runId });

// Step 2 (same runId)
const result2 = await client.chat(messages2, { runId });
```

### Streaming Responses

**Python:**
```python
for line in response.iter_lines():
    if line.startswith('data: '):
        data = line[6:]
        if data != '[DONE]':
            chunk = json.loads(data)
            print(chunk['choices'][0]['delta']['content'], end='')
```

**JavaScript:**
```typescript
await client.stream(messages, {
    onChunk: (chunk) => {
        process.stdout.write(chunk);
    }
});
```

### Error Handling

**Python:**
```python
try:
    result = client.chat(messages, run_id=run_id)
except requests.exceptions.RequestException as e:
    if response.status_code == 429:
        print("Loop detected!")
    elif response.status_code == 401:
        print("Authentication failed!")
```

**JavaScript:**
```typescript
try {
    const result = await client.chat(messages, { runId });
} catch (error) {
    if (error.message.includes("loop_detected")) {
        console.warn("Loop detected!");
    } else if (error.message.includes("401")) {
        console.error("Authentication failed!");
    }
}
```

## API Key Management

### Getting Your API Key

1. Go to https://agentwall.io/admin
2. Navigate to "API Keys"
3. Click "Create New Key"
4. Copy the key (format: `aw-xxxxx`)

### Using API Keys Securely

**Python:**
```python
import os
from dotenv import load_dotenv

load_dotenv()
API_KEY = os.getenv("AGENTWALL_API_KEY")
```

**JavaScript:**
```typescript
const API_KEY = process.env.REACT_APP_AGENTWALL_API_KEY;
```

**.env file:**
```
AGENTWALL_API_KEY=aw-your-api-key
```

## Best Practices

### 1. Always Use Run IDs for Multi-Step Tasks
Enables loop detection and cost tracking across the entire task.

### 2. Handle Streaming Properly
Use streaming for better UX and real-time feedback on long responses.

### 3. Implement Error Handling
Catch and handle API errors gracefully, especially 429 (loop detected) and 401 (auth failed).

### 4. Monitor Costs
Track spending to stay within budget limits.

### 5. Use Type Hints (Python) / TypeScript
Better IDE support and fewer runtime errors.

### 6. Implement Retry Logic
Handle transient failures with exponential backoff.

## Troubleshooting

### Loop Detection Blocking Requests (429)

**Problem:** Getting `429 Loop detected` errors

**Solution:**
- Check if you're sending the same prompt repeatedly
- Use different run IDs for different tasks
- Verify your agent logic isn't stuck in a loop

### Authentication Errors (401)

**Problem:** Getting `401 Unauthorized` errors

**Solution:**
- Verify your API key is correct
- Check the key hasn't been revoked
- Ensure the key is passed in the Authorization header

### Timeout Issues

**Problem:** Requests timing out

**Solution:**
- Increase the timeout value
- Check your network connection
- Verify the API is responding (check `/health` endpoint)

### Streaming Not Working

**Problem:** Streaming responses aren't working

**Solution:**
- Ensure `stream: true` is set in the payload
- Check that your client supports streaming
- Verify the response body is readable

## Performance Tips

1. **Reuse client instances** - Don't create a new client for each request
2. **Use connection pooling** - For high-volume applications
3. **Implement caching** - Cache responses when appropriate
4. **Monitor latency** - Track response times to identify bottlenecks
5. **Use streaming** - For long responses to improve perceived performance

## Security Tips

1. **Never hardcode API keys** - Use environment variables
2. **Rotate keys regularly** - Change keys periodically
3. **Use HTTPS only** - Always use secure connections
4. **Validate responses** - Check response structure before processing
5. **Handle sensitive data** - Be careful with PII in prompts

## Next Steps

- Read the [Python SDK Guide](./python.md) for detailed Python examples
- Read the [JavaScript SDK Guide](./javascript.md) for detailed JavaScript examples
- Check out [LangChain Integration](../integrations/langchain.md)
- Read [CrewAI Integration](../integrations/crewai.md)
- Explore [API Reference](../../api/chat-completions.md)
- Review [Concepts](../concepts.md) for architectural details

## Support

- **Documentation:** https://docs.agentwall.io
- **API Status:** https://api.agentwall.io/health
- **Dashboard:** https://agentwall.io/admin
- **Issues:** Report bugs on GitHub

---

**Motto:** Guard the Agent, Save the Budget 🛡️
