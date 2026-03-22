"""
Configuration settings for Aadhaar Policy Impact Prediction System
"""

import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

class Config:
    """Base configuration"""
    
    # Flask settings
    SECRET_KEY = os.getenv('SECRET_KEY', 'dev-secret-key-change-in-production')
    FLASK_ENV = os.getenv('FLASK_ENV', 'production')
    DEBUG = FLASK_ENV == 'development'
    
    # Server settings
    HOST = os.getenv('HOST', '0.0.0.0')
    PORT = int(os.getenv('PORT', 10000))
    
    # Database settings (Supabase)
    SUPABASE_URL = os.getenv('SUPABASE_URL')
    SUPABASE_KEY = os.getenv('SUPABASE_KEY')
    
    # Model and data paths
    MODEL_PATH = os.getenv('MODEL_PATH', 'data/models')
    DATA_PATH = os.getenv('DATA_PATH', '.')
    
    # CORS settings
    FRONTEND_URL = os.getenv('FRONTEND_URL', 'https://aadhaar-policy-frontend.vercel.app')
    CORS_ORIGINS = [
        'http://localhost:3000',  # Local development
        'https://*.vercel.app',   # Vercel deployments
        FRONTEND_URL
    ]
    
    # API settings
    MAX_FORECAST_DAYS = int(os.getenv('MAX_FORECAST_DAYS', 365))
    DEFAULT_FORECAST_DAYS = int(os.getenv('DEFAULT_FORECAST_DAYS', 60))
    
    # Logging settings
    LOG_LEVEL = os.getenv('LOG_LEVEL', 'INFO')
    
    # Cache settings
    CACHE_TIMEOUT = int(os.getenv('CACHE_TIMEOUT', 3600))  # 1 hour
    
    # Rate limiting (requests per minute)
    RATE_LIMIT = int(os.getenv('RATE_LIMIT', 60))

class DevelopmentConfig(Config):
    """Development configuration"""
    DEBUG = True
    FLASK_ENV = 'development'
    LOG_LEVEL = 'DEBUG'

class ProductionConfig(Config):
    """Production configuration"""
    DEBUG = False
    FLASK_ENV = 'production'
    
    # Ensure required environment variables are set
    @classmethod
    def validate(cls):
        """Validate production configuration"""
        required_vars = ['SUPABASE_URL', 'SUPABASE_KEY']
        missing_vars = [var for var in required_vars if not os.getenv(var)]
        
        if missing_vars:
            raise ValueError(f"Missing required environment variables: {', '.join(missing_vars)}")

class TestingConfig(Config):
    """Testing configuration"""
    TESTING = True
    DEBUG = True
    
    # Use in-memory database for testing
    SUPABASE_URL = None
    SUPABASE_KEY = None

# Configuration mapping
config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'testing': TestingConfig,
    'default': DevelopmentConfig
}

def get_config():
    """Get configuration based on environment"""
    env = os.getenv('FLASK_ENV', 'development')
    return config.get(env, config['default'])