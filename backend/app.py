"""
Production Flask API for Aadhaar Policy Impact Prediction System
Backend service for Render deployment
"""

# Apply compatibility fixes first
try:
    from compatibility_fix import apply_compatibility_fixes
    apply_compatibility_fixes()
except ImportError:
    # Fallback compatibility fixes
    import warnings
    warnings.filterwarnings('ignore', category=FutureWarning)
    warnings.filterwarnings('ignore', message='.*ComplexWarning.*')

import os
from flask import Flask, request, jsonify
from flask_cors import CORS
from datetime import datetime
import logging
from functools import lru_cache
import traceback

from api.routes import api_bp
from services.prediction_service import PredictionService
from services.database_service import DatabaseService
from models.model_loader import ModelLoader

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def create_app():
    """Application factory"""
    app = Flask(__name__)
    
    # Enable CORS for Vercel frontend
    CORS(app, origins=[
        "http://localhost:3000",  # Local development
        "https://*.vercel.app",   # Vercel deployments
        os.getenv("FRONTEND_URL", "")  # Production frontend
    ])
    
    # Register blueprints
    app.register_blueprint(api_bp, url_prefix='/api')
    
    # Health check endpoint (required by Render)
    @app.route('/health')
    def health_check():
        """Health check endpoint"""
        try:
            # Test database connection
            db_service = DatabaseService()
            db_status = db_service.test_connection()
            
            # Test model loading
            model_loader = ModelLoader()
            models_status = model_loader.test_models()
            
            # Get feature count
            models = model_loader.load_models()
            feature_count = len(models.get('feature_columns', []))
            
            return jsonify({
                "status": "ok",
                "database": "connected" if db_status else "disconnected",
                "models": "loaded" if models_status else "error",
                "features": feature_count,
                "timestamp": datetime.utcnow().isoformat()
            })
        except Exception as e:
            logger.error(f"Health check failed: {str(e)}")
            return jsonify({
                "status": "error",
                "error": str(e),
                "timestamp": datetime.utcnow().isoformat()
            }), 500
    
    # Root route for Render health checks and browser visits
    @app.route('/')
    def home():
        """Root endpoint for service identification"""
        return jsonify({
            "service": "Aadhaar Policy Impact Prediction API",
            "status": "running",
            "version": "1.0.0",
            "endpoints": {
                "health": "/health",
                "predict": "/api/predict",
                "states": "/api/states"
            }
        })
    
    # Global error handler
    @app.errorhandler(Exception)
    def handle_error(error):
        """Global error handler"""
        logger.error(f"Unhandled error: {str(error)}")
        logger.error(traceback.format_exc())
        
        return jsonify({
            "error": "Internal server error",
            "message": str(error) if app.debug else "An unexpected error occurred"
        }), 500
    
    return app

# Initialize services on startup
@lru_cache()
def get_prediction_service():
    """Get cached prediction service instance"""
    return PredictionService()

@lru_cache()
def get_database_service():
    """Get cached database service instance"""
    return DatabaseService()

# Create app instance
app = create_app()

if __name__ == '__main__':
    port = int(os.getenv('PORT', 10000))
    app.run(host='0.0.0.0', port=port, debug=os.getenv('FLASK_ENV') == 'development')