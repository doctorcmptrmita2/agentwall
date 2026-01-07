# LangChain Integration

Use AgentWall with LangChain for protected AI agents.

## Installation

```bash
pip install langchain langchain-openai
```

## Basic Setup

```python
from langchain_openai import ChatOpenAI

# Just change base_url - that's it!
llm = ChatOpenAI(
    base_url="https://api.agentwall.io/v1",
    api_key="aw-your-api-key",
    model="gpt-4"
)

response = llm.invoke("What is the capital of France?")
print(response.content)
```

## With Run Tracking

For multi-step chains, pass `agentwall_run_id` in model_kwargs:

```python
from langchain_openai import ChatOpenAI
from langchain.schema import HumanMessage
import uuid

run_id = f"langchain-{uuid.uuid4().hex[:8]}"

llm = ChatOpenAI(
    base_url="https://api.agentwall.io/v1",
    api_key="aw-your-api-key",
    model="gpt-4",
    model_kwargs={"agentwall_run_id": run_id}
)

# All requests in this chain use the same run_id
response1 = llm.invoke([HumanMessage(content="Research AI safety")])
response2 = llm.invoke([HumanMessage(content="Summarize the findings")])
```

## LangChain Agents

### ReAct Agent with AgentWall

```python
from langchain_openai import ChatOpenAI
from langchain.agents import create_react_agent, AgentExecutor
from langchain.tools import Tool
from langchain import hub
import uuid

# Create protected LLM
run_id = f"agent-{uuid.uuid4().hex[:8]}"

llm = ChatOpenAI(
    base_url="https://api.agentwall.io/v1",
    api_key="aw-your-api-key",
    model="gpt-4",
    model_kwargs={"agentwall_run_id": run_id}
)

# Define tools
def search(query: str) -> str:
    return f"Search results for: {query}"

def calculator(expression: str) -> str:
    return str(eval(expression))

tools = [
    Tool(name="search", func=search, description="Search the web"),
    Tool(name="calculator", func=calculator, description="Do math"),
]

# Create agent
prompt = hub.pull("hwchase17/react")
agent = create_react_agent(llm, tools, prompt)
executor = AgentExecutor(agent=agent, tools=tools, verbose=True)

# Run agent - protected by AgentWall!
result = executor.invoke({"input": "What is 25 * 4?"})
print(result["output"])
```

### Handling Loop Detection

```python
from langchain_openai import ChatOpenAI
from openai import APIError

llm = ChatOpenAI(
    base_url="https://api.agentwall.io/v1",
    api_key="aw-your-api-key",
    model="gpt-4",
    model_kwargs={"agentwall_run_id": "my-agent-001"}
)

try:
    # If agent gets stuck in a loop, AgentWall will block it
    response = llm.invoke("Repeat this forever")
except APIError as e:
    if e.status_code == 429:
        error = e.body.get("error", {})
        if error.get("type") == "loop_detected":
            print(f"Agent loop detected: {error.get('loop_type')}")
            # Handle gracefully - maybe start new run
        elif error.get("type") == "budget_exceeded":
            print(f"Budget exceeded: {error.get('exceeded_limit')}")
            # Stop agent or increase budget
```

## LangChain Chains

### Sequential Chain

```python
from langchain_openai import ChatOpenAI
from langchain.prompts import ChatPromptTemplate
from langchain.schema.runnable import RunnableSequence
import uuid

run_id = f"chain-{uuid.uuid4().hex[:8]}"

llm = ChatOpenAI(
    base_url="https://api.agentwall.io/v1",
    api_key="aw-your-api-key",
    model="gpt-3.5-turbo",
    model_kwargs={"agentwall_run_id": run_id}
)

# Chain 1: Generate outline
outline_prompt = ChatPromptTemplate.from_template(
    "Create an outline for an article about {topic}"
)

# Chain 2: Write article
article_prompt = ChatPromptTemplate.from_template(
    "Write a short article based on this outline:\n{outline}"
)

# Combined chain
chain = (
    outline_prompt 
    | llm 
    | (lambda x: {"outline": x.content})
    | article_prompt 
    | llm
)

result = chain.invoke({"topic": "renewable energy"})
print(result.content)
```

## Streaming with LangChain

```python
from langchain_openai import ChatOpenAI
from langchain.callbacks.streaming_stdout import StreamingStdOutCallbackHandler

llm = ChatOpenAI(
    base_url="https://api.agentwall.io/v1",
    api_key="aw-your-api-key",
    model="gpt-4",
    streaming=True,
    callbacks=[StreamingStdOutCallbackHandler()]
)

# Streams to stdout
llm.invoke("Write a haiku about coding")
```

## Best Practices

### 1. Use Unique Run IDs

```python
import uuid

def create_agent_run():
    run_id = f"agent-{uuid.uuid4().hex[:8]}"
    return ChatOpenAI(
        base_url="https://api.agentwall.io/v1",
        api_key="aw-your-api-key",
        model="gpt-4",
        model_kwargs={"agentwall_run_id": run_id}
    )
```

### 2. Handle Errors Gracefully

```python
from tenacity import retry, stop_after_attempt, retry_if_exception_type
from openai import APIError

@retry(
    stop=stop_after_attempt(3),
    retry=retry_if_exception_type(APIError)
)
def safe_invoke(llm, message):
    try:
        return llm.invoke(message)
    except APIError as e:
        if e.status_code == 429:
            # Don't retry loop/budget errors
            raise
        raise
```

### 3. Monitor Costs

```python
# After each chain run, check the dashboard
# https://agentwall.io/admin/agent-runs

# Or use the API to get run details
import requests

response = requests.get(
    f"https://api.agentwall.io/v1/runs/{run_id}",
    headers={"Authorization": "Bearer aw-your-api-key"}
)
print(response.json())
```

---

**Next**: [CrewAI Integration](./crewai.md)
