#!/bin/bash

# ============================================
# AgentWall Server Setup Script
# Domain: agentwall.io
# Server: 51.38.42.212
# ============================================

set -e  # Exit on error

echo "🛡️ AgentWall Server Setup"
echo "   agentwall.io"
echo ""

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# ============================================
# 1. System Update
# ============================================
echo -e "${YELLOW}[1/7] Updating system...${NC}"
sudo apt update && sudo apt upgrade -y

# ============================================
# 2. Install Docker
# ============================================
echo -e "${YELLOW}[2/7] Installing Docker...${NC}"
if ! command -v docker &> /dev/null; then
    curl -fsSL https://get.docker.com | sh
    sudo usermod -aG docker $USER
    echo -e "${GREEN}Docker installed!${NC}"
else
    echo -e "${GREEN}Docker already installed.${NC}"
fi

# ============================================
# 3. Install Docker Compose
# ============================================
echo -e "${YELLOW}[3/7] Installing Docker Compose...${NC}"
if ! command -v docker-compose &> /dev/null; then
    sudo apt install -y docker-compose-plugin
    echo -e "${GREEN}Docker Compose installed!${NC}"
else
    echo -e "${GREEN}Docker Compose already installed.${NC}"
fi

# ============================================
# 4. Install Nginx
# ============================================
echo -e "${YELLOW}[4/7] Installing Nginx...${NC}"
if ! command -v nginx &> /dev/null; then
    sudo apt install -y nginx
    sudo systemctl enable nginx
    sudo systemctl start nginx
    echo -e "${GREEN}Nginx installed!${NC}"
else
    echo -e "${GREEN}Nginx already installed.${NC}"
fi

# ============================================
# 5. Install Certbot (SSL)
# ============================================
echo -e "${YELLOW}[5/7] Installing Certbot...${NC}"
if ! command -v certbot &> /dev/null; then
    sudo apt install -y certbot python3-certbot-nginx
    echo -e "${GREEN}Certbot installed!${NC}"
else
    echo -e "${GREEN}Certbot already installed.${NC}"
fi

# ============================================
# 6. Create Directory Structure
# ============================================
echo -e "${YELLOW}[6/7] Creating directory structure...${NC}"
sudo mkdir -p /opt/agentwall
sudo mkdir -p /var/www/agentwall
sudo mkdir -p /var/www/agentwall-docs
sudo mkdir -p /var/www/agentwall-status
sudo chown -R $USER:$USER /opt/agentwall
echo -e "${GREEN}Directories created!${NC}"

# ============================================
# 7. Setup Nginx Config
# ============================================
echo -e "${YELLOW}[7/7] Setting up Nginx...${NC}"
sudo cp deploy/nginx/agentwall.conf /etc/nginx/sites-available/agentwall.io
sudo ln -sf /etc/nginx/sites-available/agentwall.io /etc/nginx/sites-enabled/
sudo nginx -t && sudo systemctl reload nginx
echo -e "${GREEN}Nginx configured!${NC}"

# ============================================
# Done!
# ============================================
echo ""
echo -e "${GREEN}✅ Server setup complete!${NC}"
echo ""
echo "Next steps:"
echo "1. Add DNS records for subdomains"
echo "2. Run: cd /opt/agentwall && docker-compose up -d"
echo "3. Run: sudo certbot --nginx -d agentwall.io -d api.agentwall.io -d app.agentwall.io"
echo ""
echo "🛡️ Guard the Agent, Save the Budget"
