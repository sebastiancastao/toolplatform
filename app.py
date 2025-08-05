from flask import Flask, render_template, request, jsonify
import gspread
from google.oauth2.service_account import Credentials
import requests
from bs4 import BeautifulSoup
import os
import logging
from logging.handlers import RotatingFileHandler
from concurrent.futures import ThreadPoolExecutor
import time
import random
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry
from config import config

def create_app(config_name=None):
    """Application factory pattern"""
    if config_name is None:
        config_name = os.environ.get('FLASK_ENV', 'development')
    
    app = Flask(__name__)
    app.config.from_object(config[config_name])
    
    # Setup logging for production
    if not app.debug and not app.testing:
        # File logging
        if not os.path.exists('logs'):
            os.mkdir('logs')
        file_handler = RotatingFileHandler(
            'logs/glassflask.log', 
            maxBytes=10240000, 
            backupCount=10
        )
        file_handler.setFormatter(logging.Formatter(
            '%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]'
        ))
        file_handler.setLevel(logging.INFO)
        app.logger.addHandler(file_handler)
        
        app.logger.setLevel(logging.INFO)
        app.logger.info('Glass Flask startup')
    
    # Register routes
    register_routes(app)
    register_error_handlers(app)
    
    return app

def register_routes(app):
    """Register all application routes"""
    
    @app.route('/')
    def home():
        """Home page route"""
        return render_template('index.html')

    @app.route('/about')
    def about():
        """About page route"""
        return render_template('about.html')
    
    @app.route('/health')
    def health_check():
        """Health check endpoint for monitoring"""
        return jsonify({
            'status': 'healthy',
            'message': 'Glass Flask is running perfectly!',
            'timestamp': time.time()
        })

    @app.route('/api/hello')
    def api_hello():
        """API endpoint that returns a simple greeting"""
        return jsonify({'message': 'Hello from Flask API!', 'status': 'success'})

    @app.route('/api/echo', methods=['POST'])
    def api_echo():
        """Echo API endpoint that returns the received data"""
        data = request.get_json()
        return jsonify({'received': data, 'status': 'success'})

    @app.route('/api/search-keyword', methods=['POST'])
    def search_keyword():
        """Search for keyword in URLs from Google Sheets"""
        try:
            data = request.get_json()
            custom_keyword = data.get('keyword', '').strip()
            use_custom = data.get('use_custom', False)
            
            # Configuration from app config
            CREDENTIALS_FILE = app.config['CREDENTIALS_FILE']
            SPREADSHEET_ID = app.config['SPREADSHEET_ID']
            
            # Configure Google Sheets connection
            if not os.path.exists(CREDENTIALS_FILE):
                return jsonify({
                    'status': 'error',
                    'message': 'Google Sheets credentials file not found'
                }), 400
                
            scope = ['https://www.googleapis.com/auth/spreadsheets', 'https://www.googleapis.com/auth/drive']
            creds = Credentials.from_service_account_file(CREDENTIALS_FILE, scopes=scope)
            client = gspread.authorize(creds)
            
            # Open spreadsheet
            sheet = client.open_by_key(SPREADSHEET_ID).sheet1
            
            # Get keyword
            if use_custom and custom_keyword:
                palabra_clave = custom_keyword
            else:
                palabra_clave = sheet.acell('D1').value
                
            if not palabra_clave:
                return jsonify({
                    'status': 'error',
                    'message': 'No keyword found. Please provide a keyword or add one to cell D1 in the spreadsheet.'
                }), 400
                
            # Get URLs from column A (starting from A2)
            urls = [url for url in sheet.col_values(1)[1:] if url.strip()]
            
            if not urls:
                return jsonify({
                    'status': 'error',
                    'message': 'No URLs found in column A of the spreadsheet.'
                }), 400
                
            # Create shared session for efficient connection reuse
            session = create_session()
            
            # Search for keyword in URLs using threading for better performance
            urls_con_palabra = []
            processed_count = 0
            total_urls = len(urls)
            
            print(f'🔍 Starting search for keyword "{palabra_clave}" in {total_urls} URLs...')
            
            # Use configured max workers
            max_workers = app.config.get('MAX_WORKERS', 3)
            with ThreadPoolExecutor(max_workers=max_workers) as executor:
                # Submit all URL checks with shared session
                future_to_url = {
                    executor.submit(check_url_for_keyword, url, palabra_clave, session, app): url 
                    for url in urls
                }
                
                for future in future_to_url:
                    result = future.result()
                    processed_count += 1
                    
                    # Show progress
                    progress = (processed_count / total_urls) * 100
                    print(f'📊 Progress: {processed_count}/{total_urls} ({progress:.1f}%)')
                    
                    if result:
                        urls_con_palabra.append([result])
            
            # Clear previous results in column C
            if len(urls) > 0:
                cell_range = f'C2:C{len(urls)+1}'
                cell_list = sheet.range(cell_range)
                for cell in cell_list:
                    cell.value = ''
                sheet.update_cells(cell_list)
            
            # Update column C with URLs where keyword was found
            if urls_con_palabra:
                sheet.update(f'C2:C{len(urls_con_palabra)+1}', urls_con_palabra)
                
            # Close session
            session.close()
            
            # Create detailed response message
            success_rate = (len(urls_con_palabra) / total_urls) * 100 if total_urls > 0 else 0
            
            if len(urls_con_palabra) > 0:
                message = f'✅ Search completed successfully! Found keyword "{palabra_clave}" in {len(urls_con_palabra)} out of {total_urls} URLs ({success_rate:.1f}% match rate).'
            else:
                message = f'🔍 Search completed. Keyword "{palabra_clave}" was not found in any of the {total_urls} URLs checked.'
            
            print(f'🎉 {message}')
            
            return jsonify({
                'status': 'success',
                'message': message,
                'results': {
                    'keyword': palabra_clave,
                    'total_urls': total_urls,
                    'matches_found': len(urls_con_palabra),
                    'success_rate': round(success_rate, 1),
                    'urls_with_keyword': [url[0] for url in urls_con_palabra]
                }
            })
            
        except Exception as e:
            return jsonify({
                'status': 'error',
                'message': f'An error occurred: {str(e)}'
            }), 500

def register_error_handlers(app):
    """Register error handlers"""
    
    @app.errorhandler(404)
    def not_found(error):
        """Handle 404 errors"""
        return render_template('404.html'), 404

# Create Flask application instance (for development only)
app = create_app()

def create_session():
    """Create a robust HTTP session with retry strategy"""
    session = requests.Session()
    
    # Define retry strategy
    retry_strategy = Retry(
        total=3,  # Total number of retries
        backoff_factor=1,  # Wait time between retries
        status_forcelist=[429, 500, 502, 503, 504],  # HTTP status codes to retry
        allowed_methods=["HEAD", "GET", "OPTIONS"]  # HTTP methods to retry
    )
    
    # Mount adapter with retry strategy
    adapter = HTTPAdapter(max_retries=retry_strategy)
    session.mount("http://", adapter)
    session.mount("https://", adapter)
    
    # Set realistic headers to avoid bot detection
    session.headers.update({
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
        'Accept-Language': 'en-US,en;q=0.5',
        'Accept-Encoding': 'gzip, deflate',
        'Connection': 'keep-alive',
        'Upgrade-Insecure-Requests': '1',
    })
    
    return session

def check_url_for_keyword(url, keyword, session=None, app_instance=None):
    """Check if a keyword exists in the content of a URL with robust error handling"""
    if session is None:
        session = create_session()
    
    try:
        # Add random delay to avoid rate limiting
        if app_instance:
            min_delay = app_instance.config.get('MIN_DELAY', 0.5)
            max_delay = app_instance.config.get('MAX_DELAY', 2.0)
            timeout = app_instance.config.get('REQUEST_TIMEOUT', 15)
        else:
            min_delay, max_delay, timeout = 0.5, 2.0, 15
            
        time.sleep(random.uniform(min_delay, max_delay))
        
        # Make request with extended timeout
        response = session.get(url, timeout=timeout, allow_redirects=True)
        response.raise_for_status()
        
        # Parse content
        soup = BeautifulSoup(response.content, 'html.parser')
        
        # Remove script and style elements
        for script in soup(["script", "style"]):
            script.decompose()
            
        # Get text and clean it
        text = soup.get_text(separator=' ', strip=True).lower()
        
        # Check if keyword exists
        if keyword.lower() in text:
            print(f'✓ Keyword "{keyword}" found in: {url}')
            return url
        else:
            print(f'✗ Keyword "{keyword}" not found in: {url}')
            return None
            
    except requests.exceptions.ConnectionError as e:
        print(f'🔌 Connection error for {url}: {str(e)[:100]}...')
        return None
    except requests.exceptions.Timeout as e:
        print(f'⏰ Timeout error for {url}: {str(e)[:100]}...')
        return None
    except requests.exceptions.HTTPError as e:
        if e.response.status_code == 403:
            print(f'🚫 Access forbidden (403) for {url}')
        elif e.response.status_code == 404:
            print(f'📄 Page not found (404) for {url}')
        else:
            print(f'🌐 HTTP error {e.response.status_code} for {url}')
        return None
    except requests.exceptions.RequestException as e:
        print(f'🚨 Request error for {url}: {str(e)[:100]}...')
        return None
    except Exception as e:
        print(f'❌ Unexpected error for {url}: {str(e)[:100]}...')
        return None

# Development server entry point

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    host = os.environ.get('HOST', '0.0.0.0')
    app.run(debug=app.config['DEBUG'], host=host, port=port)