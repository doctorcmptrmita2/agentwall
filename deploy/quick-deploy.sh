#!/bin/bash

# ============================================
# AgentWall Quick Deployment Script
# Deploys both FastAPI and Laravel
# ============================================

set -e

echo "🛡️ AgentWall Full Stack Deployment"
echo "   agentwall.io"
echo ""

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

# ============================================
# Pre-flight Checks
# ============================================
echo -e "${BLUE}Running pre-flight checks...${NC}"

# Check if running as root or with sudo
if [ "$EUID" -ne 0 ] && ! sudo -n true 2>/dev/null; then
    echo -e "${RED}❌ This script requires sudo privileges${NC}"
    exit 1
fi

# Check if Docker is installed
if ! command -v docker &> /dev/null; then
    echo -e "${RED}❌ Docker is not installed${NC}"
    exit 1
fi

# Check if in correct directory
if [ ! -f "docker-compose.yml" ]; then
    echo -e "${RED}❌ Please run this script from /opt/agentwall directory${NC}"
    exit 1
fi

echo -e "${GREEN}✓ Pre-flight checks passed${NC}"
echo ""

# ============================================
# 1. Deploy FastAPI (API Engine)
# ============================================
echo -e "${YELLOW}[1/3] Deploying FastAPI...${NC}"
cd /opt/agentwall

# Pull latest code
git pull origin main

# Build and start FastAPI
docker-compose up -d fastapi redis clickhouse

# Wait for services
sleep 5

# Health check
if curl -s http://localhost:8000/health | grep -q "healthy"; then
    echo -e "${GREEN}✓ FastAPI deployed successfully${NC}"
else
    echo -e "${RED}❌ FastAPI health check failed${NC}"
    docker-compose logs fastapi
    exit 1
fi

# ============================================
# 2. Deploy Laravel (Dashboard)
# ============================================
echo -e "${YELLOW}[2/3] Deploying Laravel...${NC}"
cd /opt/agentwall/deploy
chmod +x laravel-deploy.sh
./laravel-deploy.sh

# ============================================
# 3. Update Nginx & SSL
# ============================================
echo -e "${YELLOW}[3/3] Updating Nginx configuration...${NC}"

# Copy nginx config
sudo cp /opt/agentwall/deploy/nginx/agentwall.conf /etc/nginx/sites-available/agentwall.io

# Create symlink if doesn't exist
if [ ! -L /etc/nginx/sites-enabled/agentwall.io ]; then
    sudo ln -s /etc/nginx/sites-available/agentwall.io /etc/nginx/sites-enabled/
fi

# Test nginx config
if sudo nginx -t; then
    sudo systemctl reload nginx
    echo -e "${GREEN}✓ Nginx reloaded${NC}"
else
    echo -e "${RED}❌ Nginx configuration error${NC}"
    exit 1
fi

# ============================================
# Final Health Checks
# ============================================
echo ""
echo -e "${BLUE}Running final health checks...${NC}"

# Check FastAPI
if curl -s http://localhost:8000/health | grep -q "healthy"; then
    echo -e "${GREEN}✓ FastAPI: healthy${NC}"
else
    echo -e "${RED}✗ FastAPI: unhealthy${NC}"
fi

# Check Laravel
if curl -s http://localhost:8080/health | grep -q "healthy"; then
    echo -e "${GREEN}✓ Laravel: healthy${NC}"
else
    echo -e "${RED}✗ Laravel: unhealthy${NC}"
fi

# Check Nginx
if curl -s -o /dev/null -w "%{http_code}" http://localhost | grep -q "200\|301\|302"; then
    echo -e "${GREEN}✓ Nginx: healthy${NC}"
else
    echo -e "${RED}✗ Nginx: unhealthy${NC}"
fi

# ============================================
# Done!
# ============================================
echo ""
echo -e "${GREEN}✅ Full stack deployment complete!${NC}"
echo ""
echo -e "${BLUE}Services:${NC}"
echo "  - Website: https://agentwall.io"
echo "  - Blog: https://agentwall.io/blog"
echo "  - Admin: https://agentwall.io/admin"
echo "  - API: https://api.agentwall.io"
echo ""
echo -e "${BLUE}Next steps:${NC}"
echo "  1. Setup SSL: sudo certbot --nginx -d agentwall.io -d api.agentwall.io"
echo "  2. Seed blog data: docker exec agentwall-laravel php artisan db:seed --class=ProductionSeeder"
echo "  3. Create admin user: docker exec -it agentwall-laravel php artisan tinker"
echo ""
echo -e "${BLUE}Monitoring:${NC}"
echo "  - FastAPI logs: docker-compose logs -f fastapi"
echo "  - Laravel logs: docker logs -f agentwall-laravel"
echo "  - Nginx logs: sudo tail -f /var/log/nginx/access.log"
echo ""
echo "🛡️ Guard the Agent, Save the Budget"
