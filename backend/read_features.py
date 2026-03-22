#!/usr/bin/env python3
"""
Read the actual feature columns from the trained models
"""

import joblib
import os

def read_feature_columns():
    """Read feature columns from the pickle file"""
    try:
        feature_file = os.path.join('data', 'models', 'policy_feature_cols.pkl')
        if os.path.exists(feature_file):
            features = joblib.load(feature_file)
            print(f"Found {len(features)} features in policy_feature_cols.pkl:")
            for i, feature in enumerate(features):
                print(f"{i+1:2d}. {feature}")
            return features
        else:
            print("policy_feature_cols.pkl not found")
            return None
    except Exception as e:
        print(f"Error reading features: {e}")
        return None

if __name__ == "__main__":
    read_feature_columns()