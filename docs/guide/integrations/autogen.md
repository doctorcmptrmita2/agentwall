# AutoGen Integration

Use AgentWall with Microsoft AutoGen for protected conversational agents.

## Installation

```bash
pip install pyautogen
```

## Basic Setup

```python
import autogen
import uuid

run_id = f"autogen-{uuid.uuid4().hex[:8]}"

# Configure with AgentWall
config_list = [
    {
        "model": "gpt-4",
        "base_url": "https://api.agentwall.io/v1",
        "api_key": "aw-your-api-key",
    }
]

llm_config = {
    "config_list": config_list,
    "seed": 42,
    "extra_body": {"agentwall_run_id": run_id}
}

# Create agents
assistant = autogen.AssistantAgent(
    name="assistant",
    llm_config=llm_config,
)

user_proxy = autogen.UserProxyAgent(
    name="user_proxy",
    human_input_mode="NEVER",
    max_consecutive_auto_reply=10,
    code_execution_config={"work_dir": "coding"},
)

# Start conversation
user_proxy.initiate_chat(
    assistant,
    message="Write a Python function to calculate fibonacci numbers"
)
```

## Multi-Agent Conversations

```python
import autogen
import uuid

run_id = f"multiagent-{uuid.uuid4().hex[:8]}"

config_list = [
    {
        "model": "gpt-4",
        "base_url": "https://api.agentwall.io/v1",
        "api_key": "aw-your-api-key",
    }
]

llm_config = {
    "config_list": config_list,
    "extra_body": {"agentwall_run_id": run_id}
}

# Create multiple agents
coder = autogen.AssistantAgent(
    name="Coder",
    system_message="You are a Python developer.",
    llm_config=llm_config,
)

reviewer = autogen.AssistantAgent(
    name="Reviewer",
    system_message="You review code for bugs and improvements.",
    llm_config=llm_config,
)

user_proxy = autogen.UserProxyAgent(
    name="User",
    human_input_mode="NEVER",
    max_consecutive_auto_reply=5,
)

# Group chat
groupchat = autogen.GroupChat(
    agents=[user_proxy, coder, reviewer],
    messages=[],
    max_round=10
)

manager = autogen.GroupChatManager(
    groupchat=groupchat,
    llm_config=llm_config
)

# All agents protected by AgentWall
user_proxy.initiate_chat(
    manager,
    message="Create a REST API endpoint for user registration"
)
```

## Handling Loop Detection

AutoGen agents can get into repetitive conversations:

```python
import autogen
from openai import APIError

def safe_chat(user_proxy, assistant, message):
    """Run AutoGen chat with AgentWall protection"""
    try:
        user_proxy.initiate_chat(assistant, message=message)
    except APIError as e:
        if e.status_code == 429:
            error = e.body.get("error", {})
            if error.get("type") == "loop_detected":
                print(f"⚠️ Conversation loop detected!")
                print(f"   Type: {error.get('loop_type')}")
                # Agents were repeating themselves
                return False
            elif error.get("type") == "budget_exceeded":
                print(f"⚠️ Conversation budget exceeded!")
                return False
        raise
    return True

# Use it
success = safe_chat(
    user_proxy, 
    assistant, 
    "Solve this complex problem..."
)
```

## Budget Control

Set limits for AutoGen conversations:

```python
# In AgentWall dashboard:
# - max_steps: 30 (AutoGen can be chatty)
# - max_run_cost: $2.00
# - timeout: 180s

run_id = f"autogen-{uuid.uuid4().hex[:8]}"

llm_config = {
    "config_list": config_list,
    "extra_body": {"agentwall_run_id": run_id}
}

# Conversation will stop if:
# - 30 LLM calls made
# - $2.00 spent
# - 180 seconds elapsed
# - Loop detected
```

## Code Execution Safety

AutoGen can execute code. Combine with AgentWall for double protection:

```python
import autogen

run_id = f"code-exec-{uuid.uuid4().hex[:8]}"

llm_config = {
    "config_list": [
        {
            "model": "gpt-4",
            "base_url": "https://api.agentwall.io/v1",
            "api_key": "aw-your-api-key",
        }
    ],
    "extra_body": {"agentwall_run_id": run_id}
}

# Code execution in Docker for safety
user_proxy = autogen.UserProxyAgent(
    name="user_proxy",
    human_input_mode="NEVER",
    code_execution_config={
        "work_dir": "coding",
        "use_docker": True,  # Sandboxed execution
    },
)

assistant = autogen.AssistantAgent(
    name="assistant",
    llm_config=llm_config,
)

# AgentWall protects LLM calls
# Docker protects code execution
user_proxy.initiate_chat(
    assistant,
    message="Write and run a script to analyze data.csv"
)
```

## Monitoring Conversations

```python
# After conversation, check AgentWall dashboard
# https://agentwall.io/admin/agent-runs

# Filter by run_id to see:
# - All LLM calls in the conversation
# - Cost per message
# - Any loop warnings
# - Total conversation cost
```

## Best Practices

### 1. Set max_consecutive_auto_reply

```python
user_proxy = autogen.UserProxyAgent(
    name="user_proxy",
    max_consecutive_auto_reply=10,  # Limit back-and-forth
    ...
)
```

### 2. Use Termination Conditions

```python
assistant = autogen.AssistantAgent(
    name="assistant",
    is_termination_msg=lambda x: "TERMINATE" in x.get("content", ""),
    ...
)
```

### 3. Monitor Token Usage

```python
# AutoGen conversations can use many tokens
# Use GPT-3.5 for development
config_list = [
    {
        "model": "gpt-3.5-turbo",  # Cheaper for testing
        "base_url": "https://api.agentwall.io/v1",
        "api_key": "aw-your-api-key",
    }
]
```

---

**Next**: [FAQ](../faq.md)
