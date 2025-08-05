#!/bin/bash

# Production startup script for Glass Flask
echo "🚀 Starting Glass Flask in production mode..."

# Set production environment
export FLASK_ENV=production

# Create logs directory if it doesn't exist
mkdir -p logs

# Check if credentials file exists
if [ ! -f "phonic-goods-317118-1353ffa1774d.json" ]; then
    echo "❌ Error: Google Sheets credentials file not found!"
    echo "   Please ensure 'phonic-goods-317118-1353ffa1774d.json' is in the project root."
    exit 1
fi

# Check if environment variables are set
if [ -z "$SECRET_KEY" ]; then
    echo "⚠️  Warning: SECRET_KEY not set. Using default (not secure for production!)"
fi

# Start the application with Gunicorn
echo "🔧 Starting with Gunicorn..."
exec gunicorn \
    --bind 0.0.0.0:${PORT:-5000} \
    --workers ${WORKERS:-4} \
    --timeout 60 \
    --access-logfile logs/access.log \
    --error-logfile logs/error.log \
    --log-level info \
    wsgi:application