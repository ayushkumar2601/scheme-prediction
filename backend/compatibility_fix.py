"""
Compatibility fixes for NumPy and scikit-learn version issues
Run this before importing other modules to ensure compatibility
"""

import warnings
import sys
import os

def apply_compatibility_fixes():
    """Apply compatibility fixes for common dependency issues"""
    
    # Suppress all NumPy warnings related to ComplexWarning
    warnings.filterwarnings('ignore', category=FutureWarning)
    warnings.filterwarnings('ignore', category=UserWarning)
    warnings.filterwarnings('ignore', message='.*ComplexWarning.*')
    warnings.filterwarnings('ignore', message='.*numpy.core.*')
    
    # Handle NumPy compatibility
    try:
        import numpy as np
        
        # Monkey patch for ComplexWarning if it doesn't exist
        if not hasattr(np, 'ComplexWarning'):
            try:
                from numpy.core.numeric import ComplexWarning
                np.ComplexWarning = ComplexWarning
            except ImportError:
                # Create a dummy ComplexWarning class
                class ComplexWarning(UserWarning):
                    pass
                np.ComplexWarning = ComplexWarning
                
    except ImportError:
        pass
    
    # Handle scikit-learn compatibility
    try:
        import sklearn
        # Suppress sklearn warnings
        warnings.filterwarnings('ignore', category=sklearn.exceptions.DataConversionWarning)
    except ImportError:
        pass
    
    # Set environment variables for better compatibility
    os.environ['PYTHONWARNINGS'] = 'ignore'
    
    print("Compatibility fixes applied successfully")

if __name__ == "__main__":
    apply_compatibility_fixes()