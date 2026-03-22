#!/usr/bin/env python3
"""
Create feature columns file if it doesn't exist
This ensures the backend has the correct feature alignment
"""

import os
import joblib
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def create_feature_columns():
    """Create feature columns file with the expected features"""
    
    # Expected feature columns based on the trained models
    feature_columns = [
        'year', 'month', 'day', 'day_of_week', 'week_of_year', 'is_weekend',
        'days_from_policy', 'policy_active',
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
        'trend_enrolment', 'trend_update'
    ]
    
    model_path = os.getenv('MODEL_PATH', 'data/models')
    feature_file = os.path.join(model_path, 'policy_feature_cols.pkl')
    
    # Create directory if it doesn't exist
    os.makedirs(model_path, exist_ok=True)
    
    # Check if file already exists
    if os.path.exists(feature_file):
        try:
            existing_features = joblib.load(feature_file)
            logger.info(f"Feature columns file exists with {len(existing_features)} features")
            return existing_features
        except Exception as e:
            logger.warning(f"Could not load existing feature file: {e}")
    
    # Create new feature file
    try:
        joblib.dump(feature_columns, feature_file)
        logger.info(f"Created feature columns file with {len(feature_columns)} features")
        logger.info(f"Saved to: {feature_file}")
        return feature_columns
    except Exception as e:
        logger.error(f"Failed to create feature columns file: {e}")
        return feature_columns

if __name__ == "__main__":
    create_feature_columns()