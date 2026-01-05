# AgentWall - Easypanel Deployment Guide

**Domain:** agentwall.io  
**Server:** 51.38.42.212  
**Platform:** Easypanel

---

## 🎯 Easypanel Avantajları

- Docker-based, docker-compose uyumlu
- Otomatik SSL (Let's Encrypt)
- Subdomain yönetimi kolay
- Zero-downtime deployment
- Built-in monitoring

---

## 📦 Servis Mimarisi (Easypanel)

```
┌─────────────────────────────────────────────────────────┐
│                    Easypanel                             │
├─────────────────────────────────────────────────────────┤
│                                                          │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐  │
│  │   FastAPI    │  │    Redis     │  │  ClickHouse  │  │
│  │   (App)      │  │  (Database)  │  │  (Database)  │  │
│  │   :8000      │  │   :6379      │  │   :8123      │  │
│  └──────────────┘  └──────────────┘  └──────────────┘  │
│         │                                               │
│         ▼                                               │
│  ┌──────────────────────────────────────────────────┐  │
│  │              Traefik (Built-in)                   │  │
│  │         api.agentwall.io → FastAPI:8000          │  │
│  │         SSL: Auto (Let's Encrypt)                │  │
│  └──────────────────────────────────────────────────┘  │
│                                                          │
└─────────────────────────────────────────────────────────┘
```

---

## 🚀 Kurulum Adımları

### 1. Easypanel'e Giriş

```
https://51.38.42.212:3000
```

### 2. Yeni Proje Oluştur

1. "Create Project" → Name: `agentwall`
2. Project oluşturulduktan sonra içine gir

### 3. Redis Servisi Ekle

1. "Add Service" → "Database" → "Redis"
2. Name: `redis`
3. Deploy

### 4. ClickHouse Servisi Ekle

1. "Add Service" → "Docker Image"
2. Name: `clickhouse`
3. Image: `clickhouse/clickhouse-server:latest`
4. Ports: `8123` (HTTP), `9000` (Native)
5. Environment Variables:
   ```
   CLICKHOUSE_DB=agentwall
   CLICKHOUSE_USER=default
   CLICKHOUSE_PASSWORD=your-secure-password
   ```
6. Volumes: `/var/lib/clickhouse` → Persistent
7. Deploy

### 5. FastAPI Servisi Ekle

1. "Add Service" → "App" → "Docker"
2. Name: `fastapi`
3. Source: GitHub repo veya Docker Image

**Option A: GitHub (Recommended)**
- Repository: `your-github-repo`
- Branch: `main`
- Dockerfile Path: `fastapi/Dockerfile`
- Build Context: `fastapi`

**Option B: Docker Image**
- Image: Build locally, push to registry
- `docker build -t your-registry/agentwall-fastapi:latest ./fastapi`
- `docker push your-registry/agentwall-fastapi:latest`

4. Environment Variables:
   ```
   DEBUG=false
   OPENAI_API_KEY=sk-your-key
   CLICKHOUSE_HOST=clickhouse
   CLICKHOUSE_PORT=9000
   CLICKHOUSE_USER=default
   CLICKHOUSE_PASSWORD=your-secure-password
   CLICKHOUSE_DATABASE=agentwall
   REDIS_URL=redis://redis:6379
   INTERNAL_SECRET=your-random-secret-32-chars
   DLP_MODE=mask
   MAX_STEPS=30
   ```

5. Domain: `api.agentwall.io`
6. Port: `8000`
7. SSL: Enable (Auto)
8. Deploy

---

## 🔧 Easypanel Service Configs (JSON)

### fastapi-service.json
```json
{
  "name": "fastapi",
  "type": "app",
  "source": {
    "type": "github",
    "repo": "your-username/agentwall",
    "branch": "main",
    "path": "fastapi"
  },
  "build": {
    "dockerfile": "Dockerfile"
  },
  "env": {
    "DEBUG": "false",
    "OPENAI_API_KEY": "{{OPENAI_API_KEY}}",
    "CLICKHOUSE_HOST": "clickhouse",
    "REDIS_URL": "redis://redis:6379",
    "INTERNAL_SECRET": "{{INTERNAL_SECRET}}"
  },
  "domains": [
    {
      "host": "api.agentwall.io",
      "port": 8000,
      "https": true
    }
  ]
}
```

---

## 🌐 Domain Yapılandırması

### Easypanel'de Domain Ekleme

1. FastAPI servisine git
2. "Domains" tab
3. "Add Domain"
4. Host: `api.agentwall.io`
5. Port: `8000`
6. HTTPS: ✅ Enable
7. Save

### DNS (Namecheap - Zaten Yapıldı ✅)

| Type | Host | Value |
|------|------|-------|
| A | @ | 51.38.42.212 |
| A | api | 51.38.42.212 |
| A | app | 51.38.42.212 |
| A | www | 51.38.42.212 |

---

## 📋 ClickHouse Schema Kurulumu

Easypanel'de ClickHouse deploy edildikten sonra:

1. ClickHouse servisine git
2. "Terminal" tab
3. Çalıştır:

```sql
-- Database oluştur
CREATE DATABASE IF NOT EXISTS agentwall;

-- Ana log tablosu
CREATE TABLE IF NOT EXISTS agentwall.request_logs (
    id UUID DEFAULT generateUUIDv4(),
    timestamp DateTime64(3) DEFAULT now64(3),
    
    -- Request identification
    run_id String,
    step_number UInt32 DEFAULT 0,
    request_id String,
    
    -- User/Team
    team_id String,
    user_id String,
    api_key_id String,
    
    -- Agent info
    agent_id String DEFAULT '',
    agent_name String DEFAULT '',
    
    -- Request details
    model String,
    provider String DEFAULT 'openai',
    endpoint String,
    method String DEFAULT 'POST',
    
    -- Content (compressed)
    request_messages String CODEC(ZSTD(3)),
    response_content String CODEC(ZSTD(3)),
    
    -- Metrics
    prompt_tokens UInt32 DEFAULT 0,
    completion_tokens UInt32 DEFAULT 0,
    total_tokens UInt32 DEFAULT 0,
    cost_usd Decimal64(8) DEFAULT 0,
    
    -- Performance
    latency_ms UInt32 DEFAULT 0,
    overhead_ms UInt32 DEFAULT 0,
    ttfb_ms UInt32 DEFAULT 0,
    
    -- Security
    dlp_triggered Bool DEFAULT false,
    dlp_action String DEFAULT '',
    dlp_patterns Array(String) DEFAULT [],
    
    -- Loop detection
    loop_detected Bool DEFAULT false,
    similarity_score Float32 DEFAULT 0,
    
    -- Status
    status_code UInt16 DEFAULT 200,
    error_message String DEFAULT '',
    
    -- Metadata
    ip_address String DEFAULT '',
    user_agent String DEFAULT '',
    metadata String DEFAULT '{}'
)
ENGINE = MergeTree()
PARTITION BY toYYYYMM(timestamp)
ORDER BY (team_id, timestamp, run_id)
TTL timestamp + INTERVAL 90 DAY
SETTINGS index_granularity = 8192;

-- Run summary tablosu
CREATE TABLE IF NOT EXISTS agentwall.run_summary (
    run_id String,
    team_id String,
    user_id String,
    agent_id String DEFAULT '',
    
    started_at DateTime64(3),
    ended_at DateTime64(3) DEFAULT now64(3),
    
    total_steps UInt32 DEFAULT 0,
    total_tokens UInt32 DEFAULT 0,
    total_cost_usd Decimal64(8) DEFAULT 0,
    total_latency_ms UInt32 DEFAULT 0,
    
    status Enum8('running' = 1, 'completed' = 2, 'failed' = 3, 'killed' = 4) DEFAULT 'running',
    kill_reason String DEFAULT '',
    
    loop_detected Bool DEFAULT false,
    dlp_triggered Bool DEFAULT false,
    budget_exceeded Bool DEFAULT false
)
ENGINE = ReplacingMergeTree(ended_at)
PARTITION BY toYYYYMM(started_at)
ORDER BY (team_id, run_id);
```

---

## ✅ Deployment Checklist

### Phase 1: Infrastructure
- [ ] Easypanel'e giriş yap
- [ ] `agentwall` projesi oluştur
- [ ] Redis servisi ekle ve deploy et
- [ ] ClickHouse servisi ekle ve deploy et
- [ ] ClickHouse schema'yı çalıştır

### Phase 2: Application
- [ ] FastAPI servisini ekle
- [ ] Environment variables ayarla
- [ ] Domain ekle: `api.agentwall.io`
- [ ] SSL aktif et
- [ ] Deploy et

### Phase 3: Verification
- [ ] Health check: `curl https://api.agentwall.io/health`
- [ ] API test: `curl https://api.agentwall.io/`
- [ ] Streaming test (OpenAI key ile)

---

## 🔍 Test Komutları

```bash
# Health check
curl https://api.agentwall.io/health

# API info
curl https://api.agentwall.io/

# Detailed health
curl https://api.agentwall.io/health/detailed

# Chat completion test (non-streaming)
curl -X POST https://api.agentwall.io/v1/chat/completions \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer your-agentwall-api-key" \
  -d '{
    "model": "gpt-4o-mini",
    "messages": [{"role": "user", "content": "Hello!"}],
    "stream": false
  }'

# Streaming test
curl -X POST https://api.agentwall.io/v1/chat/completions \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer your-agentwall-api-key" \
  -d '{
    "model": "gpt-4o-mini",
    "messages": [{"role": "user", "content": "Count to 5"}],
    "stream": true
  }'
```

---

## 🚨 Troubleshooting

### SSL Sertifikası Alınamıyor
- DNS propagation bekle (5-30 dk)
- `dig api.agentwall.io` ile kontrol et

### ClickHouse Bağlantı Hatası
- Service name doğru mu? (`clickhouse`)
- Port doğru mu? (9000 native, 8123 HTTP)
- Password ayarlandı mı?

### Redis Bağlantı Hatası
- Service name: `redis`
- URL format: `redis://redis:6379`

### FastAPI 502 Error
- Logs kontrol et (Easypanel → Logs tab)
- Environment variables kontrol et
- OPENAI_API_KEY geçerli mi?

---

## 📊 Monitoring

Easypanel built-in monitoring:
- CPU/Memory usage
- Request logs
- Container logs

Ek monitoring (opsiyonel):
- Prometheus metrics endpoint: `/metrics`
- Grafana dashboard

---

**Status:** Ready for deployment  
**ETA:** 15-30 dakika (ilk kurulum)

🛡️ Guard the Agent, Save the Budget
