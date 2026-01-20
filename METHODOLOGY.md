# Methodology: Aadhaar Policy Impact Prediction

## Executive Summary

This document explains the technical approach used to predict the impact of Aadhaar policy changes on enrolment and update volumes.

## Problem Statement

When UIDAI implements a new policy (e.g., mandatory biometric update, new enrolment requirements), there is typically a surge in:
1. New enrolments
2. Biometric updates
3. Demographic updates

The challenge is to predict:
- **How many people** will be affected
- **Which regions** will see the most impact
- **How long** the surge will last
- **When** the peak will occur

## Approach

### 1. Interrupted Time Series Analysis (ITSA)

We use ITSA to model the effect of policy interventions on time-series data.

**Key Concept**: Compare what *would have happened* (baseline) vs what *actually happens* (with policy).

```
Impact = Observed Volume (with policy) - Expected Volume (without policy)
```

### 2. Two-Model Architecture

#### Model A: Baseline Model
- Learns normal enrolment/update patterns
- Trained on features WITHOUT policy indicators
- Captures seasonal trends, day-of-week effects, state variations
- Predicts "business as usual" volumes

#### Model B: Policy Impact Model
- Learns behavior INCLUDING policy effects
- Trained on features WITH policy indicators
- Captures surge patterns after policy implementation
- Predicts volumes under policy influence

### 3. Feature Engineering

#### Temporal Features
- Year, month, day, day of week
- Week of year
- Weekend indicator

#### Lag Features
- Previous 1, 7, 14, 30 days volumes
- Captures short and medium-term trends

#### Rolling Statistics
- 7-day, 14-day, 30-day rolling means
- Rolling standard deviations
- Captures volatility and trends

#### Growth Features
- Day-over-day growth rate
- Week-over-week growth rate
- Identifies acceleration patterns

#### Policy Features
- `policy_active`: Binary (0 before, 1 after policy date)
- `days_from_policy`: Days since/until policy
- `pre_policy_30d`: 30 days before policy window
- `post_policy_30d`: 30 days after policy window
- `post_policy_60d`: 60 days after policy window

#### State Features
- State average enrolments/updates
- Deviation from state average
- Captures regional variations

### 4. Model Selection

**Gradient Boosting Regressor** chosen for:
- Handles non-linear relationships
- Robust to outliers
- Captures complex interactions
- Good performance on time-series data
- Feature importance analysis

Hyperparameters:
- n_estimators: 100-150
- learning_rate: 0.1
- max_depth: 5-6
- random_state: 42 (reproducibility)

### 5. Training Strategy

#### Phase 1: Baseline Training
```python
# Train on all data without policy features
X = temporal + lag + rolling + growth + state features
y = total_enrolments (or total_updates)

baseline_model.fit(X, y)
```

#### Phase 2: Policy Impact Training
```python
# Train on data with policy features
X = temporal + lag + rolling + growth + state + policy features
y = total_enrolments (or total_updates)

policy_model.fit(X, y)
```

### 6. Prediction Process

For a new policy date:

1. **Create forecast dataset**
   - Generate dates from policy date to forecast horizon
   - Include all states
   - Initialize with historical averages

2. **Add features**
   - Compute all temporal, lag, rolling features
   - Add policy features based on policy date

3. **Generate baseline prediction**
   ```python
   baseline_volume = baseline_model.predict(features_without_policy)
   ```

4. **Generate policy prediction**
   ```python
   policy_volume = policy_model.predict(features_with_policy)
   ```

5. **Calculate impact**
   ```python
   impact = policy_volume - baseline_volume
   ```

6. **Aggregate results**
   - Sum by date (daily impact)
   - Sum by state (regional impact)
   - Cumulative totals

### 7. Evaluation Metrics

- **MAE (Mean Absolute Error)**: Average prediction error
- **RMSE (Root Mean Squared Error)**: Penalizes large errors
- **R² Score**: Proportion of variance explained

Target performance:
- R² > 0.80 for both models
- MAE < 10% of mean volume

### 8. Assumptions

1. **Historical patterns repeat**: Future policy responses similar to past
2. **Linear additivity**: Policy impact adds to baseline
3. **State independence**: States respond independently
4. **No external shocks**: No major unforeseen events
5. **Data quality**: Input data is accurate and complete

### 9. Limitations

1. **Novel policies**: May not predict unprecedented policy types
2. **External factors**: Cannot account for economic shocks, pandemics, etc.
3. **Interaction effects**: Multiple simultaneous policies not modeled
4. **Lag in response**: Assumes immediate policy awareness
5. **Capacity constraints**: Doesn't model system capacity limits

### 10. Validation Approach

To validate the model:

1. **Historical backtesting**
   - Identify past policy events
   - Train on data before policy
   - Predict impact
   - Compare with actual observed impact

2. **Cross-validation**
   - Time-series cross-validation
   - Ensure no data leakage

3. **Sensitivity analysis**
   - Test with different policy dates
   - Vary forecast horizons
   - Check robustness

### 11. Interpretation Guidelines

#### Confidence Levels
- **High confidence**: 30-day forecast, major states
- **Medium confidence**: 60-day forecast, medium states
- **Low confidence**: 90+ day forecast, small states

#### When to Trust Predictions
- Historical data covers similar policies
- Stable recent trends
- High model R² scores
- Consistent across scenarios

#### When to Be Cautious
- Novel policy types
- Recent data anomalies
- Low model performance
- High prediction variance

### 12. Example Calculation

**Scenario**: Mandatory biometric update policy on April 1, 2025

**Step 1**: Baseline prediction for April 15, 2025 in Uttar Pradesh
```
baseline_enrolments = 5,000 (normal day)
baseline_updates = 3,000 (normal day)
```

**Step 2**: Policy-influenced prediction
```
policy_enrolments = 8,000 (with surge)
policy_updates = 7,500 (with surge)
```

**Step 3**: Calculate impact
```
enrolment_impact = 8,000 - 5,000 = 3,000 additional
update_impact = 7,500 - 3,000 = 4,500 additional
total_impact = 7,500 people affected
```

**Step 4**: Aggregate across all states and days
```
Total 60-day impact = Sum of daily impacts across all states
```

## Conclusion

This methodology provides a systematic, data-driven approach to predicting policy impacts. While not perfect, it offers valuable insights for resource planning and decision-making.

The key innovation is the two-model comparison: baseline vs policy-influenced, which isolates the incremental effect of the policy intervention.

## References

- Interrupted Time Series Analysis (ITSA) in policy evaluation
- Gradient Boosting for time-series forecasting
- Feature engineering for temporal data
- UIDAI data standards and guidelines
