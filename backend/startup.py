#!/usr/bin/env python3
"""
Startup script for backend initialization
Ensures models are loaded and validated before serving requests
"""

import os
import sys
import logging
from models.model_loader import ModelLoader
from services.database_service import DatabaseService

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

def ensure_feature_columns():
    """Ensure feature columns file exists"""
    logger.info("Checking feature columns file...")
    
    try:
        from create_feature_cols import create_feature_columns
        feature_columns = create_feature_columns()
        logger.info(f"Feature columns ready: {len(feature_columns)} features")
        return True
    except Exception as e:
        logger.error(f"Failed to ensure feature columns: {str(e)}")
        return False

def initialize_models():
    """Initialize and validate models"""
    logger.info("Initializing ML models...")
    
    try:
        model_loader = ModelLoader()
        models = model_loader.load_models()
        
        feature_count = len(models['feature_columns'])
        logger.info(f"Models loaded successfully")
        logger.info(f"Feature columns count: {feature_count}")
        
        # Test models
        test_result = model_loader.test_models()
        if test_result:
            logger.info("Model validation passed")
        else:
            logger.warning("Model validation failed - using fallback models")
        
        return True
        
    except Exception as e:
        logger.error(f"Model initialization failed: {str(e)}")
        return False

def initialize_database():
    """Initialize database connection"""
    logger.info("Initializing database connection...")
    
    try:
        db_service = DatabaseService()
        connection_status = db_service.test_connection()
        
        if connection_status:
            logger.info("Database connection successful")
        else:
            logger.warning("Database connection failed - predictions will not be stored")
        
        return True
        
    except Exception as e:
        logger.error(f"Database initialization failed: {str(e)}")
        return False

def startup_checks():
    """Run all startup checks"""
    logger.info("=== Backend Startup Checks ===")
    
    # Check environment variables
    required_env_vars = ['MODEL_PATH', 'DATA_PATH']
    for var in required_env_vars:
        value = os.getenv(var)
        if value:
            logger.info(f"{var}: {value}")
        else:
            logger.warning(f"{var}: not set (using default)")
    
    # Initialize components
    feature_status = ensure_feature_columns()
    model_status = initialize_models()
    db_status = initialize_database()
    
    if feature_status and model_status:
        logger.info("✓ Startup completed successfully")
        return True
    else:
        logger.error("✗ Startup failed")
        return False

if __name__ == "__main__":
    success = startup_checks()
    sys.exit(0 if success else 1)