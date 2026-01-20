"""
Feature Engineering Module for Policy Impact Prediction
Creates time-series features, lag features, and policy indicators
"""

import pandas as pd
import numpy as np
from typing import List, Dict

class FeatureEngineer:
    """Create features for policy impact prediction"""
    
    def __init__(self, df: pd.DataFrame):
        self.df = df.copy()
        self.df['date'] = pd.to_datetime(self.df['date'])
        
    def add_temporal_features(self) -> pd.DataFrame:
        """Add time-based features"""
        df = self.df.copy()
        
        df['year'] = df['date'].dt.year
        df['month'] = df['date'].dt.month
        df['day'] = df['date'].dt.day
        df['day_of_week'] = df['date'].dt.dayofweek
        df['week_of_year'] = df['date'].dt.isocalendar().week
        df['is_weekend'] = df['day_of_week'].isin([5, 6]).astype(int)
        
        return df
    
    def add_lag_features(self, columns: List[str], lags: List[int] = [1, 7, 14, 30]) -> pd.DataFrame:
        """Add lag features for specified columns"""
        df = self.df.copy()
        
        for col in columns:
            for lag in lags:
                df[f'{col}_lag_{lag}'] = df.groupby('state')[col].shift(lag)
        
        return df
    
    def add_rolling_features(self, columns: List[str], windows: List[int] = [7, 14, 30]) -> pd.DataFrame:
        """Add rolling average and std features"""
        df = self.df.copy()
        
        for col in columns:
            for window in windows:
                df[f'{col}_rolling_mean_{window}'] = df.groupby('state')[col].transform(
                    lambda x: x.rolling(window=window, min_periods=1).mean()
                )
                df[f'{col}_rolling_std_{window}'] = df.groupby('state')[col].transform(
                    lambda x: x.rolling(window=window, min_periods=1).std()
                )
        
        return df
    
    def add_growth_features(self, columns: List[str]) -> pd.DataFrame:
        """Add growth rate features"""
        df = self.df.copy()
        
        for col in columns:
            # Day-over-day growth
            df[f'{col}_growth'] = df.groupby('state')[col].pct_change()
            
            # Week-over-week growth
            df[f'{col}_growth_7d'] = df.groupby('state')[col].pct_change(periods=7)
            
            # Replace inf with nan
            df[f'{col}_growth'].replace([np.inf, -np.inf], np.nan, inplace=True)
            df[f'{col}_growth_7d'].replace([np.inf, -np.inf], np.nan, inplace=True)
        
        return df
    
    def add_policy_features(self, policy_date: str) -> pd.DataFrame:
        """Add policy-related features"""
        df = self.df.copy()
        policy_dt = pd.to_datetime(policy_date)
        
        # Binary indicator
        df['policy_active'] = (df['date'] >= policy_dt).astype(int)
        
        # Days since/until policy
        df['days_from_policy'] = (df['date'] - policy_dt).dt.days
        
        # Pre/post policy periods
        df['pre_policy_30d'] = ((df['date'] >= policy_dt - pd.Timedelta(days=30)) & 
                                 (df['date'] < policy_dt)).astype(int)
        df['post_policy_30d'] = ((df['date'] >= policy_dt) & 
                                  (df['date'] < policy_dt + pd.Timedelta(days=30))).astype(int)
        df['post_policy_60d'] = ((df['date'] >= policy_dt) & 
                                  (df['date'] < policy_dt + pd.Timedelta(days=60))).astype(int)
        
        return df
    
    def add_state_features(self) -> pd.DataFrame:
        """Add state-level aggregated features"""
        df = self.df.copy()
        
        # State average enrolments and updates
        state_avg = df.groupby('state')[['total_enrolments', 'total_updates']].transform('mean')
        df['state_avg_enrolments'] = state_avg['total_enrolments']
        df['state_avg_updates'] = state_avg['total_updates']
        
        # Deviation from state average
        df['enrolment_deviation'] = df['total_enrolments'] - df['state_avg_enrolments']
        df['update_deviation'] = df['total_updates'] - df['state_avg_updates']
        
        return df
    
    def create_all_features(self, policy_date: str = None) -> pd.DataFrame:
        """Create all features at once"""
        print("Adding temporal features...")
        df = self.add_temporal_features()
        self.df = df
        
        print("Adding lag features...")
        df = self.add_lag_features(['total_enrolments', 'total_updates'])
        self.df = df
        
        print("Adding rolling features...")
        df = self.add_rolling_features(['total_enrolments', 'total_updates'])
        self.df = df
        
        print("Adding growth features...")
        df = self.add_growth_features(['total_enrolments', 'total_updates'])
        self.df = df
        
        print("Adding state features...")
        df = self.add_state_features()
        self.df = df
        
        if policy_date:
            print(f"Adding policy features (policy date: {policy_date})...")
            df = self.add_policy_features(policy_date)
            self.df = df
        
        # Fill NaN values
        df.fillna(0, inplace=True)
        
        print(f"Feature engineering complete. Total features: {len(df.columns)}")
        return df

if __name__ == "__main__":
    # Load master data
    master_df = pd.read_csv("master_aadhaar_data.csv")
    
    # Create features
    fe = FeatureEngineer(master_df)
    featured_df = fe.create_all_features()
    
    featured_df.to_csv("featured_aadhaar_data.csv", index=False)
    print("\nFeatured dataset saved to featured_aadhaar_data.csv")
