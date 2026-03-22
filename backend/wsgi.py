#!/usr/bin/env python3
"""
WSGI entry point with NumPy compatibility fixes for Render deployment
"""

import os
import sys
import warnings

# Apply compatibility fixes before any imports
warnings.filterwarnings('ignore', category=FutureWarning)
warnings.filterwarnings('ignore', category=UserWarning)
warnings.filterwarnings('ignore', category=DeprecationWarning)
warnings.filterwarnings('ignore', message='.*ComplexWarning.*')
warnings.filterwarnings('ignore', message='.*numpy.core.*')

# Set environment variables
os.environ['PYTHONWARNINGS'] = 'ignore'
os.environ['NUMPY_DISABLE_WARNINGS'] = '1'

# Handle NumPy compatibility
try:
    import numpy as np
    
    # Patch ComplexWarning if it doesn't exist
    if not hasattr(np, 'ComplexWarning'):
        class ComplexWarning(UserWarning):
            pass
        np.ComplexWarning = ComplexWarning
        
        # Also patch numpy.core.numeric
        try:
            import numpy.core.numeric as numeric
            if not hasattr(numeric, 'ComplexWarning'):
                numeric.ComplexWarning = ComplexWarning
        except (ImportError, AttributeError):
            pass
            
except ImportError:
    pass

# Import the Flask app
from app import app

# WSGI application
application = app

if __name__ == "__main__":
    port = int(os.getenv('PORT', 10000))
    app.run(host='0.0.0.0', port=port, debug=False)