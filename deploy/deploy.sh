#!/bin/bash

# ============================================
# AgentWall Deployment Script
# Domain: agentwall.io
# ============================================

set -e

echo "🛡️ AgentWall Deployment"
echo "   agentwall.io"
echo ""

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m'

DEPLOY_DIR="/opt/agentwall"

# ============================================
# 1. Pull Latest Code
# ============================================
echo -e "${YELLOW}[1/5] Pulling latest code...${NC}"
cd $DEPLOY_DIR
git pull origin main
echo -e "${GREEN}Code updated!${NC}"

# ============================================
# 2. Build Docker Images
# ============================================
echo -e "${YELLOW}[2/5] Building Docker images...${NC}"
docker-compose build --no-cache
echo -e "${GREEN}Images built!${NC}"

# ============================================
# 3. Stop Old Containers
# ============================================
echo -e "${YELLOW}[3/5] Stopping old containers...${NC}"
docker-compose down
echo -e "${GREEN}Containers stopped!${NC}"

# ============================================
# 4. Start New Containers
# ============================================
echo -e "${YELLOW}[4/5] Starting new containers...${NC}"
docker-compose up -d
echo -e "${GREEN}Containers started!${NC}"

# ============================================
# 5. Health Check
# ============================================
echo -e "${YELLOW}[5/5] Running health check...${NC}"
sleep 5  # Wait for services to start

if curl -s http://localhost:8000/health | grep -q "healthy"; then
    echo -e "${GREEN}✅ API is healthy!${NC}"
else
    echo -e "${RED}❌ API health check failed!${NC}"
    docker-compose logs fastapi
    exit 1
fi

# ============================================
# Done!
# ============================================
echo ""
echo -e "${GREEN}✅ Deployment complete!${NC}"
echo ""
echo "Services:"
echo "  - API: https://api.agentwall.io"
echo "  - App: https://app.agentwall.io (coming soon)"
echo ""
echo "Commands:"
echo "  - Logs: docker-compose logs -f"
echo "  - Status: docker-compose ps"
echo "  - Restart: docker-compose restart"
echo ""
echo "🛡️ Guard the Agent, Save the Budget"
