# 🛡️ AgentWall Laravel Deployment Guide

## Prerequisites

- Server: 51.38.42.212 (Easypanel)
- Domain: agentwall.io (DNS configured)
- Docker & Docker Compose installed
- Git repository access

---

## 📋 Deployment Steps

### 1. Prepare Production Environment File

```bash
cd /opt/agentwall/laravel
cp .env.production .env
```

Edit `.env` and set:
```bash
APP_KEY=                    # Generate with: php artisan key:generate
DB_PASSWORD=                # Strong MySQL password
REDIS_PASSWORD=             # Strong Redis password (if using auth)
MAIL_PASSWORD=              # SendGrid API key
```

### 2. Generate Application Key

```bash
# If you have PHP locally
php artisan key:generate

# Or use Docker
docker run --rm -v $(pwd):/app -w /app php:8.3-cli php artisan key:generate
```

### 3. Setup MySQL Database

```bash
# Connect to MySQL
mysql -u root -p

# Create database and user
CREATE DATABASE agentwall CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
CREATE USER 'agentwall'@'localhost' IDENTIFIED BY 'your_strong_password';
GRANT ALL PRIVILEGES ON agentwall.* TO 'agentwall'@'localhost';
FLUSH PRIVILEGES;
EXIT;
```

Update `.env` with database credentials.

### 4. Run Deployment Script

```bash
cd /opt/agentwall/deploy
chmod +x laravel-deploy.sh
./laravel-deploy.sh
```

This script will:
- Pull latest code
- Build Docker image
- Start container
- Run migrations
- Optimize Laravel
- Health check

### 5. Seed Production Data (Blog Articles)

```bash
docker exec agentwall-laravel php artisan db:seed --class=ProductionSeeder
```

This will create all 20 blog articles.

### 6. Update Nginx Configuration

```bash
# Copy updated nginx config
sudo cp /opt/agentwall/deploy/nginx/agentwall.conf /etc/nginx/sites-available/agentwall.io

# Test nginx config
sudo nginx -t

# Reload nginx
sudo systemctl reload nginx
```

### 7. Setup SSL with Certbot

```bash
sudo certbot --nginx -d agentwall.io -d www.agentwall.io -d api.agentwall.io -d app.agentwall.io
```

Follow prompts to:
- Enter email
- Agree to terms
- Choose redirect HTTP to HTTPS (recommended)

### 8. Verify Deployment

Check all endpoints:

```bash
# Main website
curl https://agentwall.io

# Blog
curl https://agentwall.io/blog

# Admin panel
curl https://agentwall.io/admin

# Health check
curl https://agentwall.io/health

# API
curl https://api.agentwall.io/health
```

---

## 🔧 Post-Deployment Tasks

### Create Admin User

```bash
docker exec -it agentwall-laravel php artisan tinker
```

In tinker:
```php
$user = new App\Models\User();
$user->name = 'Admin';
$user->email = 'admin@agentwall.io';
$user->password = bcrypt('your_secure_password');
$user->save();
```

### Setup Cron for Laravel Scheduler

```bash
# Edit crontab
sudo crontab -e

# Add this line
* * * * * docker exec agentwall-laravel php artisan schedule:run >> /dev/null 2>&1
```

### Setup Log Rotation

```bash
sudo nano /etc/logrotate.d/agentwall
```

Add:
```
/opt/agentwall/laravel/storage/logs/*.log {
    daily
    missingok
    rotate 14
    compress
    delaycompress
    notifempty
    create 0640 www-data www-data
    sharedscripts
}
```

---

## 📊 Monitoring

### View Logs

```bash
# Laravel logs
docker logs -f agentwall-laravel

# Nginx logs
sudo tail -f /var/log/nginx/access.log
sudo tail -f /var/log/nginx/error.log

# Application logs
docker exec agentwall-laravel tail -f storage/logs/laravel.log
```

### Container Status

```bash
# Check if running
docker ps | grep agentwall-laravel

# Resource usage
docker stats agentwall-laravel
```

---

## 🔄 Updates & Maintenance

### Deploy Updates

```bash
cd /opt/agentwall/deploy
./laravel-deploy.sh
```

### Clear Cache

```bash
docker exec agentwall-laravel php artisan cache:clear
docker exec agentwall-laravel php artisan config:clear
docker exec agentwall-laravel php artisan route:clear
docker exec agentwall-laravel php artisan view:clear
```

### Backup Database

```bash
# Create backup
docker exec agentwall-laravel php artisan backup:run

# Or manual MySQL dump
mysqldump -u agentwall -p agentwall > backup_$(date +%Y%m%d).sql
```

---

## 🚨 Troubleshooting

### Container Won't Start

```bash
# Check logs
docker logs agentwall-laravel

# Common issues:
# - Missing .env file
# - Wrong database credentials
# - Port 8080 already in use
```

### Permission Issues

```bash
# Fix storage permissions
docker exec agentwall-laravel chown -R www-data:www-data /var/www/html/storage
docker exec agentwall-laravel chmod -R 775 /var/www/html/storage
```

### Database Connection Failed

```bash
# Test MySQL connection
mysql -u agentwall -p -h 127.0.0.1 agentwall

# Check .env credentials
docker exec agentwall-laravel cat .env | grep DB_
```

### 502 Bad Gateway

```bash
# Check if container is running
docker ps | grep agentwall-laravel

# Check nginx config
sudo nginx -t

# Check container health
curl http://localhost:8080/health
```

---

## 📁 Important Paths

```
/opt/agentwall/                     # Project root
├── laravel/                        # Laravel application
│   ├── .env                        # Production environment
│   ├── storage/                    # Logs, cache, uploads
│   └── public/                     # Public assets
├── deploy/                         # Deployment scripts
│   ├── laravel-deploy.sh          # Main deployment script
│   └── nginx/agentwall.conf       # Nginx configuration
└── docker-compose.yml             # Docker services
```

---

## 🎯 Success Checklist

- [ ] MySQL database created
- [ ] .env file configured
- [ ] APP_KEY generated
- [ ] Docker container running
- [ ] Migrations completed
- [ ] Blog articles seeded
- [ ] Nginx configured
- [ ] SSL certificates installed
- [ ] Admin user created
- [ ] Cron job configured
- [ ] All URLs accessible

---

## 🔗 URLs

- **Website:** https://agentwall.io
- **Blog:** https://agentwall.io/blog
- **Admin:** https://agentwall.io/admin
- **API:** https://api.agentwall.io
- **Docs:** https://docs.agentwall.io (coming soon)

---

**🛡️ Guard the Agent, Save the Budget**
