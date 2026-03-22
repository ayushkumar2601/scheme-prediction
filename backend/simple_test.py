#!/usr/bin/env python3
"""
Simple test to verify backend functionality
Run this from the backend directory
"""

import sys
import os

def test_imports():
    """Test if we can import the modules"""
    print("Testing imports...")
    try:
        from models.model_loader import ModelLoader
        print("+ Can import ModelLoader")
        
        from services.prediction_service import PredictionService  
        print("+ Can import PredictionService")
        
        from flask_cors import CORS
        print("+ Can import flask-cors")
        
        return True
    except Exception as e:
        print(f"- Import failed: {e}")
        return False

def test_model_loading():
    """Test model loading"""
    print("\nTesting model loading...")
    try:
        from models.model_loader import ModelLoader
        
        loader = ModelLoader()
        models = loader.load_models()
        
        baseline_features = models.get('baseline_features', [])
        policy_features = models.get('policy_features', [])
        
        print(f"+ Baseline features: {len(baseline_features)}")
        print(f"+ Policy features: {len(policy_features)}")
        
        # Test models
        test_result = loader.test_models()
        print(f"+ Model test: {'PASSED' if test_result else 'FAILED'}")
        
        return test_result
    except Exception as e:
        print(f"- Model loading failed: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_prediction():
    """Test prediction service"""
    print("\nTesting prediction...")
    try:
        from services.prediction_service import PredictionService
        
        service = PredictionService()
        result = service.predict_policy_impact(
            policy_date="2025-04-01",
            forecast_days=10,  # Small test
            compliance_level=0.8
        )
        
        print(f"+ Prediction works: {result['summary']['total_people_affected']:,} people affected")
        return True
    except Exception as e:
        print(f"- Prediction failed: {e}")
        import traceback
        traceback.print_exc()
        return False

def main():
    print("=== Simple Backend Test ===")
    print(f"Working directory: {os.getcwd()}")
    
    tests = [test_imports, test_model_loading, test_prediction]
    results = []
    
    for test in tests:
        try:
            result = test()
            results.append(result)
        except Exception as e:
            print(f"- Test exception: {e}")
            results.append(False)
    
    print(f"\nResults: {sum(results)}/{len(results)} passed")
    
    if all(results):
        print("SUCCESS: Backend is working!")
        return 0
    else:
        print("FAILED: Some tests failed")
        return 1

if __name__ == "__main__":
    sys.exit(main())