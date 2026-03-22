import joblib
import os

# Check what features the actual trained model expects
model_path = os.path.join('backend', 'data', 'models', 'enrolment_baseline_model.pkl')

if os.path.exists(model_path):
    try:
        model = joblib.load(model_path)
        if hasattr(model, 'feature_names_in_'):
            print(f"Model expects {len(model.feature_names_in_)} features:")
            for i, feature in enumerate(model.feature_names_in_):
                print(f"{i+1:2d}. {feature}")
        else:
            print("Model doesn't have feature_names_in_ attribute")
    except Exception as e:
        print(f"Error loading model: {e}")
else:
    print("Model file not found")

# Also check the feature columns file
feature_path = os.path.join('backend', 'data', 'models', 'policy_feature_cols.pkl')
if os.path.exists(feature_path):
    try:
        features = joblib.load(feature_path)
        print(f"\nFeature file has {len(features)} features:")
        for i, feature in enumerate(features):
            print(f"{i+1:2d}. {feature}")
    except Exception as e:
        print(f"Error loading features: {e}")
else:
    print("Feature file not found")