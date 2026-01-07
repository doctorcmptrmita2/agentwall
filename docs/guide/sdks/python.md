# Python SDK Guide

Learn how to integrate AgentWall with your Python agent frameworks.

## Installation

```bash
pip install agentwall-sdk
# or
pip install requests
```

## Basic Usage

### Simple Chat Completion

```python
import requests

API_KEY = "aw-your-api-key"
BASE_URL = "https://api.agentwall.io"

def chat_with_agentwall(messages, model="gpt-4o-mini"):
    """Send a chat completion request to AgentWall"""
    
    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json"
    }
    
    payload = {
        "model": model,
        "messages": messages,
        "temperature": 0.7
    }
    
    response = requests.post(
        f"{BASE_URL}/v1/chat/completions",
        json=payload,
        headers=headers
    )
    
    response.raise_for_status()
    return response.json()

# Example
messages = [
    {"role": "user", "content": "What is 2+2?"}
]

result = chat_with_agentwall(messages)
print(result["choices"][0]["message"]["content"])
```

## Run-Level Tracking

Track multi-step agent tasks with run IDs:

```python
import requests
import uuid

API_KEY = "aw-your-api-key"
BASE_URL = "https://api.agentwall.io"

class AgentWallClient:
    def __init__(self, api_key, base_url="https://api.agentwall.io"):
        self.api_key = api_key
        self.base_url = base_url
        self.headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json"
        }
    
    def create_run(self):
        """Create a new run ID for tracking"""
        return str(uuid.uuid4())
    
    def chat(self, messages, run_id=None, model="gpt-4o-mini"):
        """Send a chat completion with run tracking"""
        
        payload = {
            "model": model,
            "messages": messages,
            "temperature": 0.7
        }
        
        # Add run ID to track multi-step tasks
        if run_id:
            payload["agentwall_run_id"] = run_id
        
        response = requests.post(
            f"{self.base_url}/v1/chat/completions",
            json=payload,
            headers=self.headers
        )
        
        response.raise_for_status()
        return response.json()

# Example: Multi-step task
client = AgentWallClient(API_KEY)
run_id = client.create_run()

# Step 1: Analyze problem
messages = [{"role": "user", "content": "Analyze this data: [1,2,3,4,5]"}]
result1 = client.chat(messages, run_id=run_id)
print(f"Step 1: {result1['choices'][0]['message']['content']}")

# Step 2: Generate solution (same run_id)
messages = [
    {"role": "user", "content": "Analyze this data: [1,2,3,4,5]"},
    {"role": "assistant", "content": result1['choices'][0]['message']['content']},
    {"role": "user", "content": "Now generate a solution"}
]
result2 = client.chat(messages, run_id=run_id)
print(f"Step 2: {result2['choices'][0]['message']['content']}")

# AgentWall tracks both steps under the same run_id
# If loop detected, request will be blocked with 429 status
```

## Streaming Responses

Handle streaming responses for real-time output:

```python
import requests
import json

def stream_chat(messages, run_id=None, model="gpt-4o-mini"):
    """Stream chat completion responses"""
    
    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json"
    }
    
    payload = {
        "model": model,
        "messages": messages,
        "stream": True
    }
    
    if run_id:
        payload["agentwall_run_id"] = run_id
    
    response = requests.post(
        f"{BASE_URL}/v1/chat/completions",
        json=payload,
        headers=headers,
        stream=True
    )
    
    response.raise_for_status()
    
    # Process streaming response
    for line in response.iter_lines():
        if line:
            line = line.decode('utf-8')
            if line.startswith('data: '):
                data = line[6:]  # Remove 'data: ' prefix
                if data == '[DONE]':
                    break
                try:
                    chunk = json.loads(data)
                    if 'choices' in chunk:
                        delta = chunk['choices'][0].get('delta', {})
                        if 'content' in delta:
                            print(delta['content'], end='', flush=True)
                except json.JSONDecodeError:
                    pass

# Example
messages = [{"role": "user", "content": "Write a short poem about AI"}]
stream_chat(messages)
```

## LangChain Integration

Use AgentWall with LangChain:

```python
from langchain.chat_models import ChatOpenAI
from langchain.schema import HumanMessage, SystemMessage
import os

# Configure to use AgentWall as proxy
os.environ["OPENAI_API_KEY"] = "aw-your-api-key"
os.environ["OPENAI_API_BASE"] = "https://api.agentwall.io/v1"

# Create LangChain chat model
chat = ChatOpenAI(
    model="gpt-4o-mini",
    temperature=0.7,
    openai_api_base="https://api.agentwall.io/v1",
    openai_api_key="aw-your-api-key"
)

# Use normally
messages = [
    SystemMessage(content="You are a helpful assistant."),
    HumanMessage(content="What is 2+2?")
]

response = chat(messages)
print(response.content)
```

## CrewAI Integration

Use AgentWall with CrewAI agents:

```python
from crewai import Agent, Task, Crew
from langchain.chat_models import ChatOpenAI
import os

# Configure OpenAI to use AgentWall
os.environ["OPENAI_API_KEY"] = "aw-your-api-key"
os.environ["OPENAI_API_BASE"] = "https://api.agentwall.io/v1"

# Create LLM instance
llm = ChatOpenAI(
    model="gpt-4o-mini",
    openai_api_base="https://api.agentwall.io/v1",
    openai_api_key="aw-your-api-key"
)

# Create agents
researcher = Agent(
    role="Researcher",
    goal="Find and analyze information",
    llm=llm
)

analyst = Agent(
    role="Analyst",
    goal="Analyze findings and provide insights",
    llm=llm
)

# Create tasks
research_task = Task(
    description="Research the latest AI trends",
    agent=researcher
)

analysis_task = Task(
    description="Analyze the research findings",
    agent=analyst
)

# Create crew
crew = Crew(
    agents=[researcher, analyst],
    tasks=[research_task, analysis_task]
)

# Execute
result = crew.kickoff()
print(result)
```

## Error Handling

Handle AgentWall-specific errors:

```python
import requests
from requests.exceptions import RequestException

def safe_chat(messages, run_id=None):
    """Chat with proper error handling"""
    
    try:
        headers = {
            "Authorization": f"Bearer {API_KEY}",
            "Content-Type": "application/json"
        }
        
        payload = {
            "model": "gpt-4o-mini",
            "messages": messages
        }
        
        if run_id:
            payload["agentwall_run_id"] = run_id
        
        response = requests.post(
            f"{BASE_URL}/v1/chat/completions",
            json=payload,
            headers=headers,
            timeout=30
        )
        
        # Handle AgentWall-specific errors
        if response.status_code == 429:
            error_data = response.json()
            if error_data.get("detail", {}).get("error", {}).get("type") == "loop_detected":
                print("⚠️ Loop detected! Agent is repeating the same prompt.")
                print(f"Steps: {error_data.get('detail', {}).get('error', {}).get('steps')}")
                return None
        
        if response.status_code == 401:
            print("❌ Authentication failed. Check your API key.")
            return None
        
        if response.status_code == 422:
            print("❌ Validation error:", response.json())
            return None
        
        response.raise_for_status()
        return response.json()
    
    except RequestException as e:
        print(f"❌ Request failed: {e}")
        return None

# Example
messages = [{"role": "user", "content": "Hello"}]
result = safe_chat(messages, run_id="my-run-123")
if result:
    print(result["choices"][0]["message"]["content"])
```

## Budget Tracking

Monitor costs and budgets:

```python
class BudgetAwareClient:
    def __init__(self, api_key, budget_limit=10.0):
        self.api_key = api_key
        self.budget_limit = budget_limit
        self.spent = 0.0
    
    def chat(self, messages, run_id=None):
        """Chat with budget awareness"""
        
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
        
        payload = {
            "model": "gpt-4o-mini",
            "messages": messages
        }
        
        if run_id:
            payload["agentwall_run_id"] = run_id
        
        response = requests.post(
            f"{BASE_URL}/v1/chat/completions",
            json=payload,
            headers=headers
        )
        
        response.raise_for_status()
        result = response.json()
        
        # Extract cost from response
        if "usage" in result:
            # Estimate cost (adjust based on your pricing)
            tokens = result["usage"].get("total_tokens", 0)
            cost = tokens * 0.000001  # Example: $1 per 1M tokens
            self.spent += cost
            
            print(f"💰 Cost: ${cost:.6f} | Total: ${self.spent:.6f} / ${self.budget_limit}")
            
            if self.spent > self.budget_limit:
                print("⚠️ Budget limit exceeded!")
        
        return result

# Example
client = BudgetAwareClient(API_KEY, budget_limit=5.0)
messages = [{"role": "user", "content": "What is AI?"}]
result = client.chat(messages)
```

## Best Practices

1. **Always use run IDs for multi-step tasks** - Enables loop detection and cost tracking
2. **Handle 429 responses** - Loop detection blocks requests with 429 status
3. **Set appropriate timeouts** - LLM responses can take time
4. **Monitor costs** - Track spending to stay within budget
5. **Use streaming for long responses** - Better UX and real-time feedback
6. **Implement retry logic** - Handle transient failures gracefully

## Troubleshooting

### Loop Detection Blocking Requests

If you see `429 Loop detected` errors:
- Check if you're sending the same prompt repeatedly
- Use different run IDs for different tasks
- Verify your agent logic isn't stuck in a loop

### Authentication Errors

If you see `401 Unauthorized`:
- Verify your API key is correct
- Check the key hasn't been revoked
- Ensure the key is passed in the Authorization header

### Timeout Issues

If requests timeout:
- Increase the timeout value
- Check your network connection
- Verify the API is responding (check `/health` endpoint)

## Next Steps

- Check out [LangChain Integration](../integrations/langchain.md)
- Read [CrewAI Integration](../integrations/crewai.md)
- Explore [API Reference](../../api/chat-completions.md)
