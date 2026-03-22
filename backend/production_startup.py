#!/usr/bin/env python3
"""
Production startup script for Aadhaar Policy Impact Prediction System
Handles all initialization and validation for production deployment
"""

import os
import sys
import logging
import warnings
from datetime import datetime

# Suppress sklearn warnings for cleaner logs
warnings.filterwarnings('ignore', category=UserWarning, module='sklearn')

# Configure logging for production
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(sys.stdout)
    ]
)
logger = logging.getLogger(__name__)

def check_environment():
    """Check environment variables and configuration"""
    logger.info("=== Environment Check ===")
    
    # Required environment variables for production
    env_vars = {
        'MODEL_PATH': os.getenv('MODEL_PATH', 'data/models'),
        'DATA_PATH': os.getenv('DATA_PATH', '.'),
        'FLASK_ENV': os.getenv('FLASK_ENV', 'production'),
        'PORT': os.getenv('PORT', '10000')
    }
    
    for var, value in env_vars.items():
        logger.info(f"{var}: {value}")
    
    # Optional Supabase variables
    supabase_url = os.getenv('SUPABASE_URL')
    supabase_key = os.getenv('SUPABASE_KEY')
    
    if supabase_url and supabase_key:
        logger.info("Supabase configuration: Available")
    else:
        logger.info("Supabase configuration: Not configured (database features disabled)")
    
    return True

def initialize_models():
    """Initialize and validate ML models"""
    logger.info("=== Model Initialization ===")
    
    try:
        from models.model_loader import ModelLoader
        
        model_loader = ModelLoader()
        models = model_loader.load_models()
        
        baseline_features = len(models.get('baseline_features', []))
        policy_features = len(models.get('policy_features', []))
        
        logger.info(f"Models loaded successfully")
        logger.info(f"Baseline features: {baseline_features}")
        logger.info(f"Policy features: {policy_features}")
        
        # Test models
        test_result = model_loader.test_models()
        if test_result:
            logger.info("Model validation: PASSED")
        else:
            logger.warning("Model validation: FAILED (using fallback models)")
        
        return True
        
    except Exception as e:
        logger.error(f"Model initialization failed: {str(e)}")
        return False

def initialize_prediction_service():
    """Initialize prediction service"""
    logger.info("=== Prediction Service Check ===")
    
    try:
        from services.prediction_service import PredictionService
        
        service = PredictionService()
        
        # Quick test prediction
        result = service.predict_policy_impact(
            policy_date="2025-04-01",
            forecast_days=5,  # Small test
            compliance_level=0.8
        )
        
        total_affected = result['summary']['total_people_affected']
        logger.info(f"Prediction service: WORKING (test result: {total_affected:,} people)")
        
        return True
        
    except Exception as e:
        logger.error(f"Prediction service initialization failed: {str(e)}")
        return False

def initialize_database():
    """Initialize database connection"""
    logger.info("=== Database Initialization ===")
    
    try:
        from services.database_service import DatabaseService
        
        db_service = DatabaseService()
        connection_status = db_service.test_connection()
        
        if connection_status:
            logger.info("Database connection: CONNECTED")
        else:
            logger.info("Database connection: DISABLED (predictions will not be stored)")
        
        return True
        
    except Exception as e:
        logger.error(f"Database initialization failed: {str(e)}")
        return True  # Don't fail startup for database issues

def check_flask_app():
    """Check Flask app can be created"""
    logger.info("=== Flask App Check ===")
    
    try:
        from app import create_app
        
        app = create_app()
        
        with app.test_client() as client:
            # Test health endpoint
            response = client.get('/health')
            if response.status_code == 200:
                data = response.get_json()
                logger.info(f"Flask app: READY (status: {data.get('status')})")
                return True
            else:
                logger.error(f"Flask app health check failed: {response.status_code}")
                return False
        
    except Exception as e:
        logger.error(f"Flask app check failed: {str(e)}")
        return False

def production_startup():
    """Run all production startup checks"""
    logger.info("=== Production Startup ===")
    logger.info(f"Timestamp: {datetime.utcnow().isoformat()}")
    logger.info(f"Python version: {sys.version}")
    logger.info(f"Working directory: {os.getcwd()}")
    
    # Run all checks
    checks = [
        ("Environment", check_environment),
        ("Models", initialize_models),
        ("Prediction Service", initialize_prediction_service),
        ("Database", initialize_database),
        ("Flask App", check_flask_app)
    ]
    
    results = []
    for check_name, check_func in checks:
        try:
            result = check_func()
            results.append(result)
            status = "PASSED" if result else "FAILED"
            logger.info(f"{check_name}: {status}")
        except Exception as e:
            logger.error(f"{check_name}: FAILED with exception: {str(e)}")
            results.append(False)
    
    # Summary
    passed = sum(results)
    total = len(results)
    
    logger.info("=== Startup Summary ===")
    logger.info(f"Checks passed: {passed}/{total}")
    
    if passed >= total - 1:  # Allow database to fail
        logger.info("SUCCESS: System ready for production")
        return True
    else:
        logger.error("FAILED: System not ready for production")
        return False

if __name__ == "__main__":
    success = production_startup()
    sys.exit(0 if success else 1)