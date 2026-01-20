"""
Data Loader Module for Aadhaar Policy Impact Prediction System
Handles loading, cleaning, and aggregating Aadhaar datasets
"""

import pandas as pd
import numpy as np
from pathlib import Path
from typing import List, Tuple
import glob

class AadhaarDataLoader:
    """Load and preprocess Aadhaar enrolment and update data"""
    
    def __init__(self, base_path: str = "."):
        self.base_path = Path(base_path)
        
    def load_enrolment_data(self) -> pd.DataFrame:
        """Load all enrolment CSV files and combine them"""
        pattern = str(self.base_path / "api_data_aadhar_enrolment" / "api_data_aadhar_enrolment" / "*.csv")
        files = glob.glob(pattern)
        
        dfs = []
        for file in files:
            df = pd.read_csv(file)
            dfs.append(df)
        
        combined = pd.concat(dfs, ignore_index=True)
        print(f"Loaded {len(combined)} enrolment records from {len(files)} files")
        return combined
    
    def load_biometric_data(self) -> pd.DataFrame:
        """Load all biometric update CSV files and combine them"""
        pattern = str(self.base_path / "api_data_aadhar_biometric" / "api_data_aadhar_biometric" / "*.csv")
        files = glob.glob(pattern)
        
        dfs = []
        for file in files:
            df = pd.read_csv(file)
            dfs.append(df)
        
        combined = pd.concat(dfs, ignore_index=True)
        print(f"Loaded {len(combined)} biometric update records from {len(files)} files")
        return combined
    
    def load_demographic_data(self) -> pd.DataFrame:
        """Load all demographic update CSV files and combine them"""
        pattern = str(self.base_path / "api_data_aadhar_demographic" / "api_data_aadhar_demographic" / "*.csv")
        files = glob.glob(pattern)
        
        dfs = []
        for file in files:
            df = pd.read_csv(file)
            dfs.append(df)
        
        combined = pd.concat(dfs, ignore_index=True)
        print(f"Loaded {len(combined)} demographic update records from {len(files)} files")
        return combined
    
    def clean_and_aggregate_enrolment(self, df: pd.DataFrame) -> pd.DataFrame:
        """Clean and aggregate enrolment data"""
        # Convert date to datetime
        df['date'] = pd.to_datetime(df['date'], format='%d-%m-%Y')
        
        # Calculate total enrolments
        df['total_enrolments'] = df['age_0_5'] + df['age_5_17'] + df['age_18_greater']
        
        # Aggregate by date and state
        agg_df = df.groupby(['date', 'state']).agg({
            'total_enrolments': 'sum',
            'age_0_5': 'sum',
            'age_5_17': 'sum',
            'age_18_greater': 'sum',
            'district': 'count'  # Count of districts
        }).reset_index()
        
        agg_df.rename(columns={'district': 'num_districts'}, inplace=True)
        
        return agg_df
    
    def clean_and_aggregate_updates(self, bio_df: pd.DataFrame, demo_df: pd.DataFrame) -> pd.DataFrame:
        """Clean and aggregate update data (biometric + demographic)"""
        # Process biometric updates
        bio_df['date'] = pd.to_datetime(bio_df['date'], format='%d-%m-%Y')
        bio_df['total_bio_updates'] = bio_df['bio_age_5_17'] + bio_df['bio_age_17_']
        
        bio_agg = bio_df.groupby(['date', 'state']).agg({
            'total_bio_updates': 'sum',
            'bio_age_5_17': 'sum',
            'bio_age_17_': 'sum'
        }).reset_index()
        
        # Process demographic updates
        demo_df['date'] = pd.to_datetime(demo_df['date'], format='%d-%m-%Y')
        demo_df['total_demo_updates'] = demo_df['demo_age_5_17'] + demo_df['demo_age_17_']
        
        demo_agg = demo_df.groupby(['date', 'state']).agg({
            'total_demo_updates': 'sum',
            'demo_age_5_17': 'sum',
            'demo_age_17_': 'sum'
        }).reset_index()
        
        # Merge biometric and demographic
        updates = pd.merge(bio_agg, demo_agg, on=['date', 'state'], how='outer')
        updates.fillna(0, inplace=True)
        
        updates['total_updates'] = updates['total_bio_updates'] + updates['total_demo_updates']
        
        return updates
    
    def create_master_dataset(self) -> pd.DataFrame:
        """Create master dataset combining enrolments and updates"""
        print("Loading data...")
        enrol_raw = self.load_enrolment_data()
        bio_raw = self.load_biometric_data()
        demo_raw = self.load_demographic_data()
        
        print("\nCleaning and aggregating...")
        enrol_clean = self.clean_and_aggregate_enrolment(enrol_raw)
        updates_clean = self.clean_and_aggregate_updates(bio_raw, demo_raw)
        
        print("\nMerging datasets...")
        master = pd.merge(enrol_clean, updates_clean, on=['date', 'state'], how='outer')
        master.fillna(0, inplace=True)
        
        # Sort by date and state
        master.sort_values(['date', 'state'], inplace=True)
        master.reset_index(drop=True, inplace=True)
        
        print(f"\nMaster dataset created: {len(master)} records")
        print(f"Date range: {master['date'].min()} to {master['date'].max()}")
        print(f"States: {master['state'].nunique()}")
        
        return master

if __name__ == "__main__":
    loader = AadhaarDataLoader()
    master_df = loader.create_master_dataset()
    master_df.to_csv("master_aadhaar_data.csv", index=False)
    print("\nMaster dataset saved to master_aadhaar_data.csv")
