# Health API

Health check endpoints for monitoring AgentWall status.

## Endpoints

### Basic Health Check

```
GET https://api.agentwall.io/health
```

Returns basic health status.

**Response (200)**

```json
{
  "status": "healthy",
  "version": "1.0.0",
  "timestamp": "2026-01-06T12:00:00Z"
}
```

### Liveness Probe

```
GET https://api.agentwall.io/health/live
```

Kubernetes liveness probe. Returns 200 if the service is running.

**Response (200)**

```json
{
  "alive": true
}
```

### Readiness Probe

```
GET https://api.agentwall.io/health/ready
```

Kubernetes readiness probe. Returns 200 if all dependencies are healthy.

**Response (200)**

```json
{
  "ready": true,
  "checks": {
    "redis": {
      "status": "healthy",
      "latency_ms": 1
    },
    "clickhouse": {
      "status": "healthy"
    },
    "openai": {
      "status": "configured"
    }
  },
  "timestamp": "2026-01-06T12:00:00Z"
}
```

**Response (503 - Not Ready)**

```json
{
  "ready": false,
  "checks": {
    "redis": {
      "status": "unhealthy",
      "error": "Connection refused"
    }
  }
}
```

## Usage

### Kubernetes

```yaml
apiVersion: v1
kind: Pod
spec:
  containers:
  - name: agentwall
    livenessProbe:
      httpGet:
        path: /health/live
        port: 8000
      initialDelaySeconds: 5
      periodSeconds: 10
    readinessProbe:
      httpGet:
        path: /health/ready
        port: 8000
      initialDelaySeconds: 5
      periodSeconds: 10
```

### Docker Compose

```yaml
services:
  agentwall:
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:8000/health/ready"]
      interval: 30s
      timeout: 10s
      retries: 3
```

### Monitoring

```bash
# Check health
curl https://api.agentwall.io/health

# Check readiness with details
curl https://api.agentwall.io/health/ready | jq
```

---

**Next**: [Errors](./errors.md)
