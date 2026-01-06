#!/bin/sh
set -e

echo "🚀 AgentWall Laravel - Starting deployment..."

# Wait for database to be ready
echo "⏳ Waiting for database..."
until php artisan db:show 2>/dev/null; do
    echo "Database not ready, waiting..."
    sleep 2
done

echo "✅ Database is ready!"

# Discover packages (skipped during build)
echo "🔍 Discovering packages..."
php artisan package:discover --ansi

# Run migrations (skip if already up to date)
echo "🔄 Running migrations..."
php artisan migrate --force || echo "⚠️  Migrations failed or already up to date, continuing..."

# Clear and cache config
echo "⚙️  Optimizing application..."
php artisan config:cache
php artisan route:cache
php artisan view:cache

# Set permissions
echo "🔐 Setting permissions..."
chown -R www-data:www-data /var/www/html/storage /var/www/html/bootstrap/cache
chmod -R 775 /var/www/html/storage /var/www/html/bootstrap/cache

echo "✅ Deployment complete! Starting services..."

# Start supervisor
exec /usr/bin/supervisord -c /etc/supervisor/conf.d/supervisord.conf
