#!/usr/bin/env python3
"""
Comprehensive deployment test for production readiness
"""

import sys
import os
import json
import time
import warnings
from datetime import datetime

# Suppress warnings for cleaner output
warnings.filterwarnings('ignore')

def test_production_startup():
    """Test the production startup script"""
    print("=== Testing Production Startup ===")
    try:
        from production_startup import production_startup
        
        result = production_startup()
        print(f"+ Production startup: {'PASSED' if result else 'FAILED'}")
        return result
    except Exception as e:
        print(f"- Production startup failed: {e}")
        return False

def test_api_endpoints():
    """Test all API endpoints"""
    print("\n=== Testing API Endpoints ===")
    try:
        from app import create_app
        
        app = create_app()
        
        with app.test_client() as client:
            # Test all endpoints
            endpoints = [
                ('GET', '/', 'Root'),
                ('GET', '/health', 'Health'),
                ('GET', '/api/states', 'States'),
            ]
            
            all_passed = True
            for method, path, name in endpoints:
                response = client.open(method=method, path=path)
                status = response.status_code
                passed = status == 200
                print(f"{'+ ' if passed else '- '}{name} endpoint: {status}")
                if not passed:
                    all_passed = False
            
            # Test prediction endpoint
            prediction_data = {
                "policy_date": "2025-04-01",
                "forecast_days": 10,
                "compliance_level": 0.8
            }
            
            start_time = time.time()
            response = client.post('/api/predict', 
                                 data=json.dumps(prediction_data),
                                 content_type='application/json')
            end_time = time.time()
            
            prediction_time = end_time - start_time
            passed = response.status_code == 200
            print(f"{'+ ' if passed else '- '}Prediction endpoint: {response.status_code} ({prediction_time:.1f}s)")
            
            if passed:
                data = response.get_json()
                if data.get('success'):
                    total_affected = data['results']['summary']['total_people_affected']
                    print(f"  Result: {total_affected:,} people affected")
                else:
                    print(f"  Error: {data.get('error')}")
                    all_passed = False
            else:
                all_passed = False
            
            return all_passed
            
    except Exception as e:
        print(f"- API endpoints test failed: {e}")
        return False

def test_performance():
    """Test performance characteristics"""
    print("\n=== Testing Performance ===")
    try:
        from services.prediction_service import PredictionService
        
        service = PredictionService()
        
        # Test multiple predictions
        test_cases = [
            (10, "Small"),
            (30, "Medium"),
            (60, "Large")
        ]
        
        all_passed = True
        for forecast_days, size in test_cases:
            start_time = time.time()
            
            result = service.predict_policy_impact(
                policy_date="2025-04-01",
                forecast_days=forecast_days,
                compliance_level=0.8
            )
            
            end_time = time.time()
            prediction_time = end_time - start_time
            
            # Performance thresholds
            max_time = 30.0  # 30 seconds max
            passed = prediction_time < max_time
            
            print(f"{'+ ' if passed else '- '}{size} prediction ({forecast_days} days): {prediction_time:.1f}s")
            
            if not passed:
                all_passed = False
        
        return all_passed
        
    except Exception as e:
        print(f"- Performance test failed: {e}")
        return False

def test_error_handling():
    """Test error handling"""
    print("\n=== Testing Error Handling ===")
    try:
        from app import create_app
        
        app = create_app()
        
        with app.test_client() as client:
            # Test invalid prediction requests
            test_cases = [
                ({}, "Empty request"),
                ({"policy_date": "invalid"}, "Invalid date"),
                ({"policy_date": "2025-04-01", "forecast_days": -1}, "Invalid forecast days"),
                ({"policy_date": "2025-04-01", "forecast_days": 30, "compliance_level": 2.0}, "Invalid compliance level")
            ]
            
            all_passed = True
            for data, description in test_cases:
                response = client.post('/api/predict',
                                     data=json.dumps(data),
                                     content_type='application/json')
                
                # Should return 400 for invalid requests
                passed = response.status_code == 400
                print(f"{'+ ' if passed else '- '}{description}: {response.status_code}")
                
                if not passed:
                    all_passed = False
            
            return all_passed
            
    except Exception as e:
        print(f"- Error handling test failed: {e}")
        return False

def main():
    """Run comprehensive deployment tests"""
    print("=== Comprehensive Deployment Test ===")
    print(f"Timestamp: {datetime.utcnow().isoformat()}")
    print(f"Python: {sys.version}")
    print(f"Directory: {os.getcwd()}")
    
    tests = [
        ("Production Startup", test_production_startup),
        ("API Endpoints", test_api_endpoints),
        ("Performance", test_performance),
        ("Error Handling", test_error_handling)
    ]
    
    results = []
    for test_name, test_func in tests:
        try:
            result = test_func()
            results.append(result)
        except Exception as e:
            print(f"- {test_name} failed with exception: {e}")
            results.append(False)
    
    # Summary
    passed = sum(results)
    total = len(results)
    
    print(f"\n=== Deployment Test Results ===")
    print(f"Tests passed: {passed}/{total}")
    
    if all(results):
        print("SUCCESS: System is production-ready and deployment-ready!")
        print("\nNext steps:")
        print("1. Push code to GitHub")
        print("2. Deploy to Render")
        print("3. Set environment variables")
        print("4. Test live deployment")
        return 0
    else:
        print("FAILED: Some tests failed. Fix issues before deployment.")
        return 1

if __name__ == "__main__":
    sys.exit(main())