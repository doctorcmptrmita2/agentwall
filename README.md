# 🛡️ AgentWall

**The Wall Between Agents and Chaos**

Guard the Agent, Save the Budget

🌐 **agentwall.io**

---

## What is AgentWall?

AgentWall is a smart security and cost control layer that sits between your AI agents and LLM providers (OpenAI, Anthropic, etc.). It prevents infinite loops, blocks sensitive data leaks, and enforces budget limits—all in real-time with <10ms overhead.

**Think of it as a wall that protects your agents from chaos.**

---

## 🎯 Core Features

### 🔄 Loop Detection
- **Step Counter:** Max 30 steps per run
- **Similarity Detection:** Catches repetitive prompts (cosine similarity)
- **Tool Frequency:** Prevents tool spam (same tool 10+ times)
- **Wall-Clock Timeout:** 2-minute maximum per run

### 🔒 Data Loss Prevention (DLP)
- **API Key Detection:** OpenAI, Anthropic, AWS, GitHub tokens
- **PII Detection:** Credit cards (Luhn validated), emails, phone numbers
- **Redaction Modes:** Block, mask, or shadow log
- **Real-time Scanning:** <5ms overhead per request

### 💰 Budget Control
- **Run-Level Budgets:** "$0.50 max per task"
- **Daily/Monthly Limits:** Team and user level
- **Real-time Alerts:** Slack, webhook, email
- **Cost Analytics:** ClickHouse-powered dashboards

### 📊 Observability
- **Run Tracking:** Trace every agent execution
- **Incident Replay:** Debug failed runs step-by-step
- **Performance Metrics:** <10ms proxy overhead
- **Audit Logs:** 90-day retention (auto-archive)

---

## 🚀 Quick Start

### 1. Drop-in Replacement

```python
# Before (Direct OpenAI)
import openai
openai.api_base = "https://api.openai.com/v1"
openai.api_key = "sk-..."

# After (AgentWall)
import openai
openai.api_base = "https://api.agentwall.io/v1"
openai.api_key = "aw-..."  # Your AgentWall API key
```

That's it! AgentFirewall now protects your agent.

### 2. Configuration (Optional)

```python
# Set run-level budget
response = openai.ChatCompletion.create(
    model="gpt-4",
    messages=[...],
    headers={
        "X-AgentFirewall-Max-Steps": "20",
        "X-AgentFirewall-Max-Cost": "0.50",
        "X-AgentFirewall-Run-ID": "task-123"
    }
)
```

---

## 🏗️ Architecture

```
┌─────────────────────────────────────────────────────┐
│  Your AI Agent                                      │
│  (LangChain, AutoGPT, Custom)                       │
└─────────────────┬───────────────────────────────────┘
                  │
                  ▼
┌─────────────────────────────────────────────────────┐
│  🛡️ AgentWall (FastAPI Proxy)                      │
│  ├─ Loop Detection (<10ms)                          │
│  ├─ DLP Scanning (<5ms)                             │
│  ├─ Budget Enforcement                              │
│  └─ Logging (async)                                 │
└─────────────────┬───────────────────────────────────┘
                  │
                  ▼
┌─────────────────────────────────────────────────────┐
│  LLM Providers                                      │
│  (OpenAI, Anthropic, Google, Azure)                 │
└─────────────────────────────────────────────────────┘
```

---

## 📦 Tech Stack

**Proxy Engine (FastAPI):**
- Python 3.11+
- FastAPI (async/await)
- Pydantic V2 (validation)
- Sentence Transformers (loop detection)
- ClickHouse (time-series logs)
- Redis (rate limiting)

**Dashboard (Laravel):**
- Laravel 11
- Filament (admin panel)
- Livewire (real-time UI)
- PostgreSQL (relational data)
- Redis (event bus)

---

## 🎯 Use Cases

### 1. Customer Support Agents
**Problem:** Agent loops on "I don't understand" → $500 bill  
**Solution:** AgentWall kills loop at step 30 → $5 bill

### 2. Content Generation Agents
**Problem:** Agent leaks API key in prompt  
**Solution:** AgentWall blocks request, alerts team

### 3. Research Agents
**Problem:** Agent calls web scraper 100+ times  
**Solution:** AgentWall limits to 10 calls per run

---

## 💰 Pricing

| Plan | Price | Features |
|------|-------|----------|
| **Free** | $0/mo | 1K requests, basic logging |
| **Starter** | $49/mo | 50K requests, loop detection, DLP |
| **Pro** | $199/mo | 500K requests, tool governance, alerts |
| **Enterprise** | Custom | Unlimited, SSO, SLA, dedicated support |

---

## 🚦 Status

**Current Version:** 0.1.0 (MVP)  
**Status:** 🚧 In Development (Week 1/3)  
**Launch Date:** February 2026 (Product Hunt)

**Completed:**
- ✅ Strategic planning
- ✅ Technical architecture
- ✅ FastAPI skeleton
- ✅ Branding & naming

**In Progress:**
- 🚧 Docker Compose setup
- 🚧 ClickHouse schema
- 🚧 OpenAI proxy service
- 🚧 Loop detection engine

**Upcoming:**
- ⏳ DLP engine
- ⏳ Budget tracking
- ⏳ Laravel dashboard

---

## 🤝 Contributing

AgentWall is currently in private development. We'll open-source the core engine after MVP launch.

**Interested in early access?** Join our waitlist: [agentwall.io](https://agentwall.io)

---

## 📄 License

Proprietary (will be open-sourced post-MVP)

---

## 🔗 Links

- **Website:** [agentwall.io](https://agentwall.io) (coming soon)
- **Docs:** [docs.agentwall.io](https://docs.agentwall.io) (coming soon)
- **Status:** [status.agentwall.io](https://status.agentwall.io) (coming soon)
- **Twitter:** [@agentwall](https://twitter.com/agentwall) (coming soon)

---

**Built with ❤️ by the AgentWall team**

*Guard the Agent, Save the Budget* 🛡️
