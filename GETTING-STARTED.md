# 🛡️ AgentWall - Getting Started

**Welcome to AgentWall!**  
The Wall Between Agents and Chaos.

🌐 **agentwall.io**

*Guard the Agent, Save the Budget*

---

## 🚀 Quick Start (5 Minutes)

### 1. Prerequisites

- Docker & Docker Compose
- OpenAI API Key
- Python 3.11+ (for local development)

### 2. Clone & Setup

```bash
# Clone repository
git clone https://github.com/agentwall/agentwall.git
cd agentwall

# Setup environment
make setup

# Edit .env file with your OpenAI API key
nano .env  # or vim, code, etc.
```

### 3. Start Services

```bash
# Start all services (FastAPI + Redis + ClickHouse)
make up

# Check logs
make logs
```

### 4. Test Installation

```bash
# Health check
curl http://localhost:8000/health

# Expected response:
# {"status":"healthy","timestamp":"...","version":"0.1.0"}
```

### 5. First Request

```bash
# Test proxy (replace with your AgentFirewall API key)
curl -X POST http://localhost:8000/v1/chat/completions \
  -H "Authorization: Bearer af-your-key-here" \
  -H "Content-Type: application/json" \
  -d '{
    "model": "gpt-4",
    "messages": [{"role": "user", "content": "Hello!"}]
  }'
```

---

## 📚 Project Structure

```
agentwall/
├── fastapi/                 # Proxy Engine (FastAPI)
│   ├── main.py             # Entry point
│   ├── config.py           # Configuration
│   ├── api/v1/             # API endpoints
│   ├── middleware/         # Auth, DLP, logging
│   ├── models/             # Pydantic models
│   └── tests/              # Test suite
│
├── clickhouse/             # Time-series database
│   └── init/               # Schema initialization
│
├── laravel/                # Dashboard (Coming Soon)
│
├── docs/                   # Documentation
│   ├── STRATEGIC-DECISIONS.md
│   ├── TECHNICAL-DEEP-DIVE.md
│   └── projeNameAndLogo.md
│
├── branding/               # Brand assets
│   └── LOGO.md
│
├── docker-compose.yml      # Docker services
├── Makefile               # Development commands
└── README.md              # Project overview
```

---

## 🛠️ Development Commands

### Docker

```bash
make up          # Start services
make down        # Stop services
make restart     # Restart services
make logs        # View all logs
make logs-api    # View FastAPI logs only
```

### Testing

```bash
make test        # Run tests
make test-cov    # Run tests with coverage
make lint        # Run linters
make format      # Format code
```

### Database

```bash
make db-init     # Initialize ClickHouse schema
make db-query    # Open ClickHouse client
```

### Cleanup

```bash
make clean       # Clean temporary files
make reset       # Reset all data (WARNING: destructive)
```

---

## 🔧 Configuration

### Environment Variables

Edit `.env` file:

```bash
# OpenAI
OPENAI_API_KEY=sk-your-key-here

# Agent Firewall Settings
MAX_STEPS=30                    # Max steps per run
MAX_TOOL_CALLS=10              # Max same tool calls
TIMEOUT_SECONDS=120            # Max run duration

# DLP
DLP_MODE=mask                  # block, mask, or shadow_log
DLP_ENABLED=true

# Loop Detection
SIMILARITY_THRESHOLD=0.95      # Cosine similarity threshold
```

### Custom Policies (Coming Soon)

```python
# policies/my-agent-policy.json
{
  "agent_id": "my-agent",
  "max_steps": 20,
  "max_cost": 0.50,
  "allowed_tools": ["web_search", "calculator"],
  "dlp_mode": "block"
}
```

---

## 📊 Monitoring

### Health Checks

```bash
# Basic health
curl http://localhost:8000/health

# Liveness probe (Kubernetes)
curl http://localhost:8000/health/live

# Readiness probe (Kubernetes)
curl http://localhost:8000/health/ready
```

### Metrics (Coming Soon)

```bash
# Prometheus metrics
curl http://localhost:9090/metrics
```

### Logs

```bash
# View logs
make logs

# Query ClickHouse
make db-query

# Example query:
SELECT 
    team_id,
    count() as requests,
    sum(cost_usd) as total_cost,
    countIf(is_loop_detected) as loops_detected
FROM agent_logs
WHERE date = today()
GROUP BY team_id;
```

---

## 🧪 Testing

### Run Tests

```bash
# All tests
make test

# Specific test
cd fastapi && pytest tests/test_health.py -v

# With coverage
make test-cov
```

### Manual Testing

```bash
# Test loop detection (will be killed at step 30)
curl -X POST http://localhost:8000/v1/chat/completions \
  -H "Authorization: Bearer af-test-key" \
  -H "Content-Type: application/json" \
  -d '{
    "model": "gpt-4",
    "messages": [{"role": "user", "content": "Repeat this forever"}],
    "headers": {
      "X-AgentFirewall-Run-ID": "test-loop-001"
    }
  }'

# Test DLP (will be blocked/masked)
curl -X POST http://localhost:8000/v1/chat/completions \
  -H "Authorization: Bearer af-test-key" \
  -H "Content-Type: application/json" \
  -d '{
    "model": "gpt-4",
    "messages": [{
      "role": "user",
      "content": "My API key is sk-proj-abc123..."
    }]
  }'
```

---

## 🐛 Troubleshooting

### Services won't start

```bash
# Check Docker
docker --version
docker-compose --version

# Check ports (8000, 6379, 9000 must be free)
lsof -i :8000
lsof -i :6379
lsof -i :9000

# View logs
make logs
```

### ClickHouse connection error

```bash
# Check ClickHouse is running
docker-compose ps clickhouse

# Reinitialize schema
make db-init

# Check tables
make db-query
SHOW TABLES;
```

### Tests failing

```bash
# Install dependencies
make install

# Clean cache
make clean

# Run tests with verbose output
cd fastapi && pytest tests/ -vv
```

---

## 📖 Next Steps

### Week 1 (Current)
- ✅ Project setup
- ✅ Docker Compose
- ✅ ClickHouse schema
- ✅ Basic tests
- 🚧 OpenAI proxy service
- 🚧 Streaming support

### Week 2 (Coming Soon)
- Loop detection engine
- DLP engine
- Budget tracking
- Alert system

### Week 3 (Coming Soon)
- Laravel dashboard
- User management
- API key management
- Analytics

---

## 🤝 Contributing

AgentFirewall is currently in private development. We'll open-source after MVP launch.

**Interested in early access?**  
Join our waitlist: [agentwall.io](https://agentwall.io)

---

## 📄 License

Proprietary (will be open-sourced post-MVP)

---

## 🔗 Resources

- **Documentation:** [docs/](./docs/)
- **Architecture:** [docs/TECHNICAL-DEEP-DIVE.md](./docs/TECHNICAL-DEEP-DIVE.md)
- **Branding:** [branding/LOGO.md](./branding/LOGO.md)
- **Status:** [PROJECT-STATUS.md](./PROJECT-STATUS.md)

---

## 💬 Support

- **Issues:** GitHub Issues (coming soon)
- **Email:** support@agentfirewall.ai (coming soon)
- **Discord:** [discord.gg/agentfirewall](https://discord.gg/agentfirewall) (coming soon)

---

**Built with ❤️ by the AgentWall team**

*Guard the Agent, Save the Budget* 🛡️
