#!/usr/bin/env python3
"""
Test script for the fixed backend functionality
"""

import sys
import os
import json
from datetime import datetime

def test_model_loading():
    """Test model loading functionality"""
    print("=== Testing Model Loading ===")
    try:
        from models.model_loader import ModelLoader
        
        loader = ModelLoader()
        models = loader.load_models()
        
        print("+ Models loaded successfully")
        
        baseline_features = models.get('baseline_features', [])
        policy_features = models.get('policy_features', [])
        
        print(f"+ Baseline features count: {len(baseline_features)}")
        print(f"+ Policy features count: {len(policy_features)}")
        
        # Show first few features
        print("First 5 baseline features:", baseline_features[:5])
        print("First 5 policy features:", policy_features[:5])
        
        # Test model predictions
        test_status = loader.test_models()
        print(f"+ Model testing: {'PASSED' if test_status else 'FAILED'}")
        
        return test_status
    except Exception as e:
        print(f"- Model loading failed: {str(e)}")
        import traceback
        traceback.print_exc()
        return False

def test_prediction_service():
    """Test prediction service"""
    print("\n=== Testing Prediction Service ===")
    try:
        from services.prediction_service import PredictionService
        
        service = PredictionService()
        
        # Test prediction
        result = service.predict_policy_impact(
            policy_date="2025-04-01",
            forecast_days=30,
            compliance_level=0.8
        )
        
        print("+ Prediction service works")
        print(f"+ Total people affected: {result['summary']['total_people_affected']:,}")
        print(f"+ Daily impact entries: {len(result['daily_impact'])}")
        print(f"+ Regional impact states: {len(result['regional_impact']['by_state'])}")
        
        return True
    except Exception as e:
        print(f"- Prediction service failed: {str(e)}")
        import traceback
        traceback.print_exc()
        return False

def test_flask_app():
    """Test Flask app endpoints"""
    print("\n=== Testing Flask App ===")
    try:
        from app import app
        
        with app.test_client() as client:
            # Test root endpoint
            response = client.get('/')
            print(f"+ Root endpoint: {response.status_code}")
            if response.status_code == 200:
                data = response.get_json()
                print(f"  Service: {data.get('service', 'Unknown')}")
            
            # Test health endpoint
            response = client.get('/health')
            print(f"+ Health endpoint: {response.status_code}")
            if response.status_code == 200:
                data = response.get_json()
                print(f"  Status: {data.get('status')}")
                print(f"  Models: {data.get('models')}")
                print(f"  Features: {data.get('features')}")
            
            # Test states endpoint
            response = client.get('/api/states')
            print(f"+ States endpoint: {response.status_code}")
            if response.status_code == 200:
                data = response.get_json()
                print(f"  States count: {len(data.get('states', []))}")
            
            # Test prediction endpoint
            prediction_data = {
                "policy_date": "2025-04-01",
                "forecast_days": 30,
                "compliance_level": 0.8
            }
            response = client.post('/api/predict', 
                                 data=json.dumps(prediction_data),
                                 content_type='application/json')
            print(f"+ Prediction endpoint: {response.status_code}")
            if response.status_code == 200:
                data = response.get_json()
                if data.get('success'):
                    print("  Prediction successful")
                    print(f"  Total affected: {data['results']['summary']['total_people_affected']:,}")
                else:
                    print(f"  Prediction failed: {data.get('error')}")
            else:
                print(f"  Response: {response.get_data(as_text=True)[:200]}")
        
        return True
    except Exception as e:
        print(f"- Flask app test failed: {str(e)}")
        import traceback
        traceback.print_exc()
        return False

def main():
    """Run all tests"""
    print("=== Fixed Backend Test Suite ===")
    print(f"Python version: {sys.version}")
    print(f"Working directory: {os.getcwd()}")
    print()
    
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
            print(f"- Test failed with exception: {str(e)}")
            results.append(False)
    
    print(f"\n=== Test Results ===")
    print(f"Passed: {sum(results)}/{len(results)}")
    
    if all(results):
        print("SUCCESS: All tests passed! Backend is ready for deployment.")
        return 0
    else:
        print("FAILED: Some tests failed. Check the errors above.")
        return 1

if __name__ == "__main__":
    sys.exit(main())