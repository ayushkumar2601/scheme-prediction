#!/usr/bin/env python3
"""
Render deployment startup script with NumPy compatibility fixes
"""

import os
import sys
import warnings

# Apply comprehensive compatibility fixes
def fix_numpy_compatibility():
    """Fix NumPy compatibility issues for Render deployment"""
    
    # Suppress all warnings that might cause issues
    warnings.filterwarnings('ignore', category=FutureWarning)
    warnings.filterwarnings('ignore', category=UserWarning)
    warnings.filterwarnings('ignore', category=DeprecationWarning)
    warnings.filterwarnings('ignore', message='.*ComplexWarning.*')
    warnings.filterwarnings('ignore', message='.*numpy.core.*')
    
    # Set environment variables to suppress warnings
    os.environ['PYTHONWARNINGS'] = 'ignore'
    os.environ['NUMPY_DISABLE_WARNINGS'] = '1'
    
    # Handle NumPy compatibility before any other imports
    try:
        import numpy as np
        
        # Check if ComplexWarning exists and patch if needed
        if not hasattr(np, 'ComplexWarning'):
            # Create a dummy ComplexWarning class
            class ComplexWarning(UserWarning):
                pass
            
            # Patch numpy
            np.ComplexWarning = ComplexWarning
            
            # Also patch numpy.core.numeric if it exists
            try:
                import numpy.core.numeric as numeric
                if not hasattr(numeric, 'ComplexWarning'):
                    numeric.ComplexWarning = ComplexWarning
            except (ImportError, AttributeError):
                pass
                
        print("NumPy compatibility fixes applied")
        
    except ImportError as e:
        print(f"Warning: Could not import NumPy: {e}")
    
    # Handle scikit-learn compatibility
    try:
        import sklearn
        warnings.filterwarnings('ignore', category=sklearn.exceptions.DataConversionWarning)
        print("Scikit-learn compatibility fixes applied")
    except ImportError:
        pass

# Apply fixes immediately
fix_numpy_compatibility()

# Now import the Flask app
try:
    from app import app
    print("Flask app imported successfully")
except ImportError as e:
    print(f"Error importing Flask app: {e}")
    sys.exit(1)

if __name__ == '__main__':
    port = int(os.getenv('PORT', 10000))
    print(f"Starting Flask app on port {port}")
    app.run(host='0.0.0.0', port=port, debug=False)