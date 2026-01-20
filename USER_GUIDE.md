# User Guide: Aadhaar Policy Impact Prediction System

## Table of Contents
1. [Getting Started](#getting-started)
2. [Basic Usage](#basic-usage)
3. [Advanced Usage](#advanced-usage)
4. [Understanding Results](#understanding-results)
5. [Customization](#customization)
6. [Troubleshooting](#troubleshooting)
7. [FAQ](#faq)

---

## Getting Started

### Prerequisites
- Python 3.8 or higher
- 2GB RAM minimum
- 500MB disk space

### Installation

1. **Install Python dependencies:**
```bash
pip install -r requirements.txt
```

2. **Verify installation:**
```bash
python -c "import pandas, sklearn, matplotlib; print('All dependencies installed!')"
```

3. **Check data files:**
Ensure you have the following folders:
- `api_data_aadhar_enrolment/`
- `api_data_aadhar_biometric/`
- `api_data_aadhar_demographic/`

---

## Basic Usage

### Option 1: Quick Start (Recommended for First-Time Users)

**Time: ~5 minutes**

```bash
python quick_start.py
```

**What it does:**
- Loads all data
- Trains models
- Generates predictions for April 1, 2025
- Shows summary results

**Output:**
```
Total People Affected: 1,234,567
Enrolments: 789,012
Updates: 445,555
Peak Date: 2025-04-15
```

### Option 2: Complete Example

**Time: ~10 minutes**

```bash
python example_usage.py
```

**What it does:**
- Everything in Quick Start, plus:
- Generates detailed report
- Creates all visualizations
- Saves results for later use

**Output files:**
- `policy_impact_report.txt`
- `summary_dashboard.png`
- `time_series_impact.png`
- `regional_impact.png`
- `cumulative_impact.png`
- `impact_heatmap.png`

### Option 3: Full Pipeline

**Time: ~15 minutes**

```bash
python run_pipeline.py
```

**What it does:**
- Complete end-to-end workflow
- Saves all intermediate files
- Comprehensive logging

**Output files:**
- All from Option 2, plus:
- `master_aadhaar_data.csv`
- `featured_aadhaar_data.csv`
- Model files (`.pkl`)

### Option 4: Interactive Notebook

**Time: Variable (interactive)**

```bash
jupyter notebook policy_impact_analysis.ipynb
```

**What it does:**
- Step-by-step guided analysis
- Explanations for each step
- Customizable parameters
- Interactive visualizations

---

## Advanced Usage

### Python API

#### Basic Prediction

```python
from prediction_system import PolicyImpactPredictor

# Initialize
predictor = PolicyImpactPredictor()

# Load data
predictor.load_and_prepare_data()

# Predict
results = predictor.predict_policy_impact(
    policy_date="2025-04-01",
    forecast_days=60
)

# Access results
print(f"Total affected: {results['summary']['total_people_affected']:,}")
```

#### Custom Policy Date

```python
# Predict for different date
results = predictor.predict_policy_impact(
    policy_date="2025-05-15",
    forecast_days=90
)
```

#### Compare Multiple Scenarios

```python
scenarios = ["2025-04-01", "2025-05-01", "2025-06-01"]
comparison = []

for date in scenarios:
    result = predictor.predict_policy_impact(date, 30)
    comparison.append({
        'date': date,
        'total_affected': result['summary']['total_people_affected'],
        'peak_date': result['summary']['peak_impact_date']
    })

import pandas as pd
df = pd.DataFrame(comparison)
print(df)
```

#### State-Specific Analysis

```python
# Get results for specific state
state_name = "Uttar Pradesh"
regional = results['regional_impact']

print(f"{state_name}:")
print(f"  Enrolments: {regional['enrolment_impact'][state_name]:,.0f}")
print(f"  Updates: {regional['update_impact'][state_name]:,.0f}")
print(f"  Total: {regional['total_impact'][state_name]:,.0f}")
```

#### Custom Visualizations

```python
from visualization import PolicyImpactVisualizer

viz = PolicyImpactVisualizer()

# Generate specific visualization
viz.plot_time_series_impact(
    results['daily_impact'],
    results['summary']['policy_date'],
    save_path="my_custom_chart.png"
)
```

### Working with Results

#### Export to CSV

```python
# Export daily impact
results['daily_impact'].to_csv('daily_impact.csv', index=False)

# Export regional impact
import pandas as pd
regional_df = pd.DataFrame(results['regional_impact'])
regional_df.to_csv('regional_impact.csv')
```

#### Save for Later Use

```python
import pickle

# Save results
with open('my_results.pkl', 'wb') as f:
    pickle.dump(results, f)

# Load results later
with open('my_results.pkl', 'rb') as f:
    loaded_results = pickle.load(f)
```

---

## Understanding Results

### Summary Statistics

```python
summary = results['summary']
```

**Key Metrics:**

| Metric | Description | Example |
|--------|-------------|---------|
| `total_people_affected` | Total enrolments + updates | 1,234,567 |
| `total_enrolment_increase` | Additional enrolments | 789,012 |
| `total_update_increase` | Additional updates | 445,555 |
| `peak_impact_date` | Date of maximum impact | 2025-04-15 |
| `peak_impact_volume` | People affected on peak day | 45,678 |
| `significant_impact_duration_days` | Days with above-average impact | 42 |

### Regional Impact

```python
regional = results['regional_impact']
```

**Structure:**
- `enrolment_impact`: Dict[state → enrolment increase]
- `update_impact`: Dict[state → update increase]
- `total_impact`: Dict[state → total increase]

**Example:**
```python
# Top 5 affected states
top_states = sorted(
    regional['total_impact'].items(),
    key=lambda x: x[1],
    reverse=True
)[:5]

for state, impact in top_states:
    print(f"{state}: {impact:,.0f} people")
```

### Daily Impact Time Series

```python
daily = results['daily_impact']
```

**Columns:**
- `date`: Date
- `enrolment_impact`: Daily enrolment increase
- `update_impact`: Daily update increase
- `total_impact`: Daily total increase

**Example:**
```python
# Find peak day
peak_day = daily.loc[daily['total_impact'].idxmax()]
print(f"Peak: {peak_day['date']} with {peak_day['total_impact']:,.0f} people")

# Calculate cumulative
daily['cumulative'] = daily['total_impact'].cumsum()
print(f"Total after 30 days: {daily.iloc[29]['cumulative']:,.0f}")
```

### Full Predictions

```python
predictions = results['full_predictions']
```

**Contains:**
- All features used for prediction
- Baseline predictions
- Policy predictions
- Calculated impacts
- State and date information

---

## Customization

### Modify Forecast Horizon

```python
# Short-term (30 days)
results_30 = predictor.predict_policy_impact("2025-04-01", forecast_days=30)

# Medium-term (60 days)
results_60 = predictor.predict_policy_impact("2025-04-01", forecast_days=60)

# Long-term (90 days)
results_90 = predictor.predict_policy_impact("2025-04-01", forecast_days=90)
```

### Add Custom Features

Edit `feature_engineering.py`:

```python
def add_custom_features(self, df: pd.DataFrame) -> pd.DataFrame:
    """Add your custom features"""
    df = df.copy()
    
    # Example: Add holiday indicator
    holidays = ['2025-01-26', '2025-08-15', '2025-10-02']
    df['is_holiday'] = df['date'].isin(holidays).astype(int)
    
    # Example: Add season
    df['season'] = df['month'].map({
        12: 'winter', 1: 'winter', 2: 'winter',
        3: 'spring', 4: 'spring', 5: 'spring',
        6: 'summer', 7: 'summer', 8: 'summer',
        9: 'fall', 10: 'fall', 11: 'fall'
    })
    
    return df
```

### Adjust Model Parameters

Edit `baseline_model.py` or `policy_impact_model.py`:

```python
model = GradientBoostingRegressor(
    n_estimators=200,      # Increase for better accuracy
    learning_rate=0.05,    # Decrease for more stable learning
    max_depth=7,           # Increase for more complex patterns
    min_samples_split=10,  # Increase to prevent overfitting
    random_state=42
)
```

### Custom Visualizations

```python
import matplotlib.pyplot as plt

# Create custom plot
daily = results['daily_impact']

plt.figure(figsize=(12, 6))
plt.plot(daily['date'], daily['total_impact'], linewidth=2)
plt.title('My Custom Impact Chart')
plt.xlabel('Date')
plt.ylabel('People Affected')
plt.grid(True, alpha=0.3)
plt.savefig('my_chart.png', dpi=300)
plt.close()
```

---

## Troubleshooting

### Common Issues

#### 1. "File not found" error

**Problem:** CSV files not in correct location

**Solution:**
```bash
# Check if folders exist
ls api_data_aadhar_enrolment/
ls api_data_aadhar_biometric/
ls api_data_aadhar_demographic/

# Verify CSV files
ls api_data_aadhar_enrolment/api_data_aadhar_enrolment/*.csv
```

#### 2. "Module not found" error

**Problem:** Dependencies not installed

**Solution:**
```bash
pip install -r requirements.txt

# Or install individually
pip install pandas numpy scikit-learn matplotlib seaborn
```

#### 3. "Memory error"

**Problem:** Insufficient RAM

**Solution:**
- Close other applications
- Process data in chunks
- Use a machine with more RAM

#### 4. "Model not found" error

**Problem:** Models not trained yet

**Solution:**
```python
# Train models first
predictor.train_baseline()
predictor.train_policy_model("2025-04-01")

# Then predict
results = predictor.predict_policy_impact("2025-04-01", 60)
```

#### 5. Poor prediction accuracy

**Problem:** Model needs retraining or more data

**Solution:**
- Retrain with more recent data
- Adjust model hyperparameters
- Add more features
- Check data quality

### Debug Mode

Enable detailed logging:

```python
import logging
logging.basicConfig(level=logging.DEBUG)

# Run prediction
results = predictor.predict_policy_impact("2025-04-01", 60)
```

---

## FAQ

### Q1: How accurate are the predictions?

**A:** Models typically achieve R² > 0.80, meaning they explain 80%+ of variance. Accuracy depends on:
- Data quality
- Historical patterns
- Policy similarity to past events
- Forecast horizon (shorter = more accurate)

### Q2: Can I use this for real policy decisions?

**A:** This is a decision support tool. Use predictions as one input among many. Always:
- Validate with domain experts
- Consider external factors
- Test on historical events
- Monitor actual vs predicted

### Q3: How often should I retrain models?

**A:** Retrain when:
- New data is available (monthly recommended)
- Prediction accuracy drops
- Major policy changes occur
- Data patterns shift

### Q4: Can I predict multiple policies at once?

**A:** Currently, the system models one policy at a time. For multiple policies:
- Predict each separately
- Sum the impacts
- Note: This assumes independence (may not be accurate)

### Q5: What if my policy is completely new?

**A:** The model learns from historical patterns. For unprecedented policies:
- Predictions are less reliable
- Use as rough estimates only
- Consider expert judgment
- Monitor closely and adjust

### Q6: How do I interpret "significant impact duration"?

**A:** This is the number of days where impact exceeds the average. It indicates how long the surge lasts.

### Q7: Can I use this for district-level predictions?

**A:** Current version aggregates to state level. For district-level:
- Modify `data_loader.py` to aggregate by district
- Retrain models
- Note: More granular = more uncertainty

### Q8: What's the difference between baseline and policy models?

**A:**
- **Baseline**: Predicts "business as usual" without policy
- **Policy**: Predicts behavior with policy influence
- **Impact**: Difference between the two

### Q9: How do I choose the right forecast horizon?

**A:**
- **30 days**: High confidence, immediate planning
- **60 days**: Medium confidence, resource allocation
- **90+ days**: Lower confidence, strategic planning

### Q10: Can I export results to Excel?

**A:** Yes:
```python
# Export to Excel
results['daily_impact'].to_excel('daily_impact.xlsx', index=False)

# Or CSV
results['daily_impact'].to_csv('daily_impact.csv', index=False)
```

---

## Best Practices

### 1. Data Quality
- Ensure CSV files are complete
- Check for missing dates
- Verify state names are consistent
- Remove obvious outliers

### 2. Model Training
- Retrain monthly with new data
- Validate on historical events
- Monitor prediction accuracy
- Adjust hyperparameters if needed

### 3. Interpretation
- Consider confidence levels
- Compare multiple scenarios
- Validate with domain experts
- Account for external factors

### 4. Reporting
- Include methodology explanation
- Show uncertainty ranges
- Provide context and assumptions
- Update stakeholders regularly

### 5. Continuous Improvement
- Track actual vs predicted
- Collect feedback
- Refine features
- Update documentation

---

## Getting Help

### Resources
- **README.md**: Overview and quick start
- **METHODOLOGY.md**: Technical details
- **ARCHITECTURE.md**: System design
- **PROJECT_SUMMARY.md**: Executive summary

### Support
- Check documentation first
- Review example scripts
- Try the Jupyter notebook
- Examine error messages carefully

---

## Next Steps

After mastering basic usage:

1. **Experiment** with different policy dates
2. **Compare** multiple scenarios
3. **Customize** features and models
4. **Validate** on historical events
5. **Integrate** into your workflow
6. **Share** insights with stakeholders

---

**Happy Predicting!** 🚀
