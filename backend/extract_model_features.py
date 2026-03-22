#!/usr/bin/env python3
"""
Extract the exact features from trained models
"""

import joblib
import os
import sys

def extract_features_from_model():
    """Extract features from the actual trained model"""
    try:
        # Try to load the baseline model and get its expected features
        model_path = os.path.join('data', 'models', 'enrolment_baseline_model.pkl')
        
        if os.path.exists(model_path):
            model = joblib.load(model_path)
            
            if hasattr(model, 'feature_names_in_'):
                features = list(model.feature_names_in_)
                print(f"Found {len(features)} features in trained model:")
                for i, feature in enumerate(features):
                    print(f"{i+1:2d}. {feature}")
                
                # Save these as the correct feature columns
                feature_file = os.path.join('data', 'models', 'policy_feature_cols.pkl')
                joblib.dump(features, feature_file)
                print(f"\nSaved correct features to {feature_file}")
                
                return features
            else:
                print("Model doesn't have feature_names_in_ attribute")
                return None
        else:
            print("Model file not found")
            return None
            
    except Exception as e:
        print(f"Error: {e}")
        return None

if __name__ == "__main__":
    extract_features_from_model()