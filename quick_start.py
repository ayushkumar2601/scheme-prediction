"""
Quick Start Script
Minimal example to get predictions quickly
"""

import warnings
warnings.filterwarnings('ignore')

print("Aadhaar Policy Impact Prediction - Quick Start")
print("=" * 60)

# Step 1: Load data
print("\n[1/4] Loading data...")
from data_loader import AadhaarDataLoader
loader = AadhaarDataLoader()
master_data = loader.create_master_dataset()
print(f"✓ Loaded {len(master_data)} records")

# Step 2: Create features
print("\n[2/4] Creating features...")
from feature_engineering import FeatureEngineer
fe = FeatureEngineer(master_data)
featured_data = fe.create_all_features()
print(f"✓ Created {len(featured_data.columns)} features")

# Step 3: Train models
print("\n[3/4] Training models...")
from baseline_model import BaselineModel
baseline = BaselineModel()
baseline.train_enrolment_model(featured_data)
baseline.train_update_model(featured_data)
print("✓ Models trained")

# Step 4: Predict
print("\n[4/4] Generating predictions...")
from prediction_system import PolicyImpactPredictor
predictor = PolicyImpactPredictor()
predictor.master_data = master_data
predictor.baseline_model = baseline

# Example policy date
POLICY_DATE = "2025-04-01"

# Add policy features and train policy model
fe_policy = FeatureEngineer(master_data)
featured_policy = fe_policy.create_all_features(policy_date=POLICY_DATE)

from policy_impact_model import PolicyImpactModel
policy_model = PolicyImpactModel()
policy_model.train_impact_models(featured_policy, POLICY_DATE)
predictor.policy_model = policy_model

# Generate predictions
results = predictor.predict_policy_impact(
    policy_date=POLICY_DATE,
    forecast_days=60
)

# Display results
print("\n" + "=" * 60)
print("RESULTS")
print("=" * 60)
summary = results['summary']
print(f"\nPolicy Date: {summary['policy_date']}")
print(f"Total People Affected: {summary['total_people_affected']:,}")
print(f"  - Enrolments: {summary['total_enrolment_increase']:,}")
print(f"  - Updates: {summary['total_update_increase']:,}")
print(f"\nPeak Date: {summary['peak_impact_date']}")
print(f"Peak Volume: {summary['peak_impact_volume']:,} people/day")
print(f"Impact Duration: {summary['significant_impact_duration_days']} days")

# Top 5 states
print("\nTop 5 Affected States:")
regional = results['regional_impact']
top_states = sorted(regional['total_impact'].items(), 
                   key=lambda x: x[1], reverse=True)[:5]
for i, (state, impact) in enumerate(top_states, 1):
    print(f"  {i}. {state}: {int(impact):,} people")

print("\n" + "=" * 60)
print("✓ Quick start complete!")
print("\nFor detailed analysis, run: python example_usage.py")
print("For full pipeline, run: python run_pipeline.py")
print("For interactive analysis, open: policy_impact_analysis.ipynb")
