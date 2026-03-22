#!/usr/bin/env python3
"""
Inspect the actual features in the trained models
"""

import joblib
import os
import sys

def inspect_features():
    """Inspect what features are actually in the models"""
    try:
        # Check the feature columns file
        feature_file = os.path.join('backend', 'data', 'models', 'policy_feature_cols.pkl')
        if os.path.exists(feature_file):
            features = joblib.load(feature_file)
            print(f"Current feature file has {len(features)} features:")
            for i, feature in enumerate(features):
                print(f"{i+1:2d}. {feature}")
            print()
        else:
            print("Feature file not found")
        
        # Try to load one of the actual models to see what it expects
        model_file = os.path.join('backend', 'data', 'models', 'enrolment_baseline_model.pkl')
        if os.path.exists(model_file):
            model = joblib.load(model_file)
            if hasattr(model, 'feature_names_in_'):
                print(f"Model expects {len(model.feature_names_in_)} features:")
                for i, feature in enumerate(model.feature_names_in_):
                    print(f"{i+1:2d}. {feature}")
            else:
                print("Model doesn't have feature_names_in_ attribute")
        else:
            print("Model file not found")
            
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    inspect_features()