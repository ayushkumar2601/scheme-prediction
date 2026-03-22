#!/usr/bin/env python3
"""
Fix feature columns to match trained models
"""

import joblib
import os

# The exact features the trained models expect (based on error message)
correct_features = [
    'year', 'month', 'day', 'day_of_week', 'week_of_year', 'is_weekend',
    'days_from_policy', 'policy_active',
    'post_policy_30d', 'post_policy_60d', 'pre_policy_30d',
    'total_enrolments_lag_1', 'total_enrolments_lag_7', 'total_enrolments_lag_30',
    'total_updates_lag_1', 'total_updates_lag_7', 'total_updates_lag_30',
    'total_enrolments_rolling_mean_7', 'total_enrolments_rolling_mean_30',
    'total_updates_rolling_mean_7', 'total_updates_rolling_mean_30',
    'enrolment_growth_1d', 'update_growth_1d',
    'total_enrolments_rolling_std_7', 'total_enrolments_rolling_std_30',
    'total_updates_rolling_std_7', 'total_updates_rolling_std_30',
    'enrolment_growth_7d', 'update_growth_7d',
    'state_avg_enrolments', 'state_avg_updates',
    'enrolment_deviation', 'update_deviation',
    'seasonal_enrolment', 'seasonal_update',
    'trend_enrolment', 'trend_update',
    'policy_period_days', 'policy_intensity', 'policy_momentum',
    'regional_policy_impact', 'temporal_policy_effect'
]

def fix_feature_columns():
    """Overwrite feature columns with correct ones"""
    try:
        # Ensure directory exists
        os.makedirs('data/models', exist_ok=True)
        
        # Save correct features
        feature_file = 'data/models/policy_feature_cols.pkl'
        joblib.dump(correct_features, feature_file)
        
        print(f"✓ Fixed feature columns file with {len(correct_features)} features")
        print(f"✓ Saved to: {feature_file}")
        
        # Verify by loading back
        loaded_features = joblib.load(feature_file)
        print(f"✓ Verification: loaded {len(loaded_features)} features")
        
        return True
        
    except Exception as e:
        print(f"✗ Failed to fix features: {e}")
        return False

if __name__ == "__main__":
    fix_feature_columns()