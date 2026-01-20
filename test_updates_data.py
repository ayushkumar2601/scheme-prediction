"""
Quick test to check if update data exists in the master dataset
"""

import pandas as pd

# Load master data
try:
    master_data = pd.read_csv("master_aadhaar_data.csv")
    print("Master data loaded successfully")
    print(f"Total records: {len(master_data)}")
    print(f"\nColumns: {list(master_data.columns)}")
    
    # Check for update columns
    update_cols = [col for col in master_data.columns if 'update' in col.lower()]
    print(f"\nUpdate-related columns: {update_cols}")
    
    # Check if updates have non-zero values
    if 'total_updates' in master_data.columns:
        total_updates = master_data['total_updates'].sum()
        non_zero_updates = (master_data['total_updates'] > 0).sum()
        print(f"\nTotal updates in dataset: {total_updates:,.0f}")
        print(f"Records with non-zero updates: {non_zero_updates} / {len(master_data)}")
        print(f"Percentage with updates: {(non_zero_updates/len(master_data)*100):.1f}%")
        
        # Show sample records with updates
        print("\nSample records with updates:")
        sample = master_data[master_data['total_updates'] > 0].head(5)
        print(sample[['date', 'state', 'total_enrolments', 'total_updates']])
    else:
        print("\nWARNING: 'total_updates' column not found!")
        
    # Check enrolments for comparison
    if 'total_enrolments' in master_data.columns:
        total_enrolments = master_data['total_enrolments'].sum()
        print(f"\nTotal enrolments in dataset: {total_enrolments:,.0f}")
        print(f"Ratio of updates to enrolments: {(total_updates/total_enrolments*100):.2f}%")
        
except FileNotFoundError:
    print("ERROR: master_aadhaar_data.csv not found!")
    print("Please run data_loader.py first to create the master dataset")
except Exception as e:
    print(f"ERROR: {e}")
    import traceback
    traceback.print_exc()
