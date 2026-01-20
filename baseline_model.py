"""
Baseline Model Module
Learns normal behavior without policy influence
"""

import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestRegressor, GradientBoostingRegressor
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
import joblib
from typing import Dict, Tuple

class BaselineModel:
    """Model to learn baseline enrolment and update patterns"""
    
    def __init__(self):
        self.enrolment_model = None
        self.update_model = None
        self.feature_cols = None
        
    def prepare_features(self, df: pd.DataFrame, exclude_policy: bool = True) -> Tuple[pd.DataFrame, List]:
        """Prepare features for modeling"""
        # Exclude policy-related features for baseline
        exclude_cols = ['date', 'state', 'total_enrolments', 'total_updates',
                       'age_0_5', 'age_5_17', 'age_18_greater',
                       'total_bio_updates', 'bio_age_5_17', 'bio_age_17_',
                       'total_demo_updates', 'demo_age_5_17', 'demo_age_17_',
                       'num_districts']
        
        if exclude_policy:
            policy_cols = [col for col in df.columns if 'policy' in col.lower()]
            exclude_cols.extend(policy_cols)
        
        feature_cols = [col for col in df.columns if col not in exclude_cols]
        
        return df[feature_cols], feature_cols
    
    def train_enrolment_model(self, df: pd.DataFrame, test_size: float = 0.2) -> Dict:
        """Train model to predict enrolments"""
        print("Training enrolment baseline model...")
        
        X, feature_cols = self.prepare_features(df)
        y = df['total_enrolments']
        
        # Remove rows with zero target (no data)
        mask = y > 0
        X = X[mask]
        y = y[mask]
        
        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=test_size, random_state=42
        )
        
        # Train Gradient Boosting model
        model = GradientBoostingRegressor(
            n_estimators=100,
            learning_rate=0.1,
            max_depth=5,
            random_state=42
        )
        
        model.fit(X_train, y_train)
        
        # Evaluate
        y_pred = model.predict(X_test)
        
        metrics = {
            'mae': mean_absolute_error(y_test, y_pred),
            'rmse': np.sqrt(mean_squared_error(y_test, y_pred)),
            'r2': r2_score(y_test, y_pred)
        }
        
        print(f"Enrolment Model - MAE: {metrics['mae']:.2f}, RMSE: {metrics['rmse']:.2f}, R²: {metrics['r2']:.4f}")
        
        self.enrolment_model = model
        self.feature_cols = feature_cols
        
        return metrics
    
    def train_update_model(self, df: pd.DataFrame, test_size: float = 0.2) -> Dict:
        """Train model to predict updates"""
        print("Training update baseline model...")
        
        X, feature_cols = self.prepare_features(df)
        y = df['total_updates']
        
        # Remove rows with zero target
        mask = y > 0
        X = X[mask]
        y = y[mask]
        
        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=test_size, random_state=42
        )
        
        # Train Gradient Boosting model
        model = GradientBoostingRegressor(
            n_estimators=100,
            learning_rate=0.1,
            max_depth=5,
            random_state=42
        )
        
        model.fit(X_train, y_train)
        
        # Evaluate
        y_pred = model.predict(X_test)
        
        metrics = {
            'mae': mean_absolute_error(y_test, y_pred),
            'rmse': np.sqrt(mean_squared_error(y_test, y_pred)),
            'r2': r2_score(y_test, y_pred)
        }
        
        print(f"Update Model - MAE: {metrics['mae']:.2f}, RMSE: {metrics['rmse']:.2f}, R²: {metrics['r2']:.4f}")
        
        self.update_model = model
        
        return metrics
    
    def predict_baseline(self, df: pd.DataFrame) -> pd.DataFrame:
        """Predict baseline enrolments and updates"""
        X, _ = self.prepare_features(df)
        
        df_pred = df.copy()
        df_pred['predicted_enrolments'] = self.enrolment_model.predict(X)
        df_pred['predicted_updates'] = self.update_model.predict(X)
        
        return df_pred
    
    def save_models(self, enrol_path: str = "enrolment_baseline_model.pkl",
                   update_path: str = "update_baseline_model.pkl"):
        """Save trained models"""
        joblib.dump(self.enrolment_model, enrol_path)
        joblib.dump(self.update_model, update_path)
        print(f"Models saved to {enrol_path} and {update_path}")
    
    def load_models(self, enrol_path: str = "enrolment_baseline_model.pkl",
                   update_path: str = "update_baseline_model.pkl"):
        """Load trained models"""
        self.enrolment_model = joblib.load(enrol_path)
        self.update_model = joblib.load(update_path)
        print("Models loaded successfully")

if __name__ == "__main__":
    # Load featured data
    df = pd.read_csv("featured_aadhaar_data.csv")
    
    # Train baseline models
    baseline = BaselineModel()
    baseline.train_enrolment_model(df)
    baseline.train_update_model(df)
    
    # Save models
    baseline.save_models()
