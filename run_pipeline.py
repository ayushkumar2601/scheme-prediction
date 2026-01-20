"""
Complete Pipeline Runner
Executes the entire workflow from data loading to prediction
"""

import sys
import warnings
warnings.filterwarnings('ignore')

def run_pipeline():
    """Run the complete prediction pipeline"""
    
    print("=" * 80)
    print("AADHAAR POLICY IMPACT PREDICTION PIPELINE")
    print("=" * 80)
    print()
    
    # Step 1: Load Data
    print("STEP 1: Loading and Preparing Data")
    print("-" * 80)
    try:
        from data_loader import AadhaarDataLoader
        loader = AadhaarDataLoader()
        master_data = loader.create_master_dataset()
        master_data.to_csv("master_aadhaar_data.csv", index=False)
        print("✓ Data loaded and saved to master_aadhaar_data.csv")
    except Exception as e:
        print(f"✗ Error loading data: {e}")
        return False
    
    # Step 2: Feature Engineering
    print("\nSTEP 2: Feature Engineering")
    print("-" * 80)
    try:
        from feature_engineering import FeatureEngineer
        fe = FeatureEngineer(master_data)
        featured_data = fe.create_all_features()
        featured_data.to_csv("featured_aadhaar_data.csv", index=False)
        print("✓ Features created and saved to featured_aadhaar_data.csv")
    except Exception as e:
        print(f"✗ Error in feature engineering: {e}")
        return False
    
    # Step 3: Train Baseline Models
    print("\nSTEP 3: Training Baseline Models")
    print("-" * 80)
    try:
        from baseline_model import BaselineModel
        baseline = BaselineModel()
        baseline.train_enrolment_model(featured_data)
        baseline.train_update_model(featured_data)
        baseline.save_models()
        print("✓ Baseline models trained and saved")
    except Exception as e:
        print(f"✗ Error training baseline models: {e}")
        return False
    
    # Step 4: Train Policy Impact Models
    print("\nSTEP 4: Training Policy Impact Models")
    print("-" * 80)
    try:
        from policy_impact_model import PolicyImpactModel
        
        # Use a sample policy date for training
        TRAINING_POLICY_DATE = "2025-03-15"
        
        # Add policy features
        fe_policy = FeatureEngineer(master_data)
        featured_policy = fe_policy.create_all_features(policy_date=TRAINING_POLICY_DATE)
        
        policy_model = PolicyImpactModel()
        policy_model.train_impact_models(featured_policy, TRAINING_POLICY_DATE)
        policy_model.save_models()
        print("✓ Policy impact models trained and saved")
    except Exception as e:
        print(f"✗ Error training policy models: {e}")
        return False
    
    # Step 5: Generate Predictions
    print("\nSTEP 5: Generating Predictions")
    print("-" * 80)
    try:
        from prediction_system import PolicyImpactPredictor
        
        predictor = PolicyImpactPredictor()
        predictor.master_data = master_data
        
        # Predict for a future policy
        POLICY_DATE = "2025-04-01"
        FORECAST_DAYS = 60
        
        results = predictor.predict_policy_impact(
            policy_date=POLICY_DATE,
            forecast_days=FORECAST_DAYS
        )
        
        print(f"✓ Predictions generated for policy on {POLICY_DATE}")
        print(f"  Total people affected: {results['summary']['total_people_affected']:,}")
        
    except Exception as e:
        print(f"✗ Error generating predictions: {e}")
        return False
    
    # Step 6: Generate Report
    print("\nSTEP 6: Generating Report")
    print("-" * 80)
    try:
        predictor.generate_report(results, output_file="policy_impact_report.txt")
        print("✓ Report saved to policy_impact_report.txt")
    except Exception as e:
        print(f"✗ Error generating report: {e}")
        return False
    
    # Step 7: Create Visualizations
    print("\nSTEP 7: Creating Visualizations")
    print("-" * 80)
    try:
        from visualization import PolicyImpactVisualizer
        viz = PolicyImpactVisualizer()
        viz.generate_all_visualizations(results)
        print("✓ All visualizations created")
    except Exception as e:
        print(f"✗ Error creating visualizations: {e}")
        return False
    
    # Summary
    print("\n" + "=" * 80)
    print("PIPELINE COMPLETED SUCCESSFULLY!")
    print("=" * 80)
    print("\nGenerated Files:")
    print("  Data:")
    print("    - master_aadhaar_data.csv")
    print("    - featured_aadhaar_data.csv")
    print("  Models:")
    print("    - enrolment_baseline_model.pkl")
    print("    - update_baseline_model.pkl")
    print("    - enrolment_impact_model.pkl")
    print("    - update_impact_model.pkl")
    print("  Reports:")
    print("    - policy_impact_report.txt")
    print("  Visualizations:")
    print("    - summary_dashboard.png")
    print("    - time_series_impact.png")
    print("    - regional_impact.png")
    print("    - cumulative_impact.png")
    print("    - impact_heatmap.png")
    
    print("\nNext Steps:")
    print("  1. Review policy_impact_report.txt for detailed findings")
    print("  2. Open summary_dashboard.png for visual overview")
    print("  3. Run example_usage.py for different scenarios")
    print("  4. Use policy_impact_analysis.ipynb for interactive analysis")
    
    return True

if __name__ == "__main__":
    success = run_pipeline()
    sys.exit(0 if success else 1)
