# CrewAI Integration

Use AgentWall with CrewAI for protected multi-agent systems.

## Installation

```bash
pip install crewai crewai-tools
```

## Basic Setup

```python
from crewai import Agent, Task, Crew
from langchain_openai import ChatOpenAI
import uuid

# Create protected LLM
run_id = f"crew-{uuid.uuid4().hex[:8]}"

llm = ChatOpenAI(
    base_url="https://api.agentwall.io/v1",
    api_key="aw-your-api-key",
    model="gpt-4",
    model_kwargs={"agentwall_run_id": run_id}
)

# Create agents with protected LLM
researcher = Agent(
    role="Researcher",
    goal="Research and gather information",
    backstory="Expert researcher with attention to detail",
    llm=llm,
    verbose=True
)

writer = Agent(
    role="Writer",
    goal="Write clear and engaging content",
    backstory="Professional writer with years of experience",
    llm=llm,
    verbose=True
)

# Create tasks
research_task = Task(
    description="Research the latest trends in AI safety",
    expected_output="A summary of key AI safety trends",
    agent=researcher
)

writing_task = Task(
    description="Write a blog post based on the research",
    expected_output="A 500-word blog post",
    agent=writer
)

# Create and run crew
crew = Crew(
    agents=[researcher, writer],
    tasks=[research_task, writing_task],
    verbose=True
)

result = crew.kickoff()
print(result)
```

## Per-Agent Run Tracking

Track each agent separately:

```python
import uuid

def create_protected_agent(role, goal, backstory):
    """Create an agent with its own run tracking"""
    run_id = f"{role.lower()}-{uuid.uuid4().hex[:8]}"
    
    llm = ChatOpenAI(
        base_url="https://api.agentwall.io/v1",
        api_key="aw-your-api-key",
        model="gpt-4",
        model_kwargs={"agentwall_run_id": run_id}
    )
    
    return Agent(
        role=role,
        goal=goal,
        backstory=backstory,
        llm=llm,
        verbose=True
    )

# Each agent has its own run_id for independent tracking
researcher = create_protected_agent(
    "Researcher",
    "Research topics thoroughly",
    "Expert researcher"
)

analyst = create_protected_agent(
    "Analyst", 
    "Analyze data and findings",
    "Data analyst"
)

writer = create_protected_agent(
    "Writer",
    "Write compelling content",
    "Content writer"
)
```

## Handling Agent Loops

CrewAI agents can sometimes get stuck. AgentWall protects against this:

```python
from crewai import Agent, Task, Crew
from openai import APIError

def safe_crew_kickoff(crew):
    """Run crew with AgentWall protection"""
    try:
        return crew.kickoff()
    except APIError as e:
        if e.status_code == 429:
            error = e.body.get("error", {})
            if error.get("type") == "loop_detected":
                print(f"⚠️ Agent stuck in loop: {error.get('loop_type')}")
                print(f"   Run ID: {error.get('run_id')}")
                # Log to monitoring, alert team, etc.
                return None
            elif error.get("type") == "budget_exceeded":
                print(f"⚠️ Budget exceeded: {error.get('exceeded_limit')}")
                return None
        raise

result = safe_crew_kickoff(crew)
```

## Budget Control for Crews

Set budget limits per crew run:

```python
# In AgentWall dashboard, set budget policy:
# - max_run_cost: $5.00 (per crew run)
# - daily_limit: $50.00
# - monthly_limit: $500.00

# All agents in the crew share the same run_id
crew_run_id = f"crew-{uuid.uuid4().hex[:8]}"

llm = ChatOpenAI(
    base_url="https://api.agentwall.io/v1",
    api_key="aw-your-api-key",
    model="gpt-4",
    model_kwargs={"agentwall_run_id": crew_run_id}
)

# All agents use same LLM = same budget tracking
researcher = Agent(role="Researcher", llm=llm, ...)
writer = Agent(role="Writer", llm=llm, ...)

crew = Crew(agents=[researcher, writer], tasks=[...])

# If total cost exceeds $5, crew is stopped
result = crew.kickoff()
```

## Monitoring Crew Runs

After crew completes, check the dashboard:

```python
# View in dashboard: https://agentwall.io/admin/agent-runs
# Filter by run_id to see all steps

# Or programmatically:
import requests

def get_crew_stats(run_id):
    response = requests.get(
        f"https://api.agentwall.io/v1/runs/{run_id}",
        headers={"Authorization": "Bearer aw-your-api-key"}
    )
    data = response.json()
    
    print(f"Crew Run: {run_id}")
    print(f"  Total Steps: {data['step_count']}")
    print(f"  Total Cost: ${data['total_cost']:.4f}")
    print(f"  Status: {data['status']}")
    
    return data

stats = get_crew_stats(crew_run_id)
```

## Best Practices

### 1. One Run ID Per Crew Execution

```python
# Good: All agents share one run_id
crew_run_id = f"crew-{uuid.uuid4().hex[:8]}"
llm = ChatOpenAI(..., model_kwargs={"agentwall_run_id": crew_run_id})

# All agents use this LLM
```

### 2. Set Appropriate Limits

CrewAI can make many LLM calls. Set limits accordingly:

```
Recommended for CrewAI:
- max_steps: 50-100 (crews are chatty)
- max_run_cost: $5-10 (depends on model)
- timeout: 300s (crews take time)
```

### 3. Use Cheaper Models for Iteration

```python
# Use GPT-3.5 for development
dev_llm = ChatOpenAI(
    base_url="https://api.agentwall.io/v1",
    api_key="aw-your-api-key",
    model="gpt-3.5-turbo",  # Cheaper
    model_kwargs={"agentwall_run_id": run_id}
)

# Use GPT-4 for production
prod_llm = ChatOpenAI(
    base_url="https://api.agentwall.io/v1",
    api_key="aw-your-api-key",
    model="gpt-4",  # Better quality
    model_kwargs={"agentwall_run_id": run_id}
)
```

---

**Next**: [AutoGen Integration](./autogen.md)
