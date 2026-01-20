"""
Example Usage of Aadhaar Policy Impact Prediction System

This script demonstrates how to use the system to predict policy impacts.
"""

import warnings
warnings.filterwarnings('ignore')

from prediction_system import PolicyImpactPredictor
from visualization import PolicyImpactVisualizer
import pickle

def main():
    print("=" * 80)
    print("AADHAAR POLICY IMPACT PREDICTION SYSTEM")
    print("=" * 80)
    print()
    
    # Initialize predictor
    print("Step 1: Initializing predictor...")
    predictor = PolicyImpactPredictor()
    
    # Load and prepare data
    print("\nStep 2: Loading and preparing data...")
    predictor.load_and_prepare_data(use_cached=True)
    
    # Train baseline models (learns normal behavior)
    print("\nStep 3: Training baseline models...")
    try:
        predictor.baseline_model.load_models()
        print("Loaded existing baseline models")
    except:
        print("Training new baseline models...")
        predictor.train_baseline()
    
    # Define policy scenario
    POLICY_DATE = "2025-04-01"
    FORECAST_DAYS = 60
    
    print(f"\nStep 4: Predicting impact for policy on {POLICY_DATE}")
    print(f"Forecast period: {FORECAST_DAYS} days")
    
    # Train policy impact model
    try:
        predictor.policy_model.load_models()
        print("Loaded existing policy models")
    except:
        print("Training policy impact model...")
        predictor.train_policy_model(POLICY_DATE)
    
    # Generate predictions
    print("\nStep 5: Generating predictions...")
    results = predictor.predict_policy_impact(
        policy_date=POLICY_DATE,
        forecast_days=FORECAST_DAYS
    )
    
    # Display results
    print("\n" + "=" * 80)
    print("PREDICTION RESULTS")
    print("=" * 80)
    
    summary = results['summary']
    
    print(f"\nPolicy Date: {summary['policy_date']}")
    print(f"Forecast Period: {summary['forecast_days']} days")
    print()
    print(f"Total People Affected: {summary['total_people_affected']:,}")
    print(f"  - Additional Enrolments: {summary['total_enrolment_increase']:,}")
    print(f"  - Additional Updates: {summary['total_update_increase']:,}")
    print()
    print(f"Peak Impact Date: {summary['peak_impact_date']}")
    print(f"Peak Daily Volume: {summary['peak_impact_volume']:,} people")
    print()
    print(f"Duration of Significant Impact: {summary['significant_impact_duration_days']} days")
    
    # Show top affected states
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
    
    # Generate report
    print("\nStep 6: Generating detailed report...")
    predictor.generate_report(results, output_file="policy_impact_report.txt")
    
    # Generate visualizations
    print("\nStep 7: Creating visualizations...")
    viz = PolicyImpactVisualizer()
    viz.generate_all_visualizations(results)
    
    # Save results for later use
    with open('prediction_results.pkl', 'wb') as f:
        pickle.dump(results, f)
    print("\nResults saved to prediction_results.pkl")
    
    print("\n" + "=" * 80)
    print("ANALYSIS COMPLETE!")
    print("=" * 80)
    print("\nGenerated files:")
    print("  - policy_impact_report.txt (detailed text report)")
    print("  - summary_dashboard.png (comprehensive dashboard)")
    print("  - time_series_impact.png (daily impact chart)")
    print("  - regional_impact.png (state-wise impact)")
    print("  - cumulative_impact.png (cumulative trends)")
    print("  - impact_heatmap.png (state vs time heatmap)")
    print("\nYou can now:")
    print("  1. Review the generated visualizations")
    print("  2. Read the detailed report")
    print("  3. Run scenario simulations with different policy dates")
    print("  4. Use the Jupyter notebook for interactive analysis")
    
    return results

if __name__ == "__main__":
    results = main()
