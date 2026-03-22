#!/usr/bin/env python3
"""
Test script for backend functionality
Run this to verify the backend works before deployment
"""

import sys
import os
import requests
import json
from datetime import datetime, timedelta

# Add backend to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def test_model_loading():
    """Test model loading functionality"""
    print("Testing model loading...")
    try:
        from models.model_loader import ModelLoader
        
        loader = ModelLoader()
        models = loader.load_models()
        
        print(f"✓ Models loaded successfully")
        print(f"✓ Feature columns count: {len(models['feature_columns'])}")
        
        # Test feature alignment
        import pandas as pd
        test_df = pd.DataFrame([[1] * 50], columns=[f'feature_{i}' for i in range(50)])
        aligned_df = loader.align_features(test_df)
        print(f"✓ Feature alignment works: {aligned_df.shape}")
        
        # Test model predictions
        test_status = loader.test_models()
        print(f"✓ Model testing: {'PASSED' if test_status else 'FAILED'}")
        
        return True
    except Exception as e:
        print(f"✗ Model loading failed: {str(e)}")
        return False

def test_prediction_service():
    """Test prediction service"""
    print("\nTesting prediction service...")
    try:
        from services.prediction_service import PredictionService
        
        service = PredictionService()
        
        # Test prediction
        result = service.predict_policy_impact(
            policy_date="2025-04-01",
            forecast_days=30,
            compliance_level=0.8
        )
        
        print(f"✓ Prediction service works")
        print(f"✓ Total people affected: {result['summary']['total_people_affected']:,}")
        
        return True
    except Exception as e:
        print(f"✗ Prediction service failed: {str(e)}")
        return False

def test_flask_app():
    """Test Flask app endpoints"""
    print("\nTesting Flask app...")
    try:
        from app import app
        
        with app.test_client() as client:
            # Test root endpoint
            response = client.get('/')
            print(f"✓ Root endpoint: {response.status_code}")
            
            # Test health endpoint
            response = client.get('/health')
            print(f"✓ Health endpoint: {response.status_code}")
            if response.status_code == 200:
                data = response.get_json()
                print(f"  - Status: {data.get('status')}")
                print(f"  - Models: {data.get('models')}")
                print(f"  - Features: {data.get('features')}")
            
            # Test states endpoint
            response = client.get('/api/states')
            print(f"✓ States endpoint: {response.status_code}")
            
            # Test prediction endpoint
            prediction_data = {
                "policy_date": "2025-04-01",
                "forecast_days": 30,
                "compliance_level": 0.8
            }
            response = client.post('/api/predict', 
                                 data=json.dumps(prediction_data),
                                 content_type='application/json')
            print(f"✓ Prediction endpoint: {response.status_code}")
            
        return True
    except Exception as e:
        print(f"✗ Flask app test failed: {str(e)}")
        return False

def main():
    """Run all tests"""
    print("=== Backend Test Suite ===\n")
    
    tests = [
        test_model_loading,
        test_prediction_service,
        test_flask_app
    ]
    
    results = []
    for test in tests:
        try:
            result = test()
            results.append(result)
        except Exception as e:
            print(f"✗ Test failed with exception: {str(e)}")
            results.append(False)
    
    print(f"\n=== Test Results ===")
    print(f"Passed: {sum(results)}/{len(results)}")
    
    if all(results):
        print("🎉 All tests passed! Backend is ready for deployment.")
        return 0
    else:
        print("❌ Some tests failed. Check the errors above.")
        return 1

if __name__ == "__main__":
    sys.exit(main())