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
                forecast_data.append({
                    'date': date,
                    'state': state,
                    'policy_date': policy_dt,
                    'days_from_policy': (date - policy_dt).days,
                    'policy_active': 1 if date >= policy_dt else 0
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
        expected_features = models['feature_columns']
        
        # For production, we'll use simplified features based on recent averages
        # In a full implementation, you'd calculate these from historical data
        
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
            
            # Set lag features to recent averages
            if 'total_enrolments_lag_1' in expected_features:
                df.loc[state_mask, 'total_enrolments_lag_1'] = avg_enrolments
            if 'total_enrolments_lag_7' in expected_features:
                df.loc[state_mask, 'total_enrolments_lag_7'] = avg_enrolments
            if 'total_enrolments_lag_30' in expected_features:
                df.loc[state_mask, 'total_enrolments_lag_30'] = avg_enrolments
            if 'total_updates_lag_1' in expected_features:
                df.loc[state_mask, 'total_updates_lag_1'] = avg_updates
            if 'total_updates_lag_7' in expected_features:
                df.loc[state_mask, 'total_updates_lag_7'] = avg_updates
            if 'total_updates_lag_30' in expected_features:
                df.loc[state_mask, 'total_updates_lag_30'] = avg_updates
            
            # Set rolling averages
            if 'total_enrolments_rolling_mean_7' in expected_features:
                df.loc[state_mask, 'total_enrolments_rolling_mean_7'] = avg_enrolments
            if 'total_enrolments_rolling_mean_30' in expected_features:
                df.loc[state_mask, 'total_enrolments_rolling_mean_30'] = avg_enrolments
            if 'total_updates_rolling_mean_7' in expected_features:
                df.loc[state_mask, 'total_updates_rolling_mean_7'] = avg_updates
            if 'total_updates_rolling_mean_30' in expected_features:
                df.loc[state_mask, 'total_updates_rolling_mean_30'] = avg_updates
            
            # Set rolling standard deviations
            if 'total_enrolments_rolling_std_7' in expected_features:
                df.loc[state_mask, 'total_enrolments_rolling_std_7'] = avg_enrolments * 0.1
            if 'total_enrolments_rolling_std_30' in expected_features:
                df.loc[state_mask, 'total_enrolments_rolling_std_30'] = avg_enrolments * 0.15
            if 'total_updates_rolling_std_7' in expected_features:
                df.loc[state_mask, 'total_updates_rolling_std_7'] = avg_updates * 0.1
            if 'total_updates_rolling_std_30' in expected_features:
                df.loc[state_mask, 'total_updates_rolling_std_30'] = avg_updates * 0.15
            
            # Set growth features
            if 'enrolment_growth_1d' in expected_features:
                df.loc[state_mask, 'enrolment_growth_1d'] = 0.02  # 2% growth
            if 'update_growth_1d' in expected_features:
                df.loc[state_mask, 'update_growth_1d'] = 0.01     # 1% growth
            if 'enrolment_growth_7d' in expected_features:
                df.loc[state_mask, 'enrolment_growth_7d'] = 0.05  # 5% weekly growth
            if 'update_growth_7d' in expected_features:
                df.loc[state_mask, 'update_growth_7d'] = 0.03     # 3% weekly growth
            
            # Set state-level features
            if 'state_avg_enrolments' in expected_features:
                df.loc[state_mask, 'state_avg_enrolments'] = avg_enrolments
            if 'state_avg_updates' in expected_features:
                df.loc[state_mask, 'state_avg_updates'] = avg_updates
            if 'enrolment_deviation' in expected_features:
                df.loc[state_mask, 'enrolment_deviation'] = 0.0
            if 'update_deviation' in expected_features:
                df.loc[state_mask, 'update_deviation'] = 0.0
            
            # Set seasonal features
            if 'seasonal_enrolment' in expected_features:
                df.loc[state_mask, 'seasonal_enrolment'] = avg_enrolments * 1.1
            if 'seasonal_update' in expected_features:
                df.loc[state_mask, 'seasonal_update'] = avg_updates * 1.1
            
            # Set trend features
            if 'trend_enrolment' in expected_features:
                df.loc[state_mask, 'trend_enrolment'] = avg_enrolments * 1.05
            if 'trend_update' in expected_features:
                df.loc[state_mask, 'trend_update'] = avg_updates * 1.05
        
        return df
    
    def _generate_baseline_predictions(self, forecast_data: pd.DataFrame) -> Dict:
        """Generate baseline predictions without policy impact"""
        models = self.models
        
        # Prepare features (exclude policy features for baseline)
        feature_cols = [col for col in forecast_data.columns 
                       if col not in ['date', 'state', 'policy_date'] 
                       and 'policy' not in col.lower()]
        
        X = forecast_data[feature_cols].fillna(0)
        
        # Align features with trained models
        X_aligned = self.model_loader.align_features(X)
        
        # Validate feature alignment before prediction
        expected_features = len(models['feature_columns'])
        if X_aligned.shape[1] != expected_features:
            logger.warning(f"Feature mismatch: got {X_aligned.shape[1]}, expected {expected_features}")
            # Force alignment using reindex
            X_aligned = X_aligned.reindex(columns=models['feature_columns'], fill_value=0)
        
        assert X_aligned.shape[1] == expected_features, \
            f"Feature alignment failed: got {X_aligned.shape[1]}, expected {expected_features}"
        
        # Generate predictions
        enrolment_pred = models['baseline_enrolment'].predict(X_aligned)
        update_pred = models['baseline_update'].predict(X_aligned)
        
        return {
            'enrolments': enrolment_pred,
            'updates': update_pred,
            'dates': forecast_data['date'].values,
            'states': forecast_data['state'].values
        }
    
    def _generate_policy_predictions(self, forecast_data: pd.DataFrame) -> Dict:
        """Generate policy-influenced predictions"""
        models = self.models
        
        # Prepare all features including policy features
        feature_cols = [col for col in forecast_data.columns 
                       if col not in ['date', 'state', 'policy_date']]
        
        X = forecast_data[feature_cols].fillna(0)
        
        # Align features with trained models
        X_aligned = self.model_loader.align_features(X)
        
        # Validate feature alignment before prediction
        expected_features = len(models['feature_columns'])
        if X_aligned.shape[1] != expected_features:
            logger.warning(f"Feature mismatch: got {X_aligned.shape[1]}, expected {expected_features}")
            # Force alignment using reindex
            X_aligned = X_aligned.reindex(columns=models['feature_columns'], fill_value=0)
        
        assert X_aligned.shape[1] == expected_features, \
            f"Feature alignment failed: got {X_aligned.shape[1]}, expected {expected_features}"
        
        # Generate predictions
        enrolment_pred = models['policy_enrolment'].predict(X_aligned)
        update_pred = models['policy_update'].predict(X_aligned)
        
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