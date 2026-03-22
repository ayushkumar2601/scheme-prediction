#!/usr/bin/env python3
"""
Simple test to check if the backend works
Run this from the backend directory
"""

import sys
import os

def test_imports():
    """Test if we can import the modules"""
    try:
        from models.model_loader import ModelLoader
        print("✓ Can import ModelLoader")
        
        from services.prediction_service import PredictionService  
        print("✓ Can import PredictionService")
        
        from flask_cors import CORS
        print("✓ Can import flask-cors")
        
        return True
    except Exception as e:
        print(f"✗ Import failed: {e}")
        return False

def test_model_loading():
    """Test model loading"""
    try:
        from models.model_loader import ModelLoader
        
        loader = ModelLoader()
        models = loader.load_models()
        
        feature_count = len(models['feature_columns'])
        print(f"✓ Models loaded with {feature_count} features")
        
        # Show first few features
        features = models['feature_columns'][:5]
        print(f"✓ First 5 features: {features}")
        
        return True
    except Exception as e:
        print(f"✗ Model loading failed: {e}")
        return False

def main():
    print("=== Simple Backend Test ===")
    
    import_ok = test_imports()
    if not import_ok:
        return False
        
    model_ok = test_model_loading()
    if not model_ok:
        return False
        
    print("✓ Basic tests passed!")
    return True

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)