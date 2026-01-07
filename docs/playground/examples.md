# Playground Examples

Interactive examples to test AgentWall features.

## Quick Test

### Test Your API Key

```bash
curl https://api.agentwall.io/health \
  -H "Authorization: Bearer aw-your-api-key"
```

Expected response:
```json
{"status": "healthy", "version": "1.0.0"}
```

### Simple Chat Request

```bash
curl https://api.agentwall.io/v1/chat/completions \
  -H "Authorization: Bearer aw-your-api-key" \
  -H "Content-Type: application/json" \
  -d '{
    "model": "gpt-3.5-turbo",
    "messages": [{"role": "user", "content": "Say hello!"}],
    "max_tokens": 50
  }'
```

## Run Tracking Examples

### Multi-Step Agent Task

Simulate an agent performing a research task:

```python
from openai import OpenAI
import uuid

client = OpenAI(
    base_url="https://api.agentwall.io/v1",
    api_key="aw-your-api-key"
)

# Create a unique run ID for this task
run_id = f"research-{uuid.uuid4().hex[:8]}"
print(f"Starting run: {run_id}")

# Step 1: Define the task
response1 = client.chat.completions.create(
    model="gpt-3.5-turbo",
    messages=[
        {"role": "system", "content": "You are a research assistant."},
        {"role": "user", "content": "I need to research renewable energy. What are the main types?"}
    ],
    max_tokens=200,
    extra_body={"agentwall_run_id": run_id}
)
print(f"Step 1: {response1.choices[0].message.content[:100]}...")
print(f"Cost: ${response1.model_extra['agentwall']['cost_usd']:.6f}")

# Step 2: Deep dive
response2 = client.chat.completions.create(
    model="gpt-3.5-turbo",
    messages=[
        {"role": "user", "content": "Tell me more about solar energy specifically."}
    ],
    max_tokens=200,
    extra_body={"agentwall_run_id": run_id}
)
print(f"Step 2: {response2.choices[0].message.content[:100]}...")
print(f"Total run cost: ${response2.model_extra['agentwall']['total_run_cost']:.6f}")

# Step 3: Summarize
response3 = client.chat.completions.create(
    model="gpt-3.5-turbo",
    messages=[
        {"role": "user", "content": "Summarize the key points in 3 bullet points."}
    ],
    max_tokens=150,
    extra_body={"agentwall_run_id": run_id}
)
print(f"Step 3: {response3.choices[0].message.content}")
print(f"\nFinal run summary:")
print(f"  Run ID: {run_id}")
print(f"  Total steps: {response3.model_extra['agentwall']['total_run_steps']}")
print(f"  Total cost: ${response3.model_extra['agentwall']['total_run_cost']:.6f}")
```

## Loop Detection Examples

### Test Exact Loop Detection

This will trigger loop detection on the 2nd request:

```python
from openai import OpenAI, APIError

client = OpenAI(
    base_url="https://api.agentwall.io/v1",
    api_key="aw-your-api-key"
)

run_id = "loop-test-001"

# Request 1: OK
response1 = client.chat.completions.create(
    model="gpt-3.5-turbo",
    messages=[{"role": "user", "content": "What is 2+2?"}],
    max_tokens=10,
    extra_body={"agentwall_run_id": run_id}
)
print(f"Request 1: {response1.choices[0].message.content}")

# Request 2: Same prompt - BLOCKED!
try:
    response2 = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": "What is 2+2?"}],  # Same!
        max_tokens=10,
        extra_body={"agentwall_run_id": run_id}
    )
except APIError as e:
    print(f"Request 2: BLOCKED!")
    print(f"  Type: {e.body['error']['type']}")
    print(f"  Loop type: {e.body['error']['loop_type']}")
    print(f"  Confidence: {e.body['error']['confidence']}")
```

Expected output:
```
Request 1: 4
Request 2: BLOCKED!
  Type: loop_detected
  Loop type: exact_prompt
  Confidence: 1.0
```

### Test Oscillation Detection

This will trigger on the A→B→A pattern:

```python
run_id = "oscillation-test-001"

prompts = ["What is Python?", "What is JavaScript?"]

for i in range(5):
    prompt = prompts[i % 2]  # Alternates: Python, JS, Python, JS...
    try:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": prompt}],
            max_tokens=30,
            extra_body={"agentwall_run_id": run_id}
        )
        print(f"Request {i+1}: OK - {prompt}")
    except APIError as e:
        print(f"Request {i+1}: BLOCKED - {e.body['error']['type']}")
        break
```

Expected output:
```
Request 1: OK - What is Python?
Request 2: OK - What is JavaScript?
Request 3: BLOCKED - loop_detected
```

## DLP Examples

### Test Sensitive Data Masking

AgentWall automatically masks sensitive data in responses:

```python
response = client.chat.completions.create(
    model="gpt-3.5-turbo",
    messages=[
        {"role": "user", "content": "Generate a fake API key for testing"}
    ],
    max_tokens=100
)

# If the model generates something like "sk-abc123...",
# AgentWall will mask it to "[REDACTED:OPENAI_KEY]"
print(response.choices[0].message.content)
```

### Test with Known Patterns

```python
# These patterns are detected and masked:
test_cases = [
    "My credit card is 4111-1111-1111-1111",
    "AWS key: AKIAIOSFODNN7EXAMPLE",
    "Email me at ceo@company.com",
    "My SSN is 123-45-6789"
]

for test in test_cases:
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": f"Repeat this: {test}"}],
        max_tokens=100
    )
    print(f"Input: {test}")
    print(f"Output: {response.choices[0].message.content}")
    print()
```

## Streaming Example

### Basic Streaming

```python
stream = client.chat.completions.create(
    model="gpt-3.5-turbo",
    messages=[{"role": "user", "content": "Write a haiku about AI"}],
    stream=True
)

print("Streaming response:")
for chunk in stream:
    if chunk.choices[0].delta.content:
        print(chunk.choices[0].delta.content, end="", flush=True)
print()
```

### Streaming with Run Tracking

```python
run_id = "stream-test-001"

stream = client.chat.completions.create(
    model="gpt-3.5-turbo",
    messages=[{"role": "user", "content": "Count from 1 to 5"}],
    stream=True,
    extra_body={"agentwall_run_id": run_id}
)

for chunk in stream:
    if chunk.choices[0].delta.content:
        print(chunk.choices[0].delta.content, end="", flush=True)
print()

# Check run status after streaming
# (Cost is calculated after stream completes)
```

## Budget Testing

### Test Budget Limits

```python
run_id = "budget-test-001"

# Make requests until budget is exceeded
for i in range(20):
    try:
        response = client.chat.completions.create(
            model="gpt-4",  # More expensive model
            messages=[{"role": "user", "content": f"Request {i+1}: Tell me a fact"}],
            max_tokens=100,
            extra_body={"agentwall_run_id": run_id}
        )
        aw = response.model_extra['agentwall']
        print(f"Request {i+1}: ${aw['cost_usd']:.4f} (Total: ${aw['total_run_cost']:.4f})")
    except APIError as e:
        if e.body['error']['type'] == 'budget_exceeded':
            print(f"Request {i+1}: BUDGET EXCEEDED!")
            print(f"  Limit: ${e.body['error']['limit']}")
            print(f"  Current: ${e.body['error']['current_cost']}")
            break
        raise
```

## cURL Examples

### Complete cURL Test Suite

```bash
# 1. Health check
curl -s https://api.agentwall.io/health | jq

# 2. Simple request
curl -s https://api.agentwall.io/v1/chat/completions \
  -H "Authorization: Bearer aw-your-api-key" \
  -H "Content-Type: application/json" \
  -d '{"model":"gpt-3.5-turbo","messages":[{"role":"user","content":"Hi"}],"max_tokens":10}' | jq

# 3. With run tracking
curl -s https://api.agentwall.io/v1/chat/completions \
  -H "Authorization: Bearer aw-your-api-key" \
  -H "Content-Type: application/json" \
  -d '{"model":"gpt-3.5-turbo","messages":[{"role":"user","content":"Hello"}],"agentwall_run_id":"curl-test-001"}' | jq '.agentwall'

# 4. Streaming
curl -N https://api.agentwall.io/v1/chat/completions \
  -H "Authorization: Bearer aw-your-api-key" \
  -H "Content-Type: application/json" \
  -d '{"model":"gpt-3.5-turbo","messages":[{"role":"user","content":"Count 1-3"}],"stream":true}'
```

---

**Next**: [LangChain Integration](../guide/integrations/langchain.md)
