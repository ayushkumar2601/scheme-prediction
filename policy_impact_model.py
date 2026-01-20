"""
Policy Impact Model Module
Predicts policy impact using interrupted time series analysis
"""

import pandas as pd
import numpy as np
from sklearn.ensemble import GradientBoostingRegressor, RandomForestRegressor
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
import joblib
from typing import Dict, Tuple
import warnings
warnings.filterwarnings('ignore')

class PolicyImpactModel:
    """Model to predict policy impact on enrolments and updates"""
    
    def __init__(self):
        self.enrolment_impact_model = None
        self.update_impact_model = None
        self.feature_cols = None
        
    def prepare_policy_features(self, df: pd.DataFrame) -> Tuple[pd.DataFrame, list]:
        """Prepare features including policy indicators"""
        exclude_cols = ['date', 'state', 'total_enrolments', 'total_updates',
                       'age_0_5', 'age_5_17', 'age_18_greater',
                       'total_bio_updates', 'bio_age_5_17', 'bio_age_17_',
                       'total_demo_updates', 'demo_age_5_17', 'demo_age_17_',
                       'num_districts']
        
        feature_cols = [col for col in df.columns if col not in exclude_cols]
        
        return df[feature_cols], feature_cols
    
    def train_impact_models(self, df: pd.DataFrame, policy_date: str, test_size: float = 0.2) -> Dict:
        """Train models with policy features"""
        print(f"Training policy impact models (policy date: {policy_date})...")
        
        # Ensure policy features exist
        if 'policy_active' not in df.columns:
            from feature_engineering import FeatureEngineer
            fe = FeatureEngineer(df)
            df = fe.add_policy_features(policy_date)
        
        X, feature_cols = self.prepare_policy_features(df)
        self.feature_cols = feature_cols
        
        # Train enrolment impact model
        y_enrol = df['total_enrolments']
        mask_enrol = y_enrol > 0
        X_enrol = X[mask_enrol]
        y_enrol = y_enrol[mask_enrol]
        
        X_train_e, X_test_e, y_train_e, y_test_e = train_test_split(
            X_enrol, y_enrol, test_size=test_size, random_state=42
        )
        
        self.enrolment_impact_model = GradientBoostingRegressor(
            n_estimators=150,
            learning_rate=0.1,
            max_depth=6,
            random_state=42
        )
        self.enrolment_impact_model.fit(X_train_e, y_train_e)
        
        y_pred_e = self.enrolment_impact_model.predict(X_test_e)
        enrol_metrics = {
            'mae': mean_absolute_error(y_test_e, y_pred_e),
            'rmse': np.sqrt(mean_squared_error(y_test_e, y_pred_e)),
            'r2': r2_score(y_test_e, y_pred_e)
        }
        
        print(f"Enrolment Impact Model - MAE: {enrol_metrics['mae']:.2f}, R²: {enrol_metrics['r2']:.4f}")
        
        # Train update impact model
        y_update = df['total_updates']
        mask_update = y_update > 0
        X_update = X[mask_update]
        y_update = y_update[mask_update]
        
        X_train_u, X_test_u, y_train_u, y_test_u = train_test_split(
            X_update, y_update, test_size=test_size, random_state=42
        )
        
        self.update_impact_model = GradientBoostingRegressor(
            n_estimators=150,
            learning_rate=0.1,
            max_depth=6,
            random_state=42
        )
        self.update_impact_model.fit(X_train_u, y_train_u)
        
        y_pred_u = self.update_impact_model.predict(X_test_u)
        update_metrics = {
            'mae': mean_absolute_error(y_test_u, y_pred_u),
            'rmse': np.sqrt(mean_squared_error(y_test_u, y_pred_u)),
            'r2': r2_score(y_test_u, y_pred_u)
        }
        
        print(f"Update Impact Model - MAE: {update_metrics['mae']:.2f}, R²: {update_metrics['r2']:.4f}")
        
        return {'enrolment': enrol_metrics, 'update': update_metrics}
    
    def predict_with_policy(self, df: pd.DataFrame) -> pd.DataFrame:
        """Predict enrolments and updates with policy impact"""
        X, _ = self.prepare_policy_features(df)
        
        df_pred = df.copy()
        df_pred['predicted_enrolments_with_policy'] = self.enrolment_impact_model.predict(X)
        df_pred['predicted_updates_with_policy'] = self.update_impact_model.predict(X)
        
        return df_pred
    
    def calculate_policy_impact(self, df: pd.DataFrame, baseline_predictions: pd.DataFrame) -> pd.DataFrame:
        """Calculate incremental impact due to policy"""
        df_impact = df.copy()
        
        # Merge baseline predictions
        df_impact['baseline_enrolments'] = baseline_predictions['predicted_enrolments']
        df_impact['baseline_updates'] = baseline_predictions['predicted_updates']
        
        # Predict with policy
        df_with_policy = self.predict_with_policy(df)
        df_impact['policy_enrolments'] = df_with_policy['predicted_enrolments_with_policy']
        df_impact['policy_updates'] = df_with_policy['predicted_updates_with_policy']
        
        # Calculate incremental impact
        df_impact['enrolment_impact'] = df_impact['policy_enrolments'] - df_impact['baseline_enrolments']
        df_impact['update_impact'] = df_impact['policy_updates'] - df_impact['baseline_updates']
        df_impact['total_impact'] = df_impact['enrolment_impact'] + df_impact['update_impact']
        
        # Only consider positive impacts after policy date
        if 'policy_active' in df_impact.columns:
            df_impact.loc[df_impact['policy_active'] == 0, 'enrolment_impact'] = 0
            df_impact.loc[df_impact['policy_active'] == 0, 'update_impact'] = 0
            df_impact.loc[df_impact['policy_active'] == 0, 'total_impact'] = 0
        
        return df_impact
    
    def save_models(self, enrol_path: str = "enrolment_impact_model.pkl",
                   update_path: str = "update_impact_model.pkl"):
        """Save trained models"""
        joblib.dump(self.enrolment_impact_model, enrol_path)
        joblib.dump(self.update_impact_model, update_path)
        joblib.dump(self.feature_cols, "policy_feature_cols.pkl")
        print(f"Policy impact models saved")
    
    def load_models(self, enrol_path: str = "enrolment_impact_model.pkl",
                   update_path: str = "update_impact_model.pkl"):
        """Load trained models"""
        self.enrolment_impact_model = joblib.load(enrol_path)
        self.update_impact_model = joblib.load(update_path)
        self.feature_cols = joblib.load("policy_feature_cols.pkl")
        print("Policy impact models loaded successfully")

if __name__ == "__main__":
    # Load featured data
    df = pd.read_csv("featured_aadhaar_data.csv")
    
    # Example: Train with a hypothetical policy date
    policy_date = "2025-03-15"
    
    model = PolicyImpactModel()
    metrics = model.train_impact_models(df, policy_date)
    model.save_models()
