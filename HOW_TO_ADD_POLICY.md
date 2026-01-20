# How to Add Your Policy Details and Get Results

## 🎯 Quick Guide: 3 Ways to Add Policy Details

---

## Method 1: Edit the Script (Easiest) ⭐

### Step 1: Open `quick_start.py`

Find these lines (around line 40):

```python
# Example policy date
POLICY_DATE = "2025-04-01"
```

### Step 2: Change the Policy Date

Replace with your policy date:

```python
# YOUR POLICY DATE HERE
POLICY_DATE = "2025-05-15"  # Change this to your date
```

### Step 3: Run the Script

```bash
python quick_start.py
```

**That's it!** You'll get predictions for your policy date.

---

## Method 2: Use Python API (Most Flexible) ⭐⭐

Create a new file called `my_policy_prediction.py`:

```python
from prediction_system import PolicyImpactPredictor

# Initialize predictor
predictor = PolicyImpactPredictor()

# Load data
print("Loading data...")
predictor.load_and_prepare_data()

# ============================================
# ADD YOUR POLICY DETAILS HERE
# ============================================

# Policy date (when policy will be implemented)
MY_POLICY_DATE = "2025-06-01"  # ← Change this

# Forecast period (how many days to predict)
FORECAST_DAYS = 60  # ← Change this (30, 60, or 90 days)

# Optional: Add policy description for your records
POLICY_DESCRIPTION = "Mandatory biometric update for all citizens above 18"

# ============================================
# GET PREDICTIONS
# ============================================

print(f"\nPredicting impact for: {POLICY_DESCRIPTION}")
print(f"Policy Date: {MY_POLICY_DATE}")
print(f"Forecast Period: {FORECAST_DAYS} days\n")

# Train models and generate predictions
predictor.train_baseline()
predictor.train_policy_model(MY_POLICY_DATE)

results = predictor.predict_policy_impact(
    policy_date=MY_POLICY_DATE,
    forecast_days=FORECAST_DAYS
)

# ============================================
# VIEW RESULTS
# ============================================

summary = results['summary']

print("=" * 80)
print("POLICY IMPACT PREDICTION RESULTS")
print("=" * 80)
print(f"\nPolicy: {POLICY_DESCRIPTION}")
print(f"Implementation Date: {MY_POLICY_DATE}")
print(f"\nTOTAL PEOPLE AFFECTED: {summary['total_people_affected']:,}")
print(f"  - Additional Enrolments: {summary['total_enrolment_increase']:,}")
print(f"  - Additional Updates: {summary['total_update_increase']:,}")
print(f"\nPeak Impact Date: {summary['peak_impact_date']}")
print(f"Peak Daily Volume: {summary['peak_impact_volume']:,} people")
print(f"Impact Duration: {summary['significant_impact_duration_days']} days")

# Show top 5 affected states
print("\nTop 5 Most Affected States:")
regional = results['regional_impact']
top_states = sorted(regional['total_impact'].items(), 
                   key=lambda x: x[1], reverse=True)[:5]
for i, (state, impact) in enumerate(top_states, 1):
    print(f"  {i}. {state}: {int(impact):,} people")

# Generate report and visualizations
predictor.generate_report(results, output_file=f"policy_report_{MY_POLICY_DATE}.txt")

from visualization import PolicyImpactVisualizer
viz = PolicyImpactVisualizer()
viz.generate_all_visualizations(results)

print("\n✓ Report and visualizations generated!")
```

Then run:
```bash
python my_policy_prediction.py
```

---

## Method 3: Interactive Notebook (Best for Exploration) ⭐⭐⭐

### Step 1: Open the Notebook

```bash
jupyter notebook policy_impact_analysis.ipynb
```

### Step 2: Find the Policy Configuration Cell

Look for this cell (around cell 10):

```python
# Define policy scenario
POLICY_DATE = "2025-04-01"
FORECAST_DAYS = 60
```

### Step 3: Change the Values

```python
# ============================================
# YOUR POLICY DETAILS HERE
# ============================================

POLICY_DATE = "2025-07-01"      # Your policy date
FORECAST_DAYS = 90               # How many days to forecast

# Optional: Add notes
POLICY_NAME = "New Aadhaar Mandate 2025"
POLICY_DESCRIPTION = """
This policy requires all citizens to update their 
biometric information by July 2025.
"""

print(f"Policy: {POLICY_NAME}")
print(f"Date: {POLICY_DATE}")
print(f"Forecast: {FORECAST_DAYS} days")
```

### Step 4: Run All Cells

Click "Cell" → "Run All" or press Shift+Enter on each cell.

---

## 📋 Policy Details You Can Specify

### Required Parameters

| Parameter | Description | Example |
|-----------|-------------|---------|
| `policy_date` | When policy will be implemented | `"2025-04-01"` |
| `forecast_days` | How many days to predict | `60` (30, 60, or 90) |

### Optional Information (for your records)

You can add these as comments or variables:

```python
# Policy metadata (optional, for documentation)
POLICY_INFO = {
    'name': 'Mandatory Biometric Update 2025',
    'description': 'All citizens must update biometric data',
    'target_group': 'Citizens above 18 years',
    'expected_compliance': '80%',
    'implementation_date': '2025-04-01',
    'deadline': '2025-06-30',
    'affected_states': ['All states'],
    'priority_states': ['Uttar Pradesh', 'Maharashtra', 'Bihar']
}
```

---

## 🎯 Complete Example: Multiple Policy Scenarios

Create `compare_policies.py`:

```python
from prediction_system import PolicyImpactPredictor

# Initialize
predictor = PolicyImpactPredictor()
predictor.load_and_prepare_data()

# ============================================
# DEFINE MULTIPLE POLICY SCENARIOS
# ============================================

policies = [
    {
        'name': 'Early Implementation',
        'date': '2025-04-01',
        'days': 60,
        'description': 'Implement in April'
    },
    {
        'name': 'Mid-Year Implementation',
        'date': '2025-06-01',
        'days': 60,
        'description': 'Implement in June'
    },
    {
        'name': 'Late Implementation',
        'date': '2025-08-01',
        'days': 60,
        'description': 'Implement in August'
    }
]

# ============================================
# COMPARE SCENARIOS
# ============================================

print("=" * 80)
print("POLICY SCENARIO COMPARISON")
print("=" * 80)

comparison_results = []

for policy in policies:
    print(f"\nAnalyzing: {policy['name']} ({policy['date']})...")
    
    # Train and predict
    predictor.train_policy_model(policy['date'])
    results = predictor.predict_policy_impact(
        policy_date=policy['date'],
        forecast_days=policy['days']
    )
    
    # Store results
    comparison_results.append({
        'Policy': policy['name'],
        'Date': policy['date'],
        'Total Affected': results['summary']['total_people_affected'],
        'Peak Date': results['summary']['peak_impact_date'],
        'Peak Volume': results['summary']['peak_impact_volume'],
        'Duration (days)': results['summary']['significant_impact_duration_days']
    })

# ============================================
# DISPLAY COMPARISON
# ============================================

import pandas as pd
df = pd.DataFrame(comparison_results)

print("\n" + "=" * 80)
print("COMPARISON RESULTS")
print("=" * 80)
print(df.to_string(index=False))

# Find best option
best_idx = df['Total Affected'].idxmin()
print(f"\n✓ Recommended: {df.loc[best_idx, 'Policy']} - Lowest impact")
```

Run:
```bash
python compare_policies.py
```

---

## 📊 What Results You'll Get

After specifying your policy details, you'll receive:

### 1. Console Output
```
POLICY IMPACT PREDICTION RESULTS
================================================================================
Policy Date: 2025-04-01
Total People Affected: 1,234,567
  - Additional Enrolments: 789,012
  - Additional Updates: 445,555

Peak Impact Date: 2025-04-15
Peak Daily Volume: 45,678 people
Impact Duration: 42 days

Top 5 Most Affected States:
  1. Uttar Pradesh: 234,567 people
  2. Maharashtra: 198,765 people
  ...
```

### 2. Text Report
- `policy_impact_report.txt` - Detailed formatted report

### 3. Visualizations (5 PNG files)
- `summary_dashboard.png` - Overview dashboard
- `time_series_impact.png` - Daily impact chart
- `regional_impact.png` - State-wise breakdown
- `cumulative_impact.png` - Cumulative trends
- `impact_heatmap.png` - State vs time heatmap

### 4. Data Files
- `master_aadhaar_data.csv` - Cleaned data
- `featured_aadhaar_data.csv` - Data with features

### 5. Python Dictionary
```python
results = {
    'summary': {
        'policy_date': '2025-04-01',
        'total_people_affected': 1234567,
        'peak_impact_date': '2025-04-15',
        ...
    },
    'regional_impact': {...},
    'daily_impact': DataFrame,
    'full_predictions': DataFrame
}
```

---

## 🔧 Advanced: Custom Policy Features

If you want to add more policy-specific features, edit `feature_engineering.py`:

```python
def add_policy_features(self, policy_date: str) -> pd.DataFrame:
    """Add policy-related features"""
    df = self.df.copy()
    policy_dt = pd.to_datetime(policy_date)
    
    # Existing features
    df['policy_active'] = (df['date'] >= policy_dt).astype(int)
    df['days_from_policy'] = (df['date'] - policy_dt).dt.days
    
    # ============================================
    # ADD YOUR CUSTOM POLICY FEATURES HERE
    # ============================================
    
    # Example: Policy intensity (how strict)
    POLICY_INTENSITY = 0.8  # 0.0 to 1.0 (0.8 = strict)
    df['policy_intensity'] = df['policy_active'] * POLICY_INTENSITY
    
    # Example: Grace period
    GRACE_PERIOD_DAYS = 30
    df['in_grace_period'] = (
        (df['days_from_policy'] >= 0) & 
        (df['days_from_policy'] <= GRACE_PERIOD_DAYS)
    ).astype(int)
    
    # Example: Penalty phase
    PENALTY_START_DAY = 60
    df['penalty_phase'] = (
        df['days_from_policy'] > PENALTY_START_DAY
    ).astype(int)
    
    return df
```

---

## 💡 Quick Tips

### Tip 1: Date Format
Always use `"YYYY-MM-DD"` format:
- ✅ Correct: `"2025-04-01"`
- ❌ Wrong: `"01-04-2025"` or `"April 1, 2025"`

### Tip 2: Forecast Period
- **30 days**: High confidence, immediate planning
- **60 days**: Medium confidence, resource allocation
- **90 days**: Lower confidence, strategic planning

### Tip 3: Multiple Scenarios
Always compare 2-3 different dates to find the optimal implementation time.

### Tip 4: Save Results
```python
# Save for later analysis
import pickle
with open(f'results_{POLICY_DATE}.pkl', 'wb') as f:
    pickle.dump(results, f)

# Load later
with open(f'results_{POLICY_DATE}.pkl', 'rb') as f:
    loaded_results = pickle.load(f)
```

---

## 🚀 Recommended Workflow

1. **Start Simple**: Use `quick_start.py` with one policy date
2. **Explore**: Use the Jupyter notebook to understand results
3. **Compare**: Create `compare_policies.py` to test multiple dates
4. **Customize**: Create your own script with specific policy details
5. **Automate**: Set up regular predictions with different scenarios

---

## ❓ Common Questions

### Q: Can I predict for past dates?
**A:** Yes, for validation. The system will use historical data to check accuracy.

### Q: How far in the future can I predict?
**A:** Up to 90 days with reasonable confidence. Beyond that, accuracy decreases.

### Q: Can I add policy type (e.g., mandatory vs voluntary)?
**A:** Yes! Add it as a custom feature in `feature_engineering.py` (see Advanced section above).

### Q: Can I specify which states will be affected?
**A:** The model predicts all states automatically. You can filter results afterward:
```python
# Filter specific states
states_of_interest = ['Uttar Pradesh', 'Maharashtra', 'Karnataka']
filtered = results['full_predictions'][
    results['full_predictions']['state'].isin(states_of_interest)
]
```

---

## 📞 Need Help?

- **Basic usage**: See `USER_GUIDE.md`
- **Examples**: See `example_usage.py`
- **Troubleshooting**: See `USER_GUIDE.md` → Troubleshooting
- **API details**: See `prediction_system.py` docstrings

---

**Ready to predict?** Start with Method 1 (edit `quick_start.py`) - it's the easiest! 🚀
