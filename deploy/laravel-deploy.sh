#!/bin/bash

# ============================================
# AgentWall Laravel Deployment Script
# Domain: agentwall.io
# ============================================

set -e

echo "🛡️ AgentWall Laravel Deployment"
echo "   agentwall.io"
echo ""

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

DEPLOY_DIR="/opt/agentwall"
LARAVEL_DIR="$DEPLOY_DIR/laravel"

# ============================================
# 1. Pull Latest Code
# ============================================
echo -e "${YELLOW}[1/8] Pulling latest code...${NC}"
cd $DEPLOY_DIR
git pull origin main
echo -e "${GREEN}✓ Code updated${NC}"

# ============================================
# 2. Build Laravel Docker Image
# ============================================
echo -e "${YELLOW}[2/8] Building Laravel Docker image...${NC}"
cd $LARAVEL_DIR
docker build -t agentwall-laravel:latest .
echo -e "${GREEN}✓ Image built${NC}"

# ============================================
# 3. Stop Old Container
# ============================================
echo -e "${YELLOW}[3/8] Stopping old container...${NC}"
docker stop agentwall-laravel 2>/dev/null || true
docker rm agentwall-laravel 2>/dev/null || true
echo -e "${GREEN}✓ Old container removed${NC}"

# ============================================
# 4. Start New Container
# ============================================
echo -e "${YELLOW}[4/8] Starting new container...${NC}"
docker run -d \
  --name agentwall-laravel \
  --restart unless-stopped \
  -p 8080:80 \
  --env-file $LARAVEL_DIR/.env \
  -v $LARAVEL_DIR/storage:/var/www/html/storage \
  -v $LARAVEL_DIR/bootstrap/cache:/var/www/html/bootstrap/cache \
  agentwall-laravel:latest

echo -e "${GREEN}✓ Container started${NC}"

# ============================================
# 5. Wait for Container
# ============================================
echo -e "${YELLOW}[5/8] Waiting for container to be ready...${NC}"
sleep 5

# ============================================
# 6. Run Migrations
# ============================================
echo -e "${YELLOW}[6/8] Running database migrations...${NC}"
docker exec agentwall-laravel php artisan migrate --force
echo -e "${GREEN}✓ Migrations completed${NC}"

# ============================================
# 7. Optimize Laravel
# ============================================
echo -e "${YELLOW}[7/8] Optimizing Laravel...${NC}"
docker exec agentwall-laravel php artisan config:cache
docker exec agentwall-laravel php artisan route:cache
docker exec agentwall-laravel php artisan view:cache
docker exec agentwall-laravel php artisan event:cache
echo -e "${GREEN}✓ Laravel optimized${NC}"

# ============================================
# 8. Health Check
# ============================================
echo -e "${YELLOW}[8/8] Running health check...${NC}"
sleep 3

if curl -s http://localhost:8080/health | grep -q "healthy"; then
    echo -e "${GREEN}✅ Laravel is healthy!${NC}"
else
    echo -e "${RED}❌ Health check failed!${NC}"
    docker logs agentwall-laravel --tail 50
    exit 1
fi

# ============================================
# Done!
# ============================================
echo ""
echo -e "${GREEN}✅ Laravel deployment complete!${NC}"
echo ""
echo -e "${BLUE}Services:${NC}"
echo "  - Website: https://agentwall.io"
echo "  - Admin: https://agentwall.io/admin"
echo "  - Blog: https://agentwall.io/blog"
echo ""
echo -e "${BLUE}Commands:${NC}"
echo "  - Logs: docker logs -f agentwall-laravel"
echo "  - Shell: docker exec -it agentwall-laravel sh"
echo "  - Artisan: docker exec agentwall-laravel php artisan [command]"
echo ""
echo "🛡️ Guard the Agent, Save the Budget"
