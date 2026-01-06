#!/bin/bash

echo "=== Filament Asset Diagnostics ==="
echo ""

echo "1. Checking Filament CSS files..."
ls -lh /var/www/html/public/css/filament/filament/ 2>/dev/null || echo "❌ Directory not found"
echo ""

echo "2. Checking app.css size and first 20 lines..."
if [ -f "/var/www/html/public/css/filament/filament/app.css" ]; then
    ls -lh /var/www/html/public/css/filament/filament/app.css
    echo "First 20 lines:"
    head -20 /var/www/html/public/css/filament/filament/app.css
else
    echo "❌ app.css not found"
fi
echo ""

echo "3. Checking Filament JS files..."
ls -lh /var/www/html/public/js/filament/filament/ 2>/dev/null || echo "❌ Directory not found"
echo ""

echo "4. Running Filament commands..."
php artisan optimize:clear
php artisan config:cache
php artisan route:cache
php artisan view:cache
php artisan filament:assets
echo ""

echo "5. Checking permissions..."
ls -la /var/www/html/public/css/filament/ 2>/dev/null || echo "❌ Directory not found"
echo ""

echo "6. Checking if Filament is properly installed..."
php artisan about | grep -i filament
echo ""

echo "=== Diagnostics Complete ==="
