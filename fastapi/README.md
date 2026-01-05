# AgentWall Proxy Engine

**Role:** The Engine - High-performance agent wall  
**Domain:** agentwall.io  
**Motto:** Guard the Agent, Save the Budget  
**Target:** <10ms overhead, streaming support, real-time DLP

---

## Architecture

```
fastapi/
├── main.py                 # FastAPI app entry point
├── config.py               # Settings (Pydantic BaseSettings)
├── dependencies.py         # Dependency injection
│
├── api/
│   ├── v1/
│   │   ├── chat.py        # /v1/chat/completions endpoint
│   │   └── health.py      # Health check endpoints
│
├── middleware/
│   ├── auth.py            # API key authentication
│   ├── dlp.py             # Data Loss Prevention
│   ├── loop_detection.py  # Loop detection pipeline
│   └── logging.py         # Request/response logging
│
├── services/
│   ├── openai_proxy.py    # OpenAI API client
│   ├── clickhouse.py      # ClickHouse log writer
│   └── redis_client.py    # Redis for rate limiting
│
├── models/
│   ├── requests.py        # Pydantic request models
│   ├── responses.py       # Pydantic response models
│   └── internal.py        # Internal data models
│
├── dlp/
│   ├── engine.py          # DLP engine
│   ├── patterns.py        # Regex patterns
│   └── validators.py      # Luhn, entropy checks
│
├── loop_detection/
│   ├── pipeline.py        # Loop detection pipeline
│   ├── step_counter.py    # Step counting
│   ├── similarity.py      # Cosine similarity
│   └── tool_frequency.py  # Tool call frequency
│
└── tests/
    ├── test_proxy.py
    ├── test_dlp.py
    └── test_loop_detection.py
```

---

## Quick Start

```bash
# Install dependencies
pip install -r requirements.txt

# Run development server
uvicorn main:app --reload --port 8000

# Run tests
pytest tests/ -v

# Run with Docker
docker-compose up fastapi
```

---

## Environment Variables

```bash
# OpenAI
OPENAI_API_KEY=sk-...

# ClickHouse
CLICKHOUSE_HOST=localhost
CLICKHOUSE_PORT=9000
CLICKHOUSE_USER=default
CLICKHOUSE_PASSWORD=

# Redis
REDIS_URL=redis://localhost:6379

# Laravel Integration
LARAVEL_URL=http://localhost:8080
INTERNAL_SECRET=your-secret-key

# Performance
MAX_STEPS=30
MAX_TOOL_CALLS=10
TIMEOUT_SECONDS=120
```

---

## Performance Targets

| Metric | Target | Current |
|--------|--------|---------|
| Proxy Overhead (non-streaming) | <10ms | TBD |
| Proxy Overhead (streaming) | <1ms/chunk | TBD |
| DLP Scan | <5ms | TBD |
| Loop Detection | <5ms | TBD |
| Memory Usage (10 streams) | <100MB | TBD |

---

## Development

```bash
# Format code
black .

# Type check
mypy .

# Lint
ruff check .

# Run specific test
pytest tests/test_proxy.py::test_streaming -v
```
