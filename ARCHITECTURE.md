# System Architecture

## Overview

```
┌─────────────────────────────────────────────────────────────────┐
│                  AADHAAR POLICY IMPACT PREDICTION SYSTEM         │
└─────────────────────────────────────────────────────────────────┘

INPUT: Policy Date + Forecast Horizon
OUTPUT: Total Impact + Regional Distribution + Time Series
```

## Data Flow

```
┌──────────────────┐
│   Raw CSV Data   │
│  - Enrolment     │
│  - Biometric     │
│  - Demographic   │
└────────┬─────────┘
         │
         ▼
┌──────────────────┐
│  Data Loader     │
│  - Load files    │
│  - Clean data    │
│  - Aggregate     │
└────────┬─────────┘
         │
         ▼
┌──────────────────┐
│  Master Dataset  │
│  (State/Date)    │
└────────┬─────────┘
         │
         ▼
┌──────────────────┐
│ Feature Engineer │
│  - Temporal      │
│  - Lag           │
│  - Rolling       │
│  - Growth        │
│  - Policy        │
└────────┬─────────┘
         │
         ▼
┌──────────────────┐
│ Featured Dataset │
│  (40+ features)  │
└────────┬─────────┘
         │
         ├─────────────────────┬─────────────────────┐
         ▼                     ▼                     ▼
┌──────────────────┐  ┌──────────────────┐  ┌──────────────────┐
│ Baseline Model   │  │ Policy Model     │  │ Prediction       │
│ (No Policy)      │  │ (With Policy)    │  │ System           │
│                  │  │                  │  │                  │
│ - Enrolment      │  │ - Enrolment      │  │ - Orchestrate    │
│ - Update         │  │ - Update         │  │ - Calculate      │
│                  │  │                  │  │ - Aggregate      │
└────────┬─────────┘  └────────┬─────────┘  └────────┬─────────┘
         │                     │                     │
         └──────────┬──────────┘                     │
                    ▼                                │
         ┌──────────────────┐                        │
         │  Impact = Policy │                        │
         │  - Baseline      │                        │
         └────────┬─────────┘                        │
                  │                                  │
                  └──────────────┬───────────────────┘
                                 ▼
                  ┌──────────────────────┐
                  │   Results            │
                  │  - Summary stats     │
                  │  - Regional impact   │
                  │  - Daily time series │
                  └────────┬─────────────┘
                           │
                           ├─────────────┬─────────────┐
                           ▼             ▼             ▼
                  ┌──────────────┐ ┌──────────┐ ┌──────────┐
                  │ Visualizer   │ │ Report   │ │ Export   │
                  │ - Charts     │ │ - Text   │ │ - CSV    │
                  │ - Dashboard  │ │ - Tables │ │ - Pickle │
                  └──────────────┘ └──────────┘ └──────────┘
```

## Module Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                         USER INTERFACE                           │
├─────────────────┬─────────────────┬─────────────────────────────┤
│ quick_start.py  │ example_usage.py│ policy_impact_analysis.ipynb│
│ (5 min)         │ (10 min)        │ (Interactive)               │
└────────┬────────┴────────┬────────┴────────┬────────────────────┘
         │                 │                 │
         └─────────────────┼─────────────────┘
                           ▼
         ┌─────────────────────────────────────┐
         │     prediction_system.py            │
         │     (Main Orchestrator)             │
         └─────────────────┬───────────────────┘
                           │
         ┌─────────────────┼─────────────────┐
         │                 │                 │
         ▼                 ▼                 ▼
┌──────────────┐  ┌──────────────┐  ┌──────────────┐
│data_loader.py│  │baseline_     │  │policy_impact_│
│              │  │model.py      │  │model.py      │
└──────┬───────┘  └──────┬───────┘  └──────┬───────┘
       │                 │                 │
       ▼                 ▼                 ▼
┌──────────────┐  ┌──────────────┐  ┌──────────────┐
│feature_      │  │sklearn       │  │sklearn       │
│engineering.py│  │GradientBoost │  │GradientBoost │
└──────────────┘  └──────────────┘  └──────────────┘
       │
       ▼
┌──────────────┐
│visualization │
│.py           │
└──────────────┘
```

## Component Responsibilities

### 1. Data Layer
```
data_loader.py
├── AadhaarDataLoader
│   ├── load_enrolment_data()
│   ├── load_biometric_data()
│   ├── load_demographic_data()
│   ├── clean_and_aggregate_enrolment()
│   ├── clean_and_aggregate_updates()
│   └── create_master_dataset()
```

### 2. Feature Layer
```
feature_engineering.py
├── FeatureEngineer
│   ├── add_temporal_features()
│   ├── add_lag_features()
│   ├── add_rolling_features()
│   ├── add_growth_features()
│   ├── add_policy_features()
│   ├── add_state_features()
│   └── create_all_features()
```

### 3. Model Layer
```
baseline_model.py
├── BaselineModel
│   ├── prepare_features()
│   ├── train_enrolment_model()
│   ├── train_update_model()
│   ├── predict_baseline()
│   ├── save_models()
│   └── load_models()

policy_impact_model.py
├── PolicyImpactModel
│   ├── prepare_policy_features()
│   ├── train_impact_models()
│   ├── predict_with_policy()
│   ├── calculate_policy_impact()
│   ├── save_models()
│   └── load_models()
```

### 4. Prediction Layer
```
prediction_system.py
├── PolicyImpactPredictor
│   ├── load_and_prepare_data()
│   ├── train_baseline()
│   ├── train_policy_model()
│   ├── predict_policy_impact()
│   ├── _analyze_predictions()
│   └── generate_report()
```

### 5. Visualization Layer
```
visualization.py
├── PolicyImpactVisualizer
│   ├── plot_time_series_impact()
│   ├── plot_regional_impact()
│   ├── plot_impact_heatmap()
│   ├── plot_cumulative_impact()
│   ├── create_summary_dashboard()
│   └── generate_all_visualizations()
```

## Execution Flow

### Scenario: Predict Policy Impact

```
1. User Input
   ├── policy_date = "2025-04-01"
   └── forecast_days = 60

2. Data Loading
   ├── Load enrolment CSVs (4 files)
   ├── Load biometric CSVs (4 files)
   ├── Load demographic CSVs (5 files)
   └── Aggregate to state/date level

3. Feature Engineering
   ├── Create temporal features (7)
   ├── Create lag features (8)
   ├── Create rolling features (12)
   ├── Create growth features (4)
   ├── Create policy features (5)
   └── Create state features (4)
   Total: 40+ features

4. Baseline Training
   ├── Train enrolment model (GBR)
   └── Train update model (GBR)

5. Policy Training
   ├── Add policy features
   ├── Train enrolment impact model (GBR)
   └── Train update impact model (GBR)

6. Prediction
   ├── Create forecast dataset (60 days × 36 states)
   ├── Add features
   ├── Predict baseline (no policy)
   ├── Predict with policy
   └── Calculate impact = policy - baseline

7. Analysis
   ├── Aggregate by date (daily impact)
   ├── Aggregate by state (regional impact)
   ├── Calculate cumulative impact
   ├── Identify peak date
   └── Calculate duration

8. Output
   ├── Generate text report
   ├── Create 5 visualizations
   ├── Export CSV results
   └── Save pickle for later use
```

## Data Structures

### Master Dataset
```python
{
    'date': datetime,
    'state': str,
    'total_enrolments': int,
    'total_updates': int,
    'age_0_5': int,
    'age_5_17': int,
    'age_18_greater': int,
    'num_districts': int
}
```

### Featured Dataset
```python
{
    # Original columns
    'date', 'state', 'total_enrolments', 'total_updates', ...
    
    # Temporal features
    'year', 'month', 'day', 'day_of_week', 'week_of_year', 'is_weekend',
    
    # Lag features
    'total_enrolments_lag_1', 'total_enrolments_lag_7', ...
    
    # Rolling features
    'total_enrolments_rolling_mean_7', 'total_enrolments_rolling_std_7', ...
    
    # Growth features
    'total_enrolments_growth', 'total_enrolments_growth_7d', ...
    
    # Policy features
    'policy_active', 'days_from_policy', 'pre_policy_30d', ...
    
    # State features
    'state_avg_enrolments', 'enrolment_deviation', ...
}
```

### Results Structure
```python
{
    'summary': {
        'policy_date': str,
        'forecast_days': int,
        'total_people_affected': int,
        'total_enrolment_increase': int,
        'total_update_increase': int,
        'peak_impact_date': str,
        'peak_impact_volume': int,
        'significant_impact_duration_days': int
    },
    'regional_impact': {
        'enrolment_impact': {state: value, ...},
        'update_impact': {state: value, ...},
        'total_impact': {state: value, ...}
    },
    'daily_impact': DataFrame[date, enrolment_impact, update_impact, total_impact],
    'full_predictions': DataFrame[all predictions with features]
}
```

## Technology Stack

```
┌─────────────────────────────────────────┐
│           Application Layer              │
│  Python 3.8+, Jupyter Notebook          │
└─────────────────────────────────────────┘
┌─────────────────────────────────────────┐
│         Data Processing Layer            │
│  pandas, numpy                          │
└─────────────────────────────────────────┘
┌─────────────────────────────────────────┐
│        Machine Learning Layer            │
│  scikit-learn (GradientBoostingRegressor)│
└─────────────────────────────────────────┘
┌─────────────────────────────────────────┐
│         Visualization Layer              │
│  matplotlib, seaborn, plotly            │
└─────────────────────────────────────────┘
┌─────────────────────────────────────────┐
│          Persistence Layer               │
│  CSV, pickle (joblib)                   │
└─────────────────────────────────────────┘
```

## Scalability Considerations

### Current Scale
- States: ~36
- Days: ~30-90
- Records per prediction: ~2,000-3,000
- Features: 40+
- Processing time: 5-15 minutes

### Scaling Options
1. **More states**: Linear scaling, no code changes needed
2. **Longer forecasts**: Linear scaling, may need more memory
3. **More features**: May need feature selection
4. **Real-time**: Add caching, incremental updates
5. **Distributed**: Use Dask for parallel processing

## Error Handling

```
Try-Except Blocks at:
├── Data loading (file not found)
├── Model training (insufficient data)
├── Prediction (missing features)
├── Visualization (empty results)
└── Report generation (I/O errors)

Validation Checks:
├── Date format validation
├── Feature completeness
├── Model existence
├── Result sanity checks
└── Output file permissions
```

## Testing Strategy

```
Unit Tests (Recommended):
├── test_data_loader.py
├── test_feature_engineering.py
├── test_baseline_model.py
├── test_policy_impact_model.py
└── test_prediction_system.py

Integration Tests:
├── test_end_to_end_pipeline.py
└── test_scenario_simulations.py

Validation Tests:
├── test_historical_backtest.py
└── test_prediction_accuracy.py
```

## Deployment Options

### Option 1: Standalone Scripts
```bash
python quick_start.py
```

### Option 2: Jupyter Notebook
```bash
jupyter notebook policy_impact_analysis.ipynb
```

### Option 3: Python Package
```python
from aadhaar_prediction import PolicyImpactPredictor
predictor = PolicyImpactPredictor()
```

### Option 4: REST API (Future)
```python
@app.route('/predict', methods=['POST'])
def predict():
    policy_date = request.json['policy_date']
    results = predictor.predict_policy_impact(policy_date)
    return jsonify(results)
```

### Option 5: Scheduled Batch (Future)
```bash
cron: 0 0 * * * python run_pipeline.py
```

## Conclusion

This architecture provides:
- **Modularity**: Each component has clear responsibilities
- **Extensibility**: Easy to add new features or models
- **Maintainability**: Well-organized, documented code
- **Scalability**: Can handle larger datasets
- **Usability**: Multiple entry points for different users
