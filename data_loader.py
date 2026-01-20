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
        
        # Clean and standardize state names
        df['state'] = df['state'].astype(str).str.strip()
        
        # Remove rows where state is numeric or too short
        df = df[df['state'].str.len() > 2]
        df = df[~df['state'].str.isdigit()]
        df = df[df['state'].notna()]
        df = df[df['state'] != '']
        df = df[df['state'] != 'nan']
        
        # Official list of 28 States + 8 UTs
        # Standardize to exact official names (case-insensitive mapping)
        state_mapping = {
            # States (28)
            'andhra pradesh': 'Andhra Pradesh',
            'arunachal pradesh': 'Arunachal Pradesh',
            'assam': 'Assam',
            'bihar': 'Bihar',
            'chhattisgarh': 'Chhattisgarh',
            'goa': 'Goa',
            'gujarat': 'Gujarat',
            'haryana': 'Haryana',
            'himachal pradesh': 'Himachal Pradesh',
            'jharkhand': 'Jharkhand',
            'karnataka': 'Karnataka',
            'kerala': 'Kerala',
            'madhya pradesh': 'Madhya Pradesh',
            'maharashtra': 'Maharashtra',
            'manipur': 'Manipur',
            'meghalaya': 'Meghalaya',
            'mizoram': 'Mizoram',
            'nagaland': 'Nagaland',
            'odisha': 'Odisha',
            'orissa': 'Odisha',  # Old name
            'punjab': 'Punjab',
            'rajasthan': 'Rajasthan',
            'sikkim': 'Sikkim',
            'tamil nadu': 'Tamil Nadu',
            'tamilnadu': 'Tamil Nadu',
            'telangana': 'Telangana',
            'tripura': 'Tripura',
            'uttar pradesh': 'Uttar Pradesh',
            'uttarakhand': 'Uttarakhand',
            'uttaranchal': 'Uttarakhand',  # Old name
            'west bengal': 'West Bengal',
            'west  bengal': 'West Bengal',
            'west bangal': 'West Bengal',
            'westbengal': 'West Bengal',
            
            # Union Territories (8)
            'andaman and nicobar islands': 'Andaman and Nicobar Islands',
            'andaman & nicobar islands': 'Andaman and Nicobar Islands',
            'andaman and nicobar': 'Andaman and Nicobar Islands',
            'chandigarh': 'Chandigarh',
            'dadra and nagar haveli and daman and diu': 'Dadra and Nagar Haveli and Daman and Diu',
            'dadra and nagar haveli': 'Dadra and Nagar Haveli and Daman and Diu',
            'dadra & nagar haveli': 'Dadra and Nagar Haveli and Daman and Diu',
            'daman and diu': 'Dadra and Nagar Haveli and Daman and Diu',
            'daman & diu': 'Dadra and Nagar Haveli and Daman and Diu',
            'the dadra and nagar haveli and daman and diu': 'Dadra and Nagar Haveli and Daman and Diu',
            'delhi': 'Delhi',
            'delhi (national capital territory)': 'Delhi',
            'national capital territory of delhi': 'Delhi',
            'nct of delhi': 'Delhi',
            'jammu and kashmir': 'Jammu and Kashmir',
            'jammu & kashmir': 'Jammu and Kashmir',
            'jammu and kashmir': 'Jammu and Kashmir',
            'ladakh': 'Ladakh',
            'lakshadweep': 'Lakshadweep',
            'puducherry': 'Puducherry',
            'pondicherry': 'Puducherry',  # Old name
        }
        
        # Apply mapping (case-insensitive)
        df['state_lower'] = df['state'].str.lower()
        df['state'] = df['state_lower'].map(state_mapping)
        
        # Remove rows where state couldn't be mapped (invalid states)
        df = df[df['state'].notna()]
        df = df.drop('state_lower', axis=1)
        
        # Calculate total enrolments
        df['total_enrolments'] = df['age_0_5'] + df['age_5_17'] + df['age_18_greater']
        
        # Aggregate by date and state
        agg_df = df.groupby(['date', 'state']).agg({
            'total_enrolments': 'sum',
            'age_0_5': 'sum',
            'age_5_17': 'sum',
            'age_18_greater': 'sum',
            'district': 'count'
        }).reset_index()
        
        agg_df.rename(columns={'district': 'num_districts'}, inplace=True)
        
        return agg_df
    
    def clean_and_aggregate_updates(self, bio_df: pd.DataFrame, demo_df: pd.DataFrame) -> pd.DataFrame:
        """Clean and aggregate update data (biometric + demographic)"""
        
        # Official list of 28 States + 8 UTs - Standardization mapping
        state_mapping = {
            # States (28)
            'andhra pradesh': 'Andhra Pradesh',
            'arunachal pradesh': 'Arunachal Pradesh',
            'assam': 'Assam',
            'bihar': 'Bihar',
            'chhattisgarh': 'Chhattisgarh',
            'goa': 'Goa',
            'gujarat': 'Gujarat',
            'haryana': 'Haryana',
            'himachal pradesh': 'Himachal Pradesh',
            'jharkhand': 'Jharkhand',
            'karnataka': 'Karnataka',
            'kerala': 'Kerala',
            'madhya pradesh': 'Madhya Pradesh',
            'maharashtra': 'Maharashtra',
            'manipur': 'Manipur',
            'meghalaya': 'Meghalaya',
            'mizoram': 'Mizoram',
            'nagaland': 'Nagaland',
            'odisha': 'Odisha',
            'orissa': 'Odisha',
            'punjab': 'Punjab',
            'rajasthan': 'Rajasthan',
            'sikkim': 'Sikkim',
            'tamil nadu': 'Tamil Nadu',
            'tamilnadu': 'Tamil Nadu',
            'telangana': 'Telangana',
            'tripura': 'Tripura',
            'uttar pradesh': 'Uttar Pradesh',
            'uttarakhand': 'Uttarakhand',
            'uttaranchal': 'Uttarakhand',
            'west bengal': 'West Bengal',
            'west  bengal': 'West Bengal',
            'west bangal': 'West Bengal',
            'westbengal': 'West Bengal',
            
            # Union Territories (8)
            'andaman and nicobar islands': 'Andaman and Nicobar Islands',
            'andaman & nicobar islands': 'Andaman and Nicobar Islands',
            'andaman and nicobar': 'Andaman and Nicobar Islands',
            'chandigarh': 'Chandigarh',
            'dadra and nagar haveli and daman and diu': 'Dadra and Nagar Haveli and Daman and Diu',
            'dadra and nagar haveli': 'Dadra and Nagar Haveli and Daman and Diu',
            'dadra & nagar haveli': 'Dadra and Nagar Haveli and Daman and Diu',
            'daman and diu': 'Dadra and Nagar Haveli and Daman and Diu',
            'daman & diu': 'Dadra and Nagar Haveli and Daman and Diu',
            'the dadra and nagar haveli and daman and diu': 'Dadra and Nagar Haveli and Daman and Diu',
            'delhi': 'Delhi',
            'delhi (national capital territory)': 'Delhi',
            'national capital territory of delhi': 'Delhi',
            'nct of delhi': 'Delhi',
            'jammu and kashmir': 'Jammu and Kashmir',
            'jammu & kashmir': 'Jammu and Kashmir',
            'ladakh': 'Ladakh',
            'lakshadweep': 'Lakshadweep',
            'puducherry': 'Puducherry',
            'pondicherry': 'Puducherry',
        }
        
        # Process biometric updates
        bio_df['date'] = pd.to_datetime(bio_df['date'], format='%d-%m-%Y')
        
        # Clean and standardize state names
        bio_df['state'] = bio_df['state'].astype(str).str.strip()
        bio_df = bio_df[bio_df['state'].str.len() > 2]
        bio_df = bio_df[~bio_df['state'].str.isdigit()]
        bio_df = bio_df[bio_df['state'].notna()]
        bio_df = bio_df[bio_df['state'] != '']
        bio_df = bio_df[bio_df['state'] != 'nan']
        
        # Apply mapping
        bio_df['state_lower'] = bio_df['state'].str.lower()
        bio_df['state'] = bio_df['state_lower'].map(state_mapping)
        bio_df = bio_df[bio_df['state'].notna()]  # Remove unmapped states
        bio_df = bio_df.drop('state_lower', axis=1)
        
        bio_df['total_bio_updates'] = bio_df['bio_age_5_17'] + bio_df['bio_age_17_']
        
        bio_agg = bio_df.groupby(['date', 'state']).agg({
            'total_bio_updates': 'sum',
            'bio_age_5_17': 'sum',
            'bio_age_17_': 'sum'
        }).reset_index()
        
        # Process demographic updates
        demo_df['date'] = pd.to_datetime(demo_df['date'], format='%d-%m-%Y')
        
        # Clean and standardize state names
        demo_df['state'] = demo_df['state'].astype(str).str.strip()
        demo_df = demo_df[demo_df['state'].str.len() > 2]
        demo_df = demo_df[~demo_df['state'].str.isdigit()]
        demo_df = demo_df[demo_df['state'].notna()]
        demo_df = demo_df[demo_df['state'] != '']
        demo_df = demo_df[demo_df['state'] != 'nan']
        
        # Apply mapping
        demo_df['state_lower'] = demo_df['state'].str.lower()
        demo_df['state'] = demo_df['state_lower'].map(state_mapping)
        demo_df = demo_df[demo_df['state'].notna()]  # Remove unmapped states
        demo_df = demo_df.drop('state_lower', axis=1)
        
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
        
        # FINAL VALIDATION: Only keep official 28 states + 8 UTs
        valid_states = {
            'Andhra Pradesh', 'Arunachal Pradesh', 'Assam', 'Bihar', 'Chhattisgarh',
            'Goa', 'Gujarat', 'Haryana', 'Himachal Pradesh', 'Jharkhand',
            'Karnataka', 'Kerala', 'Madhya Pradesh', 'Maharashtra', 'Manipur',
            'Meghalaya', 'Mizoram', 'Nagaland', 'Odisha', 'Punjab',
            'Rajasthan', 'Sikkim', 'Tamil Nadu', 'Telangana', 'Tripura',
            'Uttar Pradesh', 'Uttarakhand', 'West Bengal',
            'Andaman and Nicobar Islands', 'Chandigarh',
            'Dadra and Nagar Haveli and Daman and Diu', 'Delhi',
            'Jammu and Kashmir', 'Ladakh', 'Lakshadweep', 'Puducherry'
        }
        
        # Filter to keep ONLY valid states
        master = master[master['state'].isin(valid_states)]
        
        # Sort by date and state
        master.sort_values(['date', 'state'], inplace=True)
        master.reset_index(drop=True, inplace=True)
        
        print(f"\nMaster dataset created: {len(master)} records")
        print(f"Date range: {master['date'].min()} to {master['date'].max()}")
        print(f"States: {master['state'].nunique()}")
        print(f"Valid states in data: {sorted(master['state'].unique())}")
        
        return master

if __name__ == "__main__":
    loader = AadhaarDataLoader()
    master_df = loader.create_master_dataset()
    master_df.to_csv("master_aadhaar_data.csv", index=False)
    print("\nMaster dataset saved to master_aadhaar_data.csv")
