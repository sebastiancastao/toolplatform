# Production startup script for Glass Flask (Windows PowerShell)
Write-Host "🚀 Starting Glass Flask in production mode..." -ForegroundColor Green

# Set production environment
$env:FLASK_ENV = "production"

# Create logs directory if it doesn't exist
if (-not (Test-Path "logs")) {
    New-Item -ItemType Directory -Path "logs"
    Write-Host "📁 Created logs directory" -ForegroundColor Yellow
}

# Check if credentials file exists
if (-not (Test-Path "phonic-goods-317118-1353ffa1774d.json")) {
    Write-Host "❌ Error: Google Sheets credentials file not found!" -ForegroundColor Red
    Write-Host "   Please ensure 'phonic-goods-317118-1353ffa1774d.json' is in the project root." -ForegroundColor Red
    exit 1
}

# Check if environment variables are set
if (-not $env:SECRET_KEY) {
    Write-Host "⚠️  Warning: SECRET_KEY not set. Using default (not secure for production!)" -ForegroundColor Yellow
}

# Start the application with Gunicorn
Write-Host "🔧 Starting with Gunicorn..." -ForegroundColor Blue

$port = if ($env:PORT) { $env:PORT } else { "5000" }
$workers = if ($env:WORKERS) { $env:WORKERS } else { "4" }

gunicorn `
    --bind "0.0.0.0:$port" `
    --workers $workers `
    --timeout 60 `
    --access-logfile "logs/access.log" `
    --error-logfile "logs/error.log" `
    --log-level info `
    wsgi:application