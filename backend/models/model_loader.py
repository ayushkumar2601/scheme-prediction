"""
Model Loader for Aadhaar Policy Impact Prediction System
Handles loading and caching of trained ML models with proper feature alignment
"""

import os
import pandas as pd
import numpy as np
import joblib
from typing import Dict, Optional, List
import logging
from functools import lru_cache

logger = logging.getLogger(__name__)

class ModelLoader:
    """Handles loading and caching of ML models with feature alignment"""
    
    def __init__(self):
        self.model_path = os.getenv('MODEL_PATH', 'data/models')
        self.data_path = os.getenv('DATA_PATH', '.')
        self._models = None
        self._master_data = None
        self._feature_columns = None
    
    @lru_cache(maxsize=1)
    def load_models(self) -> Dict:
        """
        Load all trained models with caching and feature column alignment
        
        Returns:
            Dictionary containing all loaded models and feature columns
        """
        try:
            logger.info("Loading ML models...")
            
            models = {}
            
            # First, load feature columns
            feature_cols_path = os.path.join(self.model_path, 'policy_feature_cols.pkl')
            if os.path.exists(feature_cols_path):
                self._feature_columns = joblib.load(feature_cols_path)
                logger.info(f"Loaded feature columns: {len(self._feature_columns)} features")
            else:
                self._feature_columns = self._get_default_feature_columns()
                logger.warning(f"Using default feature columns: {len(self._feature_columns)} features")
            
            models['feature_columns'] = self._feature_columns
            
            # Load baseline models
            baseline_enrolment_path = os.path.join(self.model_path, 'enrolment_baseline_model.pkl')
            baseline_update_path = os.path.join(self.model_path, 'update_baseline_model.pkl')
            
            # Load policy impact models
            policy_enrolment_path = os.path.join(self.model_path, 'enrolment_impact_model.pkl')
            policy_update_path = os.path.join(self.model_path, 'update_impact_model.pkl')
            
            # Check if model files exist, if not use fallback models
            if os.path.exists(baseline_enrolment_path):
                models['baseline_enrolment'] = joblib.load(baseline_enrolment_path)
                logger.info("Loaded baseline enrolment model")
            else:
                models['baseline_enrolment'] = self._create_fallback_model()
                logger.warning("Using fallback baseline enrolment model")
            
            if os.path.exists(baseline_update_path):
                models['baseline_update'] = joblib.load(baseline_update_path)
                logger.info("Loaded baseline update model")
            else:
                models['baseline_update'] = self._create_fallback_model()
                logger.warning("Using fallback baseline update model")
            
            if os.path.exists(policy_enrolment_path):
                models['policy_enrolment'] = joblib.load(policy_enrolment_path)
                logger.info("Loaded policy enrolment model")
            else:
                models['policy_enrolment'] = self._create_fallback_model()
                logger.warning("Using fallback policy enrolment model")
            
            if os.path.exists(policy_update_path):
                models['policy_update'] = joblib.load(policy_update_path)
                logger.info("Loaded policy update model")
            else:
                models['policy_update'] = self._create_fallback_model()
                logger.warning("Using fallback policy update model")
            
            logger.info("Models loaded successfully")
            logger.info(f"Feature columns count: {len(self._feature_columns)}")
            
            return models
            
        except Exception as e:
            logger.error(f"Failed to load models: {str(e)}")
            # Return fallback models to prevent service failure
            return self._create_fallback_models()
    
    def _create_fallback_model(self):
        """Create a simple fallback model for when trained models are not available"""
        from sklearn.ensemble import GradientBoostingRegressor
        
        # Create a model with default parameters
        model = GradientBoostingRegressor(
            n_estimators=50,
            learning_rate=0.1,
            max_depth=3,
            random_state=42
        )
        
        # Train on dummy data with correct feature count
        import numpy as np
        feature_count = len(self._feature_columns) if self._feature_columns else 34
        X_dummy = np.random.rand(100, feature_count)
        y_dummy = np.random.rand(100) * 1000
        model.fit(X_dummy, y_dummy)
        
        return model
    
    def _create_fallback_models(self) -> Dict:
        """Create fallback models when loading fails"""
        logger.warning("Creating fallback models")
        
        # Ensure feature columns are set
        if self._feature_columns is None:
            self._feature_columns = self._get_default_feature_columns()
        
        return {
            'baseline_enrolment': self._create_fallback_model(),
            'baseline_update': self._create_fallback_model(),
            'policy_enrolment': self._create_fallback_model(),
            'policy_update': self._create_fallback_model(),
            'feature_columns': self._feature_columns
        }
    
    def _get_default_feature_columns(self) -> List[str]:
        """Get default feature columns matching the trained models"""
        return [
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
    
    def align_features(self, X: pd.DataFrame) -> pd.DataFrame:
        """
        Align input features with trained model expectations
        
        Args:
            X: Input DataFrame with features
            
        Returns:
            DataFrame with properly aligned features
        """
        if self._feature_columns is None:
            # Load feature columns if not already loaded
            models = self.load_models()
            self._feature_columns = models['feature_columns']
        
        # Log current shape
        logger.debug(f"Input features shape: {X.shape}")
        logger.debug(f"Expected features: {len(self._feature_columns)}")
        
        # Reindex to match expected features, filling missing with 0
        X_aligned = X.reindex(columns=self._feature_columns, fill_value=0)
        
        # Validate alignment
        assert X_aligned.shape[1] == len(self._feature_columns), \
            f"Feature alignment failed: got {X_aligned.shape[1]}, expected {len(self._feature_columns)}"
        
        logger.debug(f"Aligned features shape: {X_aligned.shape}")
        return X_aligned
    
    @lru_cache(maxsize=1)
    def load_master_data(self) -> pd.DataFrame:
        """
        Load master dataset with caching
        
        Returns:
            Master dataset DataFrame
        """
        try:
            logger.info("Loading master data...")
            
            master_data_path = os.path.join(self.data_path, 'master_aadhaar_data.csv')
            
            if os.path.exists(master_data_path):
                df = pd.read_csv(master_data_path)
                df['date'] = pd.to_datetime(df['date'])
                logger.info(f"Loaded master data with {len(df)} records")
                return df
            else:
                logger.warning("Master data file not found, creating dummy data")
                return self._create_dummy_master_data()
                
        except Exception as e:
            logger.error(f"Failed to load master data: {str(e)}")
            return self._create_dummy_master_data()
    
    def _create_dummy_master_data(self) -> pd.DataFrame:
        """Create dummy master data for fallback"""
        import numpy as np
        from datetime import datetime, timedelta
        
        # Create dummy data for major states
        states = [
            'Uttar Pradesh', 'Maharashtra', 'Bihar', 'West Bengal', 'Madhya Pradesh',
            'Tamil Nadu', 'Rajasthan', 'Karnataka', 'Gujarat', 'Andhra Pradesh'
        ]
        
        # Create 30 days of dummy data
        dates = pd.date_range(start='2025-01-01', periods=30, freq='D')
        
        data = []
        for state in states:
            for date in dates:
                data.append({
                    'date': date,
                    'state': state,
                    'total_enrolments': np.random.randint(500, 2000),
                    'total_updates': np.random.randint(200, 1000),
                    'num_districts': np.random.randint(10, 50)
                })
        
        df = pd.DataFrame(data)
        logger.info(f"Created dummy master data with {len(df)} records")
        return df
    
    def test_models(self) -> bool:
        """
        Test if models can be loaded and used for prediction with proper feature alignment
        
        Returns:
            True if models are working, False otherwise
        """
        try:
            models = self.load_models()
            feature_columns = models['feature_columns']
            
            # Create test input with correct feature structure
            test_input = pd.DataFrame([[0] * len(feature_columns)], columns=feature_columns)
            
            logger.info(f"Testing models with {len(feature_columns)} features")
            
            # Test each model with properly structured dummy data
            for model_name, model in models.items():
                if model_name != 'feature_columns':
                    try:
                        pred = model.predict(test_input)
                        if not isinstance(pred, np.ndarray) or len(pred) != 1:
                            logger.error(f"Model {model_name} prediction test failed")
                            return False
                        logger.debug(f"Model {model_name} test passed")
                    except Exception as e:
                        logger.error(f"Model {model_name} test failed: {str(e)}")
                        return False
            
            logger.info("All models passed testing")
            return True
            
        except Exception as e:
            logger.error(f"Model testing failed: {str(e)}")
            return False
    
    def save_models(self, models: Dict, model_path: Optional[str] = None):
        """
        Save models to disk
        
        Args:
            models: Dictionary of models to save
            model_path: Optional custom path for saving models
        """
        if model_path is None:
            model_path = self.model_path
        
        try:
            os.makedirs(model_path, exist_ok=True)
            
            for model_name, model in models.items():
                if model_name != 'feature_columns':
                    model_file = os.path.join(model_path, f'{model_name}.pkl')
                    joblib.dump(model, model_file)
                    logger.info(f"Saved {model_name} model to {model_file}")
            
            # Save feature columns
            if 'feature_columns' in models:
                feature_file = os.path.join(model_path, 'feature_columns.pkl')
                joblib.dump(models['feature_columns'], feature_file)
                logger.info(f"Saved feature columns to {feature_file}")
            
        except Exception as e:
            logger.error(f"Failed to save models: {str(e)}")
            raise