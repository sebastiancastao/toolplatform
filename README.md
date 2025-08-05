# 🌟 Glass Flask - Advanced Web Scraping Application

A modern, production-ready Flask web application with elegant glass morphism UI, advanced web scraping capabilities, and Google Sheets integration.

## ✨ Features

### 🎨 **Modern UI Design**
- **Liquid Glass Morphism**: Elegant refractive glass effects and minimalistic design
- **Slim Typography**: Inter font with optimized letter-spacing
- **Responsive Design**: Mobile-first approach with Bootstrap 5
- **Dark Theme**: Beautiful gradient backgrounds with glass panels
- **Smooth Animations**: Hover effects, shimmer animations, and floating sparkles

### 🚀 **Advanced Web Scraping**
- **Robust Error Handling**: Comprehensive retry mechanisms and timeout management
- **Anti-Bot Detection**: Realistic browser headers and random delays
- **Rate Limiting**: Respectful server interactions with configurable delays
- **Session Management**: Efficient connection reuse for better performance
- **Multi-threading**: Concurrent URL processing with progress tracking

### 🔧 **Production-Ready Features**
- **Application Factory Pattern**: Scalable Flask architecture
- **Environment Configuration**: Separate configs for development/production
- **Logging System**: Rotating file logs with proper formatting
- **Docker Support**: Complete containerization with health checks
- **WSGI Ready**: Gunicorn integration for production deployment

### 📊 **Google Sheets Integration**
- **Keyword Search**: Intelligent URL content analysis
- **Real-time Progress**: Live updates during processing
- **Flexible Input**: Custom keywords or sheet-based configuration
- **Results Tracking**: Automatic updating of spreadsheet results

## 🗂️ Project Structure

```
GlassFlask/
├── 📱 Application Files
│   ├── app.py                          # Main Flask application
│   ├── config.py                       # Configuration management
│   ├── wsgi.py                        # WSGI entry point
│   └── phonic-goods-317118-*.json     # Google Sheets credentials
│
├── 🎨 Frontend
│   ├── templates/
│   │   ├── base.html                  # Glass morphism base template
│   │   ├── index.html                 # Modern homepage
│   │   ├── about.html                 # About page
│   │   └── 404.html                   # Error page
│   └── static/
│       ├── css/style.css              # Liquid glass CSS
│       └── js/main.js                 # Interactive JavaScript
│
├── 🚀 Deployment
│   ├── Dockerfile                     # Container configuration
│   ├── docker-compose.yml             # Multi-container setup
│   ├── railway.json                   # Railway deployment
│   ├── Procfile                       # Heroku configuration
│   ├── start_production.sh            # Production startup script
│   └── env.example                    # Environment template
│
├── 📋 Configuration
│   ├── requirements.txt               # Python dependencies
│   ├── .gitignore                     # Git ignore rules
│   └── README.md                      # This documentation
│
└── 📊 Runtime
    └── logs/                          # Application logs (created at runtime)
```

## 🚀 Quick Start

### Prerequisites

- **Python 3.8+** (recommended: Python 3.12)
- **pip** (Python package installer)
- **Docker** (optional, for containerized deployment)
- **Google Sheets API credentials** file

### 🔧 Local Development Setup

1. **Clone the repository**:
   ```bash
   git clone <repository-url>
   cd GlassFlask
   ```

2. **Create and activate virtual environment**:
   ```bash
   python -m venv venv
   
   # Windows
   venv\Scripts\activate
   
   # macOS/Linux
   source venv/bin/activate
   ```

3. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure environment** (copy and edit):
   ```bash
   cp env.example .env
   ```

5. **Add Google Sheets credentials**:
   - Place your `phonic-goods-317118-1353ffa1774d.json` file in the project root
   - Update `.env` with your spreadsheet ID
   - **⚠️ See [DEPLOYMENT_SECURITY.md](DEPLOYMENT_SECURITY.md) for secure credential handling**

6. **Run the application**:
   ```bash
   # Development mode
   python app.py
   
   # Production mode
   FLASK_ENV=production python app.py
   ```

7. **Access the application**:
   - Open your browser to `http://localhost:5000`
   - Enjoy the beautiful glass morphism UI! ✨
   - Windows:
     ```bash
     venv\Scripts\activate
     ```
   - macOS/Linux:
     ```bash
     source venv/bin/activate
     ```

5. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

### Running the Application

1. **Start the Flask server**:
   ```bash
   python app.py
   ```

2. **Open your browser** and navigate to:
   ```
   http://localhost:5000
   ```

3. **Explore the application**:
   - Home page with interactive features
   - About page with project information
   - Test the API endpoints using the buttons

## API Endpoints

### GET `/api/hello`
Returns a simple JSON greeting message.

**Response:**
```json
{
    "message": "Hello from Flask API!",
    "status": "success"
}
```

### POST `/api/echo`
Echoes back the JSON data sent in the request body.

**Request Body:**
```json
{
    "message": "Your message here",
    "data": "Any data"
}
```

**Response:**
```json
{
    "received": {
        "message": "Your message here",
        "data": "Any data"
    },
    "status": "success"
}
```

### POST `/api/search-keyword`
🔍 **Keyword Search Tool** - Searches for keywords in URLs from Google Sheets.

**Request Body:**
```json
{
    "use_custom": true,
    "keyword": "your search term"
}
```

**Response:**
```json
{
    "status": "success",
    "message": "Search completed! Found keyword 'test' in 3 out of 10 URLs.",
    "results": {
        "keyword": "test",
        "total_urls": 10,
        "matches_found": 3,
        "urls_with_keyword": ["https://example1.com", "https://example2.com"]
    }
}
```

**How it works:**
1. Connects to your Google Sheets using service account credentials
2. Reads URLs from column A (starting from A2)
3. Gets keyword from cell D1 or uses custom keyword
4. Scrapes each URL and searches for the keyword
5. Updates column C with URLs containing the keyword

**Requirements:**
- Google Sheets API credentials file
- URLs in column A of your spreadsheet
- Keyword in cell D1 (optional if using custom keyword)

## Development

### Configuration

The app includes several configuration options in `app.py`:

- `DEBUG = True`: Enable debug mode for development
- `SECRET_KEY`: Used for session management (change in production)
- `HOST = '0.0.0.0'`: Listen on all interfaces
- `PORT = 5000`: Default port

### Adding New Routes

To add new routes, edit `app.py`:

```python
@app.route('/new-route')
def new_route():
    return render_template('new_template.html')
```

### Customizing Styles

Edit `static/css/style.css` to customize the appearance:

```css
:root {
    --primary-color: #your-color;
}
```

### Adding JavaScript Functionality

Add new functions to `static/js/main.js`:

```javascript
function newFunction() {
    // Your code here
}
```

## 🚀 Production Deployment

### 🐳 Docker Deployment (Recommended)

#### Using Docker Compose
```bash
# Build and run
docker-compose up --build

# Run in background
docker-compose up -d

# View logs
docker-compose logs -f
```

#### Using Docker directly
```bash
# Build image
docker build -t glass-flask .

# Run container
docker run -p 5000:5000 \
  -e SECRET_KEY="your-secret-key" \
  -e SPREADSHEET_ID="your-spreadsheet-id" \
  -v $(pwd)/phonic-goods-317118-1353ffa1774d.json:/app/phonic-goods-317118-1353ffa1774d.json:ro \
  glass-flask
```

### 🌐 Platform Deployments

#### Railway
1. Connect repository to Railway
2. Set environment variables in dashboard
3. Deploy automatically on push

#### Heroku
```bash
heroku create your-app-name
heroku config:set SECRET_KEY="your-secret-key"
heroku config:set SPREADSHEET_ID="your-spreadsheet-id"
git push heroku main
```

### 🔧 Manual Production Setup

#### Using the production script:
```bash
chmod +x start_production.sh
./start_production.sh
```

#### Manual Gunicorn setup:
```bash
gunicorn --bind 0.0.0.0:5000 \
         --workers 4 \
         --timeout 60 \
         --access-logfile logs/access.log \
         --error-logfile logs/error.log \
         wsgi:application
```

### 🔐 Environment Variables

```bash
# Flask Configuration
FLASK_ENV=production
SECRET_KEY=your-super-secret-key-here

# Google Sheets Configuration
CREDENTIALS_FILE=phonic-goods-317118-1353ffa1774d.json
SPREADSHEET_ID=your-spreadsheet-id

# Performance Configuration
REQUEST_TIMEOUT=30
MAX_WORKERS=2
MIN_DELAY=1.0
MAX_DELAY=3.0
```

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## License

This project is open source and available under the [MIT License](LICENSE).

## Support

If you encounter any issues or have questions:

1. Check the console output for error messages
2. Ensure all dependencies are installed correctly
3. Verify Python version compatibility
4. Review the Flask documentation: https://flask.palletsprojects.com/

---

**Happy coding!** 🎉