# AgentWall DNS & Infrastructure Setup

**Domain:** agentwall.io  
**Server IP:** 51.38.42.212  
**Date:** 5 Ocak 2026

---

## 🌐 DNS Records (Namecheap)

### Required A Records

| Type | Host | Value | TTL | Status |
|------|------|-------|-----|--------|
| A | `@` | 51.38.42.212 | Automatic | ✅ Done |
| A | `www` | 51.38.42.212 | Automatic | ⏳ Add |
| A | `api` | 51.38.42.212 | Automatic | ⏳ Add |
| A | `app` | 51.38.42.212 | Automatic | ⏳ Add |
| A | `docs` | 51.38.42.212 | Automatic | ⏳ Add |
| A | `status` | 51.38.42.212 | Automatic | ⏳ Add |

### How to Add in Namecheap

1. Go to Advanced DNS
2. Click "ADD NEW RECORD"
3. Select Type: A Record
4. Host: `api` (or `www`, `app`, etc.)
5. Value: `51.38.42.212`
6. TTL: Automatic
7. Save

---

## 🏗️ Subdomain Architecture

| Subdomain | Purpose | Service |
|-----------|---------|---------|
| `agentwall.io` | Landing page | Nginx (static) |
| `www.agentwall.io` | Redirect to root | Nginx |
| `api.agentwall.io` | FastAPI Proxy | FastAPI :8000 |
| `app.agentwall.io` | Dashboard | Laravel :8080 |
| `docs.agentwall.io` | Documentation | Docusaurus/VitePress |
| `status.agentwall.io` | Status page | Upptime/Cachet |

---

## 🔒 SSL/TLS Setup (Let's Encrypt)

### Option 1: Certbot (Recommended)

```bash
# Install certbot
sudo apt install certbot python3-certbot-nginx

# Get certificates for all domains
sudo certbot --nginx -d agentwall.io -d www.agentwall.io -d api.agentwall.io -d app.agentwall.io -d docs.agentwall.io -d status.agentwall.io

# Auto-renewal (cron)
sudo certbot renew --dry-run
```

### Option 2: Cloudflare (Alternative)

1. Add domain to Cloudflare
2. Change nameservers to Cloudflare
3. Enable "Full (strict)" SSL mode
4. Get Origin Certificate for server

---

## 🖥️ Server Requirements

### Minimum Specs (MVP)

| Resource | Minimum | Recommended |
|----------|---------|-------------|
| CPU | 2 cores | 4 cores |
| RAM | 4 GB | 8 GB |
| Disk | 40 GB SSD | 80 GB SSD |
| OS | Ubuntu 22.04 | Ubuntu 22.04 |

### Software Requirements

```bash
# Update system
sudo apt update && sudo apt upgrade -y

# Install Docker
curl -fsSL https://get.docker.com | sh
sudo usermod -aG docker $USER

# Install Docker Compose
sudo apt install docker-compose-plugin

# Install Nginx (reverse proxy)
sudo apt install nginx

# Install Certbot (SSL)
sudo apt install certbot python3-certbot-nginx
```

---

## 📁 Server Directory Structure

```
/opt/agentwall/
├── fastapi/           # FastAPI Proxy Engine
├── laravel/           # Laravel Dashboard (Week 3)
├── clickhouse/        # ClickHouse data
├── redis/             # Redis data
├── nginx/             # Nginx configs
├── ssl/               # SSL certificates
├── logs/              # Application logs
├── backups/           # Database backups
└── docker-compose.yml
```

---

## 🚀 Deployment Checklist

### Phase 1: Server Setup

- [ ] SSH into server (51.38.42.212)
- [ ] Update system packages
- [ ] Install Docker & Docker Compose
- [ ] Install Nginx
- [ ] Install Certbot
- [ ] Create directory structure
- [ ] Clone repository

### Phase 2: DNS Setup

- [ ] Add A record for `@` ✅
- [ ] Add A record for `www`
- [ ] Add A record for `api`
- [ ] Add A record for `app`
- [ ] Add A record for `docs`
- [ ] Add A record for `status`
- [ ] Wait for DNS propagation (5-30 min)
- [ ] Verify with `dig agentwall.io`

### Phase 3: SSL Setup

- [ ] Run certbot for all domains
- [ ] Verify SSL certificates
- [ ] Setup auto-renewal

### Phase 4: Application Deployment

- [ ] Copy docker-compose.yml to server
- [ ] Create .env file
- [ ] Start services: `docker-compose up -d`
- [ ] Verify health: `curl http://localhost:8000/health`
- [ ] Configure Nginx reverse proxy
- [ ] Test: `curl https://api.agentwall.io/health`

---

## 🔧 Nginx Configuration

### /etc/nginx/sites-available/agentwall.io

```nginx
# API Subdomain (FastAPI)
server {
    listen 80;
    server_name api.agentwall.io;
    
    location / {
        proxy_pass http://localhost:8000;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection 'upgrade';
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
        proxy_cache_bypass $http_upgrade;
        
        # SSE/Streaming support
        proxy_buffering off;
        proxy_read_timeout 86400;
    }
}

# App Subdomain (Laravel Dashboard)
server {
    listen 80;
    server_name app.agentwall.io;
    
    location / {
        proxy_pass http://localhost:8080;
        proxy_http_version 1.1;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}

# Main Domain (Landing Page)
server {
    listen 80;
    server_name agentwall.io www.agentwall.io;
    
    root /var/www/agentwall;
    index index.html;
    
    location / {
        try_files $uri $uri/ =404;
    }
}
```

---

## 🔍 Verification Commands

```bash
# Check DNS propagation
dig agentwall.io
dig api.agentwall.io
nslookup agentwall.io

# Check SSL certificate
curl -vI https://api.agentwall.io

# Check API health
curl https://api.agentwall.io/health

# Check Docker services
docker-compose ps
docker-compose logs -f fastapi
```

---

## 📊 Monitoring Setup (Future)

### Uptime Monitoring
- UptimeRobot (free)
- Pingdom
- status.agentwall.io (self-hosted)

### Application Monitoring
- Prometheus + Grafana
- Sentry (error tracking)
- Datadog (APM)

---

**Status:** Ready for deployment  
**Next:** Add DNS records, then deploy
