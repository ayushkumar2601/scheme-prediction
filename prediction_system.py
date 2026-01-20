"""
Policy Impact Prediction System
Main interface for predicting policy impacts
"""

import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from typing import Dict, Tuple
import warnings
warnings.filterwarnings('ignore')

from data_loader import AadhaarDataLoader
from feature_engineering import FeatureEngineer
from baseline_model import BaselineModel
from policy_impact_model import PolicyImpactModel

class PolicyImpactPredictor:
    """Main system for predicting policy impacts"""
    
    def __init__(self):
        self.baseline_model = BaselineModel()
        self.policy_model = PolicyImpactModel()
        self.master_data = None
        
    def load_and_prepare_data(self, use_cached: bool = True):
        """Load and prepare all data"""
        if use_cached:
            try:
                self.master_data = pd.read_csv("master_aadhaar_data.csv")
                print("Loaded cached master data")
                return
            except FileNotFoundError:
                pass
        
        print("Loading raw data...")
        loader = AadhaarDataLoader()
        self.master_data = loader.create_master_dataset()
        self.master_data.to_csv("master_aadhaar_data.csv", index=False)
    
    def train_baseline(self):
        """Train baseline models"""
        print("\n=== Training Baseline Models ===")
        
        # Create features without policy
        fe = FeatureEngineer(self.master_data)
        featured_data = fe.create_all_features(policy_date=None)
        
        self.baseline_model.train_enrolment_model(featured_data)
        self.baseline_model.train_update_model(featured_data)
        self.baseline_model.save_models()
    
    def train_policy_model(self, policy_date: str):
        """Train policy impact model"""
        print(f"\n=== Training Policy Impact Model (Policy Date: {policy_date}) ===")
        
        # Create features with policy
        fe = FeatureEngineer(self.master_data)
        featured_data = fe.create_all_features(policy_date=policy_date)
        
        self.policy_model.train_impact_models(featured_data, policy_date)
        self.policy_model.save_models()
    
    def predict_policy_impact(self, policy_date: str, forecast_days: int = 60) -> Dict:
        """
        Predict impact of a policy
        
        Args:
            policy_date: Date when policy will be implemented (YYYY-MM-DD)
            forecast_days: Number of days to forecast after policy
            
        Returns:
            Dictionary with predictions and analysis
        """
        print(f"\n=== Predicting Policy Impact ===")
        print(f"Policy Date: {policy_date}")
        print(f"Forecast Period: {forecast_days} days")
        
        # Load models
        try:
            self.baseline_model.load_models()
            self.policy_model.load_models()
        except:
            print("Models not found. Training new models...")
            self.train_baseline()
            self.train_policy_model(policy_date)
        
        # Create forecast dataset
        policy_dt = pd.to_datetime(policy_date)
        
        # Get date range for forecast
        max_date = self.master_data['date'].max()
        if pd.to_datetime(max_date) < policy_dt:
            # Need to create future dates
            forecast_dates = pd.date_range(
                start=policy_dt,
                periods=forecast_days,
                freq='D'
            )
        else:
            # Use existing data around policy date
            forecast_dates = pd.date_range(
                start=policy_dt - timedelta(days=30),
                end=policy_dt + timedelta(days=forecast_days),
                freq='D'
            )
        
        # Create forecast dataframe
        states = self.master_data['state'].unique()
        forecast_data = []
        
        for date in forecast_dates:
            for state in states:
                # Get historical average for this state
                state_data = self.master_data[self.master_data['state'] == state]
                avg_enrol = state_data['total_enrolments'].mean()
                avg_update = state_data['total_updates'].mean()
                
                forecast_data.append({
                    'date': date,
                    'state': state,
                    'total_enrolments': avg_enrol,
                    'total_updates': avg_update,
                    'num_districts': state_data['num_districts'].mean()
                })
        
        forecast_df = pd.DataFrame(forecast_data)
        
        # Add features
        fe = FeatureEngineer(forecast_df)
        forecast_featured = fe.create_all_features(policy_date=policy_date)
        
        # Get baseline predictions
        baseline_pred = self.baseline_model.predict_baseline(forecast_featured)
        
        # Get policy impact predictions
        impact_pred = self.policy_model.calculate_policy_impact(forecast_featured, baseline_pred)
        
        # Analyze results
        results = self._analyze_predictions(impact_pred, policy_date, forecast_days)
        
        return results
    
    def _analyze_predictions(self, predictions: pd.DataFrame, policy_date: str, 
                           forecast_days: int) -> Dict:
        """Analyze prediction results"""
        policy_dt = pd.to_datetime(policy_date)
        
        # Filter post-policy data
        post_policy = predictions[predictions['date'] >= policy_dt].copy()
        
        if len(post_policy) == 0:
            return {
                'error': 'No post-policy data available',
                'predictions': predictions
            }
        
        # Overall impact
        total_enrolment_impact = post_policy['enrolment_impact'].sum()
        total_update_impact = post_policy['update_impact'].sum()
        total_people_affected = total_enrolment_impact + total_update_impact
        
        # Regional impact
        regional_impact = post_policy.groupby('state').agg({
            'enrolment_impact': 'sum',
            'update_impact': 'sum',
            'total_impact': 'sum'
        }).sort_values('total_impact', ascending=False)
        
        # Time-series impact
        daily_impact = post_policy.groupby('date').agg({
            'enrolment_impact': 'sum',
            'update_impact': 'sum',
            'total_impact': 'sum'
        }).reset_index()
        
        # Peak impact day
        peak_day = daily_impact.loc[daily_impact['total_impact'].idxmax()]
        
        # Duration analysis
        significant_impact_days = len(daily_impact[daily_impact['total_impact'] > 
                                                   daily_impact['total_impact'].mean()])
        
        results = {
            'summary': {
                'policy_date': policy_date,
                'forecast_days': forecast_days,
                'total_people_affected': int(total_people_affected),
                'total_enrolment_increase': int(total_enrolment_impact),
                'total_update_increase': int(total_update_impact),
                'peak_impact_date': peak_day['date'].strftime('%Y-%m-%d'),
                'peak_impact_volume': int(peak_day['total_impact']),
                'significant_impact_duration_days': significant_impact_days
            },
            'regional_impact': regional_impact.to_dict(),
            'daily_impact': daily_impact,
            'full_predictions': predictions
        }
        
        return results
    
    def generate_report(self, results: Dict, output_file: str = "policy_impact_report.txt"):
        """Generate human-readable report"""
        with open(output_file, 'w') as f:
            f.write("=" * 80 + "\n")
            f.write("AADHAAR POLICY IMPACT PREDICTION REPORT\n")
            f.write("=" * 80 + "\n\n")
            
            summary = results['summary']
            
            f.write(f"Policy Implementation Date: {summary['policy_date']}\n")
            f.write(f"Forecast Period: {summary['forecast_days']} days\n\n")
            
            f.write("OVERALL IMPACT SUMMARY\n")
            f.write("-" * 80 + "\n")
            f.write(f"Total People Affected: {summary['total_people_affected']:,}\n")
            f.write(f"  - Additional Enrolments: {summary['total_enrolment_increase']:,}\n")
            f.write(f"  - Additional Updates: {summary['total_update_increase']:,}\n\n")
            
            f.write(f"Peak Impact Date: {summary['peak_impact_date']}\n")
            f.write(f"Peak Daily Volume: {summary['peak_impact_volume']:,} people\n")
            f.write(f"Duration of Significant Impact: {summary['significant_impact_duration_days']} days\n\n")
            
            f.write("TOP 10 MOST AFFECTED STATES\n")
            f.write("-" * 80 + "\n")
            
            regional = results['regional_impact']
            top_states = sorted(regional['total_impact'].items(), 
                              key=lambda x: x[1], reverse=True)[:10]
            
            for i, (state, impact) in enumerate(top_states, 1):
                enrol = regional['enrolment_impact'][state]
                update = regional['update_impact'][state]
                f.write(f"{i}. {state}: {int(impact):,} people\n")
                f.write(f"   Enrolments: {int(enrol):,} | Updates: {int(update):,}\n")
            
            f.write("\n" + "=" * 80 + "\n")
        
        print(f"\nReport saved to {output_file}")

if __name__ == "__main__":
    predictor = PolicyImpactPredictor()
    
    # Load data
    predictor.load_and_prepare_data()
    
    # Example: Predict impact of a policy on April 1, 2025
    results = predictor.predict_policy_impact(
        policy_date="2025-04-01",
        forecast_days=60
    )
    
    # Generate report
    predictor.generate_report(results)
    
    print("\n=== SUMMARY ===")
    print(f"Total People Affected: {results['summary']['total_people_affected']:,}")
    print(f"Peak Impact Date: {results['summary']['peak_impact_date']}")
