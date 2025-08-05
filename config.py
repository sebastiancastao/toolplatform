"""
Configuration settings for Flask application
"""
import os
from pathlib import Path

class Config:
    """Base configuration class"""
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'dev-secret-key-change-in-production'
    
    # Google Sheets configuration
    CREDENTIALS_FILE = os.environ.get('CREDENTIALS_FILE') or 'phonic-goods-317118-1353ffa1774d.json'
    SPREADSHEET_ID = os.environ.get('SPREADSHEET_ID') or '1BJpXRY7WZ7K0IE7sOpXSC-0-k7cBk1Z-w8PqbdxJvpY'
    
    # Request settings
    REQUEST_TIMEOUT = int(os.environ.get('REQUEST_TIMEOUT', 15))
    MAX_WORKERS = int(os.environ.get('MAX_WORKERS', 3))
    
    # Rate limiting
    MIN_DELAY = float(os.environ.get('MIN_DELAY', 0.5))
    MAX_DELAY = float(os.environ.get('MAX_DELAY', 2.0))
    
class DevelopmentConfig(Config):
    """Development configuration"""
    DEBUG = True
    TESTING = False

class ProductionConfig(Config):
    """Production configuration"""
    DEBUG = False
    TESTING = False
    
    # Production-specific settings
    REQUEST_TIMEOUT = int(os.environ.get('REQUEST_TIMEOUT', 30))
    MAX_WORKERS = int(os.environ.get('MAX_WORKERS', 2))  # Conservative for production
    
    # Security headers
    SEND_FILE_MAX_AGE_DEFAULT = 31536000  # 1 year
    
class TestingConfig(Config):
    """Testing configuration"""
    DEBUG = True
    TESTING = True
    WTF_CSRF_ENABLED = False

# Configuration dictionary
config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'testing': TestingConfig,
    'default': DevelopmentConfig
}