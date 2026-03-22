"""
Prediction Service for Aadhaar Policy Impact Prediction System
Handles ML model inference and prediction logic
"""

import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from typing import Dict, List, Optional
import logging
from functools import lru_cache
import warnings

# Suppress compatibility warnings
warnings.filterwarnings('ignore', category=FutureWarning)
warnings.filterwarnings('ignore', category=UserWarning)
warnings.filterwarnings('ignore', message='.*ComplexWarning.*')

from models.model_loader import ModelLoader

logger = logging.getLogger(__name__)

class PredictionService:
    """Service for generating policy impact predictions"""
    
    def __init__(self):
        self.model_loader = ModelLoader()
        self._models = None
        self._master_data = None
        
    @property
    def models(self):
        """Lazy load models"""
        if self._models is None:
            self._models = self.model_loader.load_models()
        return self._models
    
    @property
    def master_data(self):
        """Lazy load master data"""
        if self._master_data is None:
            self._master_data = self.model_loader.load_master_data()
        return self._master_data
    
    def predict_policy_impact(self, 
                            policy_date: str, 
                            forecast_days: int = 60,
                            compliance_level: float = 1.0,
                            affected_states: Optional[List[str]] = None) -> Dict:
        """
        Generate policy impact predictions
        
        Args:
            policy_date: Policy implementation date (YYYY-MM-DD)
            forecast_days: Number of days to forecast
            compliance_level: Expected compliance rate (0.0-1.0)
            affected_states: List of affected states (None for all states)
            
        Returns:
            Dictionary with comprehensive prediction results
        """
        try:
            logger.info(f"Starting prediction: policy_date={policy_date}, forecast_days={forecast_days}")
            
            # Create forecast dataset
            forecast_data = self._create_forecast_dataset(policy_date, forecast_days, affected_states)
            
            # Generate baseline predictions (without policy)
            baseline_predictions = self._generate_baseline_predictions(forecast_data)
            
            # Generate policy-influenced predictions
            policy_predictions = self._generate_policy_predictions(forecast_data)
            
            # Calculate incremental impact
            impact_data = self._calculate_impact(
                baseline_predictions, 
                policy_predictions, 
                forecast_data,
                compliance_level
            )
            
            # Generate comprehensive results
            results = self._compile_results(impact_data, forecast_data, policy_date, forecast_days)
            
            logger.info("Prediction completed successfully")
            return results
            
        except Exception as e:
            logger.error(f"Prediction failed: {str(e)}")
            raise
    
    def _create_forecast_dataset(self, policy_date: str, forecast_days: int, affected_states: Optional[List[str]]) -> pd.DataFrame:
        """Create dataset for forecasting"""
        policy_dt = pd.to_datetime(policy_date)
        
        # Get available states from master data
        if affected_states is None:
            available_states = self.master_data['state'].unique()
        else:
            available_states = [s for s in affected_states if s in self.master_data['state'].unique()]
        
        # Create date range for forecast
        forecast_dates = pd.date_range(
            start=policy_dt,
            periods=forecast_days,
            freq='D'
        )
        
        # Create forecast dataset
        forecast_data = []
        for state in available_states:
            for date in forecast_dates:
                days_from_policy = (date - policy_dt).days
                forecast_data.append({
                    'date': date,
                    'state': state,
                    'policy_date': policy_dt,
                    'days_from_policy': days_from_policy,
                    'policy_active': 1 if date >= policy_dt else 0,
                    # Add the policy features that the policy impact models expect
                    'pre_policy_30d': 1 if days_from_policy >= -30 and days_from_policy < 0 else 0,
                    'post_policy_30d': 1 if days_from_policy <= 30 and days_from_policy >= 0 else 0,
                    'post_policy_60d': 1 if days_from_policy <= 60 and days_from_policy >= 0 else 0,
                })
        
        forecast_df = pd.DataFrame(forecast_data)
        
        # Add temporal features
        forecast_df = self._add_temporal_features(forecast_df)
        
        # Add historical features (lag, rolling averages)
        forecast_df = self._add_historical_features(forecast_df)
        
        return forecast_df
    
    def _add_temporal_features(self, df: pd.DataFrame) -> pd.DataFrame:
        """Add temporal features"""
        df = df.copy()
        df['year'] = df['date'].dt.year
        df['month'] = df['date'].dt.month
        df['day'] = df['date'].dt.day
        df['day_of_week'] = df['date'].dt.dayofweek
        df['week_of_year'] = df['date'].dt.isocalendar().week
        df['is_weekend'] = df['day_of_week'].isin([5, 6]).astype(int)
        return df
    
    def _add_historical_features(self, df: pd.DataFrame) -> pd.DataFrame:
        """Add historical lag and rolling features"""
        # Get expected feature columns from model loader
        models = self.models
        policy_features = models.get('policy_features', models['feature_columns'])
        
        # Use state-based averages from historical data
        for state in df['state'].unique():
            state_historical = self.master_data[self.master_data['state'] == state]
            if len(state_historical) > 0:
                avg_enrolments = state_historical['total_enrolments'].mean()
                avg_updates = state_historical['total_updates'].mean()
            else:
                avg_enrolments = 1000  # Default fallback
                avg_updates = 500
            
            state_mask = df['state'] == state
            
            # Set lag features (1, 7, 14, 30 days)
            for lag in [1, 7, 14, 30]:
                if f'total_enrolments_lag_{lag}' in policy_features:
                    df.loc[state_mask, f'total_enrolments_lag_{lag}'] = avg_enrolments
                if f'total_updates_lag_{lag}' in policy_features:
                    df.loc[state_mask, f'total_updates_lag_{lag}'] = avg_updates
            
            # Set rolling mean and std features (7, 14, 30 days)
            for window in [7, 14, 30]:
                if f'total_enrolments_rolling_mean_{window}' in policy_features:
                    df.loc[state_mask, f'total_enrolments_rolling_mean_{window}'] = avg_enrolments
                if f'total_enrolments_rolling_std_{window}' in policy_features:
                    df.loc[state_mask, f'total_enrolments_rolling_std_{window}'] = avg_enrolments * 0.1
                if f'total_updates_rolling_mean_{window}' in policy_features:
                    df.loc[state_mask, f'total_updates_rolling_mean_{window}'] = avg_updates
                if f'total_updates_rolling_std_{window}' in policy_features:
                    df.loc[state_mask, f'total_updates_rolling_std_{window}'] = avg_updates * 0.1
            
            # Set growth features
            if 'total_enrolments_growth' in policy_features:
                df.loc[state_mask, 'total_enrolments_growth'] = 0.02  # 2% growth
            if 'total_enrolments_growth_7d' in policy_features:
                df.loc[state_mask, 'total_enrolments_growth_7d'] = 0.05  # 5% weekly growth
            if 'total_updates_growth' in policy_features:
                df.loc[state_mask, 'total_updates_growth'] = 0.01  # 1% growth
            if 'total_updates_growth_7d' in policy_features:
                df.loc[state_mask, 'total_updates_growth_7d'] = 0.03  # 3% weekly growth
            
            # Set state-level features
            if 'state_avg_enrolments' in policy_features:
                df.loc[state_mask, 'state_avg_enrolments'] = avg_enrolments
            if 'state_avg_updates' in policy_features:
                df.loc[state_mask, 'state_avg_updates'] = avg_updates
            if 'enrolment_deviation' in policy_features:
                df.loc[state_mask, 'enrolment_deviation'] = 0.0
            if 'update_deviation' in policy_features:
                df.loc[state_mask, 'update_deviation'] = 0.0
        
        return df
    
    def _generate_baseline_predictions(self, forecast_data: pd.DataFrame) -> Dict:
        """Generate baseline predictions without policy impact"""
        models = self.models
        
        # Get baseline features (exclude policy features)
        baseline_features = models.get('baseline_features', models['feature_columns'])
        
        # Prepare features for baseline models (exclude policy features)
        X = forecast_data.copy()
        
        # Align features with baseline model expectations
        X_baseline = X.reindex(columns=baseline_features, fill_value=0)
        
        # Validate feature alignment before prediction
        expected_features = len(baseline_features)
        if X_baseline.shape[1] != expected_features:
            logger.warning(f"Baseline feature mismatch: got {X_baseline.shape[1]}, expected {expected_features}")
            X_baseline = X_baseline.reindex(columns=baseline_features, fill_value=0)
        
        assert X_baseline.shape[1] == expected_features, \
            f"Baseline feature alignment failed: got {X_baseline.shape[1]}, expected {expected_features}"
        
        # Generate predictions
        enrolment_pred = models['baseline_enrolment'].predict(X_baseline)
        update_pred = models['baseline_update'].predict(X_baseline)
        
        return {
            'enrolments': enrolment_pred,
            'updates': update_pred,
            'dates': forecast_data['date'].values,
            'states': forecast_data['state'].values
        }
    
    def _generate_policy_predictions(self, forecast_data: pd.DataFrame) -> Dict:
        """Generate policy-influenced predictions"""
        models = self.models
        
        # Get policy features (includes all features including policy ones)
        policy_features = models.get('policy_features', models['feature_columns'])
        
        # Prepare all features including policy features
        X = forecast_data.copy()
        
        # Align features with policy model expectations
        X_policy = X.reindex(columns=policy_features, fill_value=0)
        
        # Validate feature alignment before prediction
        expected_features = len(policy_features)
        if X_policy.shape[1] != expected_features:
            logger.warning(f"Policy feature mismatch: got {X_policy.shape[1]}, expected {expected_features}")
            X_policy = X_policy.reindex(columns=policy_features, fill_value=0)
        
        assert X_policy.shape[1] == expected_features, \
            f"Policy feature alignment failed: got {X_policy.shape[1]}, expected {expected_features}"
        
        # Generate predictions
        enrolment_pred = models['policy_enrolment'].predict(X_policy)
        update_pred = models['policy_update'].predict(X_policy)
        
        return {
            'enrolments': enrolment_pred,
            'updates': update_pred,
            'dates': forecast_data['date'].values,
            'states': forecast_data['state'].values
        }
    
    def _calculate_impact(self, baseline_pred: Dict, policy_pred: Dict, 
                         forecast_data: pd.DataFrame, compliance_level: float) -> pd.DataFrame:
        """Calculate incremental impact of policy"""
        
        # Calculate raw impact
        enrolment_impact = policy_pred['enrolments'] - baseline_pred['enrolments']
        update_impact = policy_pred['updates'] - baseline_pred['updates']
        
        # Apply compliance level adjustment
        enrolment_impact *= compliance_level
        update_impact *= compliance_level
        
        # Create impact dataframe
        impact_df = pd.DataFrame({
            'date': forecast_data['date'],
            'state': forecast_data['state'],
            'enrolment_impact': enrolment_impact,
            'update_impact': update_impact,
            'total_impact': enrolment_impact + update_impact,
            'baseline_enrolments': baseline_pred['enrolments'],
            'baseline_updates': baseline_pred['updates'],
            'policy_enrolments': policy_pred['enrolments'],
            'policy_updates': policy_pred['updates']
        })
        
        return impact_df
    
    def _compile_results(self, impact_data: pd.DataFrame, forecast_data: pd.DataFrame, 
                        policy_date: str, forecast_days: int) -> Dict:
        """Compile comprehensive results"""
        
        # Summary metrics
        total_enrolment_impact = impact_data['enrolment_impact'].sum()
        total_update_impact = impact_data['update_impact'].sum()
        total_people_affected = total_enrolment_impact + total_update_impact
        
        # Daily impact aggregation
        daily_impact = impact_data.groupby('date').agg({
            'enrolment_impact': 'sum',
            'update_impact': 'sum',
            'total_impact': 'sum'
        }).reset_index()
        
        daily_impact['date'] = daily_impact['date'].dt.strftime('%Y-%m-%d')
        
        # Regional impact aggregation
        regional_impact = impact_data.groupby('state').agg({
            'enrolment_impact': 'sum',
            'update_impact': 'sum',
            'total_impact': 'sum'
        }).reset_index()
        
        # Sort by total impact
        regional_impact = regional_impact.sort_values('total_impact', ascending=False)
        
        # Peak analysis
        peak_day = daily_impact.loc[daily_impact['total_impact'].idxmax()]
        
        # Risk assessment
        high_impact_states = regional_impact[regional_impact['total_impact'] > 
                                          regional_impact['total_impact'].quantile(0.75)]
        
        return {
            'summary': {
                'total_people_affected': int(total_people_affected),
                'total_enrolment_impact': int(total_enrolment_impact),
                'total_update_impact': int(total_update_impact),
                'average_daily_impact': int(total_people_affected / forecast_days),
                'policy_date': policy_date,
                'forecast_days': forecast_days
            },
            'daily_impact': daily_impact.to_dict('records'),
            'regional_impact': {
                'by_state': regional_impact.to_dict('records'),
                'top_10_states': regional_impact.head(10).to_dict('records'),
                'total_impact': regional_impact.set_index('state')['total_impact'].to_dict(),
                'enrolment_impact': regional_impact.set_index('state')['enrolment_impact'].to_dict(),
                'update_impact': regional_impact.set_index('state')['update_impact'].to_dict()
            },
            'peak_analysis': {
                'peak_date': peak_day['date'],
                'peak_volume': int(peak_day['total_impact']),
                'peak_enrolments': int(peak_day['enrolment_impact']),
                'peak_updates': int(peak_day['update_impact'])
            },
            'risk_assessment': {
                'high_impact_states': high_impact_states['state'].tolist(),
                'states_at_risk': len(high_impact_states),
                'risk_level': 'High' if len(high_impact_states) > 10 else 'Medium' if len(high_impact_states) > 5 else 'Low'
            }
        }