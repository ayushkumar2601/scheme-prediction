"""
My Policy Prediction Template
Copy this file and modify the policy details below to get your predictions
"""

from prediction_system import PolicyImpactPredictor
from visualization import PolicyImpactVisualizer

# ============================================================================
# STEP 1: ADD YOUR POLICY DETAILS HERE
# ============================================================================

# Policy implementation date (format: "YYYY-MM-DD")
MY_POLICY_DATE = "2025-04-01"  # ← CHANGE THIS

# How many days to forecast after policy
FORECAST_DAYS = 60  # ← CHANGE THIS (30, 60, or 90 recommended)

# Optional: Add description for your records
POLICY_NAME = "New Aadhaar Policy 2025"
POLICY_DESCRIPTION = """
Describe your policy here:
- What is the policy about?
- Who does it affect?
- What actions are required?
"""

# ============================================================================
# STEP 2: RUN THE PREDICTION (No changes needed below)
# ============================================================================

print("=" * 80)
print("AADHAAR POLICY IMPACT PREDICTION")
print("=" * 80)
print(f"\nPolicy: {POLICY_NAME}")
print(f"Implementation Date: {MY_POLICY_DATE}")
print(f"Forecast Period: {FORECAST_DAYS} days")
print(f"\nDescription: {POLICY_DESCRIPTION}")
print("\n" + "=" * 80)

# Initialize predictor
print("\n[1/5] Initializing predictor...")
predictor = PolicyImpactPredictor()

# Load data
print("[2/5] Loading and preparing data...")
predictor.load_and_prepare_data(use_cached=True)

# Train baseline models
print("[3/5] Training baseline models...")
try:
    predictor.baseline_model.load_models()
    print("      ✓ Loaded existing baseline models")
except:
    print("      Training new baseline models...")
    predictor.train_baseline()

# Train policy impact model
print(f"[4/5] Training policy impact model for {MY_POLICY_DATE}...")
try:
    predictor.policy_model.load_models()
    print("      ✓ Loaded existing policy models")
except:
    print("      Training new policy models...")
    predictor.train_policy_model(MY_POLICY_DATE)

# Generate predictions
print("[5/5] Generating predictions...")
results = predictor.predict_policy_impact(
    policy_date=MY_POLICY_DATE,
    forecast_days=FORECAST_DAYS
)

# ============================================================================
# STEP 3: VIEW YOUR RESULTS
# ============================================================================

summary = results['summary']

print("\n" + "=" * 80)
print("PREDICTION RESULTS")
print("=" * 80)

print(f"\nPolicy Implementation Date: {summary['policy_date']}")
print(f"Forecast Period: {summary['forecast_days']} days")

print("\n" + "-" * 80)
print("OVERALL IMPACT")
print("-" * 80)
print(f"Total People Affected: {summary['total_people_affected']:,}")
print(f"  - Additional Enrolments: {summary['total_enrolment_increase']:,}")
print(f"  - Additional Updates: {summary['total_update_increase']:,}")

print("\n" + "-" * 80)
print("PEAK IMPACT")
print("-" * 80)
print(f"Peak Impact Date: {summary['peak_impact_date']}")
print(f"Peak Daily Volume: {summary['peak_impact_volume']:,} people")
print(f"Duration of Significant Impact: {summary['significant_impact_duration_days']} days")

print("\n" + "-" * 80)
print("TOP 10 MOST AFFECTED STATES")
print("-" * 80)

regional = results['regional_impact']
top_states = sorted(regional['total_impact'].items(), 
                   key=lambda x: x[1], reverse=True)[:10]

for i, (state, impact) in enumerate(top_states, 1):
    enrol = regional['enrolment_impact'][state]
    update = regional['update_impact'][state]
    print(f"{i:2d}. {state:25s}: {int(impact):10,} people")
    print(f"    Enrolments: {int(enrol):8,} | Updates: {int(update):8,}")

# ============================================================================
# STEP 4: GENERATE REPORT AND VISUALIZATIONS
# ============================================================================

print("\n" + "=" * 80)
print("GENERATING OUTPUTS")
print("=" * 80)

# Generate text report
report_filename = f"policy_report_{MY_POLICY_DATE}.txt"
print(f"\nGenerating report: {report_filename}")
predictor.generate_report(results, output_file=report_filename)

# Generate visualizations
print("Generating visualizations...")
viz = PolicyImpactVisualizer()
viz.generate_all_visualizations(results)

# Save results for later use
import pickle
results_filename = f"results_{MY_POLICY_DATE}.pkl"
with open(results_filename, 'wb') as f:
    pickle.dump(results, f)
print(f"Results saved: {results_filename}")

print("\n" + "=" * 80)
print("ANALYSIS COMPLETE!")
print("=" * 80)

print("\nGenerated Files:")
print(f"  1. {report_filename} - Detailed text report")
print("  2. summary_dashboard.png - Comprehensive dashboard")
print("  3. time_series_impact.png - Daily impact over time")
print("  4. regional_impact.png - State-wise breakdown")
print("  5. cumulative_impact.png - Cumulative trends")
print("  6. impact_heatmap.png - State vs time heatmap")
print(f"  7. {results_filename} - Results for later analysis")

print("\nNext Steps:")
print("  - Review the generated visualizations")
print(f"  - Read {report_filename} for detailed findings")
print("  - Modify MY_POLICY_DATE and FORECAST_DAYS to test other scenarios")
print("  - Compare multiple policy dates to find optimal timing")

print("\n" + "=" * 80)

# ============================================================================
# OPTIONAL: EXPORT RESULTS TO CSV
# ============================================================================

# Uncomment these lines if you want CSV exports:

# # Export daily impact
# results['daily_impact'].to_csv(f'daily_impact_{MY_POLICY_DATE}.csv', index=False)
# print(f"Daily impact exported to: daily_impact_{MY_POLICY_DATE}.csv")

# # Export regional impact
# import pandas as pd
# regional_df = pd.DataFrame(results['regional_impact'])
# regional_df.to_csv(f'regional_impact_{MY_POLICY_DATE}.csv')
# print(f"Regional impact exported to: regional_impact_{MY_POLICY_DATE}.csv")

# ============================================================================
# OPTIONAL: QUICK ANALYSIS FUNCTIONS
# ============================================================================

def analyze_state(state_name):
    """Get detailed analysis for a specific state"""
    regional = results['regional_impact']
    if state_name in regional['total_impact']:
        print(f"\nAnalysis for {state_name}:")
        print(f"  Total Impact: {regional['total_impact'][state_name]:,.0f} people")
        print(f"  Enrolments: {regional['enrolment_impact'][state_name]:,.0f}")
        print(f"  Updates: {regional['update_impact'][state_name]:,.0f}")
    else:
        print(f"State '{state_name}' not found in results")

def get_impact_on_date(date_str):
    """Get impact for a specific date"""
    daily = results['daily_impact']
    daily['date'] = pd.to_datetime(daily['date'])
    target_date = pd.to_datetime(date_str)
    
    row = daily[daily['date'] == target_date]
    if len(row) > 0:
        print(f"\nImpact on {date_str}:")
        print(f"  Total: {row['total_impact'].values[0]:,.0f} people")
        print(f"  Enrolments: {row['enrolment_impact'].values[0]:,.0f}")
        print(f"  Updates: {row['update_impact'].values[0]:,.0f}")
    else:
        print(f"Date '{date_str}' not in forecast period")

# Example usage (uncomment to use):
# analyze_state("Uttar Pradesh")
# get_impact_on_date("2025-04-15")
