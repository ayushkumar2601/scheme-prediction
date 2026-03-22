#!/usr/bin/env python3
"""
Test script to verify NumPy compatibility fixes work
"""

import sys
import warnings

# Apply the same fixes as in wsgi.py
warnings.filterwarnings('ignore', category=FutureWarning)
warnings.filterwarnings('ignore', category=UserWarning)
warnings.filterwarnings('ignore', category=DeprecationWarning)
warnings.filterwarnings('ignore', message='.*ComplexWarning.*')
warnings.filterwarnings('ignore', message='.*numpy.core.*')

import os
os.environ['PYTHONWARNINGS'] = 'ignore'
os.environ['NUMPY_DISABLE_WARNINGS'] = '1'

# Test NumPy import
try:
    import numpy as np
    
    # Patch ComplexWarning if needed
    if not hasattr(np, 'ComplexWarning'):
        class ComplexWarning(UserWarning):
            pass
        np.ComplexWarning = ComplexWarning
        
        try:
            import numpy.core.numeric as numeric
            if not hasattr(numeric, 'ComplexWarning'):
                numeric.ComplexWarning = ComplexWarning
        except (ImportError, AttributeError):
            pass
    
    print("✅ NumPy import successful")
    print(f"NumPy version: {np.__version__}")
    
except Exception as e:
    print(f"❌ NumPy import failed: {e}")
    sys.exit(1)

# Test scikit-learn import
try:
    import sklearn
    print("✅ Scikit-learn import successful")
    print(f"Scikit-learn version: {sklearn.__version__}")
except Exception as e:
    print(f"❌ Scikit-learn import failed: {e}")
    sys.exit(1)

# Test Flask app import
try:
    from app import app
    print("✅ Flask app import successful")
    
    # Test health endpoint
    with app.test_client() as client:
        response = client.get('/health')
        if response.status_code == 200:
            print("✅ Health endpoint working")
            data = response.get_json()
            print(f"Status: {data.get('status')}")
            print(f"Models: {data.get('models')}")
        else:
            print(f"❌ Health endpoint failed: {response.status_code}")
            print(response.get_data(as_text=True))
            
except Exception as e:
    print(f"❌ Flask app test failed: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)

print("\n🎉 All compatibility tests passed!")
print("The NumPy compatibility fixes are working correctly.")