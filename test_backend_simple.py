#!/usr/bin/env python3
"""
Simple test for backend - run from root directory
"""

import sys
import os

# Add backend to path
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), 'backend'))

def test_model_loading():
    """Test model loading functionality"""
    print("Testing model loading...")
    try:
        from models.model_loader import ModelLoader
        
        loader = ModelLoader()
        models = loader.load_models()
        
        print(f"✓ Models loaded successfully")
        print(f"✓ Feature columns count: {len(models['feature_columns'])}")
        
        # Print first few features to see what we have
        features = models['feature_columns']
        print("First 10 features:")
        for i, feature in enumerate(features[:10]):
            print(f"  {i+1}. {feature}")
        
        # Test model predictions
        test_status = loader.test_models()
        print(f"✓ Model testing: {'PASSED' if test_status else 'FAILED'}")
        
        return True
    except Exception as e:
        print(f"✗ Model loading failed: {str(e)}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    test_model_loading()