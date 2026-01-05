# 🛡️ AgentWall Deployment Checklist

## 📋 Pre-Deployment

### Server Setup
- [ ] Server accessible: `ssh root@51.38.42.212`
- [ ] Docker installed: `docker --version`
- [ ] Docker Compose installed: `docker-compose --version`
- [ ] Nginx installed: `nginx -v`
- [ ] Git installed: `git --version`
- [ ] Certbot installed: `certbot --version`

### DNS Configuration
- [ ] A record: `agentwall.io` → `51.38.42.212`
- [ ] A record: `www.agentwall.io` → `51.38.42.212`
- [ ] A record: `api.agentwall.io` → `51.38.42.212`
- [ ] A record: `app.agentwall.io` → `51.38.42.212`
- [ ] DNS propagated (check: `dig agentwall.io`)

### Repository
- [ ] Code pushed to main branch
- [ ] All migrations committed
- [ ] All seeders committed
- [ ] .env.production file ready

---

## 🚀 Deployment Steps

### 1. Initial Server Setup (One-time)

```bash
# Clone repository
cd /opt
git clone https://github.com/yourusername/agentwall.git
cd agentwall

# Run setup script
chmod +x deploy/setup.sh
./deploy/setup.sh
```

- [ ] Repository cloned to `/opt/agentwall`
- [ ] Setup script completed successfully
- [ ] Nginx configured

### 2. Database Setup

```bash
# Install MySQL
sudo apt install -y mysql-server

# Secure installation
sudo mysql_secure_installation

# Create database
mysql -u root -p
```

SQL commands:
```sql
CREATE DATABASE agentwall CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
CREATE USER 'agentwall'@'localhost' IDENTIFIED BY 'STRONG_PASSWORD_HERE';
GRANT ALL PRIVILEGES ON agentwall.* TO 'agentwall'@'localhost';
FLUSH PRIVILEGES;
EXIT;
```

- [ ] MySQL installed
- [ ] Database `agentwall` created
- [ ] User `agentwall` created with strong password
- [ ] Privileges granted

### 3. Laravel Environment

```bash
cd /opt/agentwall/laravel
cp .env.production .env
nano .env
```

Update these values:
```env
APP_KEY=                    # Generate: php artisan key:generate
DB_PASSWORD=                # MySQL password from step 2
REDIS_PASSWORD=             # If using Redis auth
MAIL_PASSWORD=              # SendGrid API key
```

- [ ] `.env` file created
- [ ] `APP_KEY` generated
- [ ] Database credentials set
- [ ] Mail credentials set (if available)

### 4. Deploy FastAPI

```bash
cd /opt/agentwall
docker-compose up -d fastapi redis clickhouse
```

- [ ] FastAPI container running
- [ ] Redis container running
- [ ] ClickHouse container running
- [ ] Health check passed: `curl http://localhost:8000/health`

### 5. Deploy Laravel

```bash
cd /opt/agentwall/deploy
chmod +x laravel-deploy.sh
./laravel-deploy.sh
```

- [ ] Laravel Docker image built
- [ ] Container started
- [ ] Migrations ran successfully
- [ ] Laravel optimized
- [ ] Health check passed: `curl http://localhost:8080/health`

### 6. Seed Production Data

```bash
docker exec agentwall-laravel php artisan db:seed --class=ProductionSeeder
```

- [ ] 20 blog articles seeded
- [ ] Verify: `docker exec agentwall-laravel php artisan tinker`
  - Run: `App\Models\Article::count()` (should return 20)

### 7. Setup SSL

```bash
sudo certbot --nginx \
  -d agentwall.io \
  -d www.agentwall.io \
  -d api.agentwall.io \
  -d app.agentwall.io
```

- [ ] SSL certificates obtained
- [ ] Auto-renewal configured
- [ ] HTTPS redirect enabled

### 8. Create Admin User

```bash
docker exec -it agentwall-laravel php artisan tinker
```

In tinker:
```php
$user = new App\Models\User();
$user->name = 'Admin';
$user->email = 'admin@agentwall.io';
$user->password = bcrypt('STRONG_PASSWORD_HERE');
$user->save();
```

- [ ] Admin user created
- [ ] Can login to `/admin`

### 9. Setup Cron Jobs

```bash
sudo crontab -e
```

Add:
```
* * * * * docker exec agentwall-laravel php artisan schedule:run >> /dev/null 2>&1
```

- [ ] Cron job added
- [ ] Scheduler running

---

## ✅ Post-Deployment Verification

### URLs to Test

- [ ] https://agentwall.io (Homepage)
- [ ] https://agentwall.io/blog (Blog listing)
- [ ] https://agentwall.io/blog/protecting-ai-agents-from-prompt-injection (Article)
- [ ] https://agentwall.io/about (About page)
- [ ] https://agentwall.io/contact (Contact page)
- [ ] https://agentwall.io/admin (Admin panel)
- [ ] https://api.agentwall.io/health (API health)
- [ ] https://api.agentwall.io/docs (API docs)

### Functionality Tests

- [ ] Homepage loads correctly
- [ ] Blog articles display with images
- [ ] Blog article detail pages work
- [ ] FAQs display on article pages
- [ ] Admin panel accessible
- [ ] Can login to admin
- [ ] API responds to health checks
- [ ] SSL certificates valid (no warnings)

### Performance Tests

```bash
# Test API latency
curl -w "@curl-format.txt" -o /dev/null -s https://api.agentwall.io/health

# Test Laravel response time
curl -w "@curl-format.txt" -o /dev/null -s https://agentwall.io
```

- [ ] API response < 100ms
- [ ] Laravel response < 500ms
- [ ] No 500 errors in logs

---

## 📊 Monitoring Setup

### Log Locations

```bash
# FastAPI logs
docker-compose logs -f fastapi

# Laravel logs
docker logs -f agentwall-laravel

# Nginx access logs
sudo tail -f /var/log/nginx/access.log

# Nginx error logs
sudo tail -f /var/log/nginx/error.log

# Laravel application logs
docker exec agentwall-laravel tail -f storage/logs/laravel.log
```

- [ ] Can access all logs
- [ ] No critical errors in logs

### Health Monitoring

Create `/opt/agentwall/monitor.sh`:
```bash
#!/bin/bash
curl -s https://api.agentwall.io/health || echo "API DOWN"
curl -s https://agentwall.io/health || echo "Laravel DOWN"
```

- [ ] Monitoring script created
- [ ] Consider setting up external monitoring (UptimeRobot, etc.)

---

## 🔄 Backup Setup

### Database Backup

```bash
# Create backup script
sudo nano /opt/agentwall/backup-db.sh
```

Add:
```bash
#!/bin/bash
DATE=$(date +%Y%m%d_%H%M%S)
mysqldump -u agentwall -p agentwall > /opt/backups/agentwall_$DATE.sql
find /opt/backups -name "agentwall_*.sql" -mtime +7 -delete
```

- [ ] Backup script created
- [ ] Backup directory created: `sudo mkdir -p /opt/backups`
- [ ] Cron job for daily backup added

---

## 🎯 Final Checklist

### Security
- [ ] Firewall configured (UFW)
- [ ] Only necessary ports open (80, 443, 22)
- [ ] SSH key authentication enabled
- [ ] Root login disabled
- [ ] Fail2ban installed and configured

### Performance
- [ ] OPcache enabled (Laravel)
- [ ] Redis caching working
- [ ] Static assets cached
- [ ] Gzip compression enabled

### Documentation
- [ ] Deployment documented
- [ ] Credentials stored securely (password manager)
- [ ] Team notified of deployment
- [ ] Rollback plan documented

---

## 🚨 Rollback Plan

If something goes wrong:

```bash
# Stop new containers
docker stop agentwall-laravel
docker-compose down

# Restore previous version
git checkout <previous-commit>
./deploy/quick-deploy.sh

# Restore database backup
mysql -u agentwall -p agentwall < /opt/backups/agentwall_YYYYMMDD.sql
```

- [ ] Rollback plan tested
- [ ] Database backup available
- [ ] Previous version tagged in git

---

## 📞 Support Contacts

- **Server Provider:** Easypanel
- **Domain Registrar:** [Your registrar]
- **SSL Provider:** Let's Encrypt (Certbot)
- **Email Service:** SendGrid

---

**Deployment Date:** _____________  
**Deployed By:** _____________  
**Version:** _____________

🛡️ **Guard the Agent, Save the Budget**
