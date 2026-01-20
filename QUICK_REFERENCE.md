# Quick Reference Card

## 🚀 One-Minute Start

```bash
# Install dependencies
pip install -r requirements.txt

# Run prediction
python quick_start.py
```

## 📋 Common Commands

### Get Predictions
```bash
python quick_start.py              # Fastest (5 min)
python example_usage.py            # Complete (10 min)
python run_pipeline.py             # Full pipeline (15 min)
jupyter notebook policy_impact_analysis.ipynb  # Interactive
```

### Python API
```python
from prediction_system import PolicyImpactPredictor

predictor = PolicyImpactPredictor()
predictor.load_and_prepare_data()

results = predictor.predict_policy_impact(
    policy_date="2025-04-01",
    forecast_days=60
)

print(f"Total affected: {results['summary']['total_people_affected']:,}")
```

## 📊 Key Results

### Access Summary
```python
summary = results['summary']
print(f"Total people: {summary['total_people_affected']:,}")
print(f"Peak date: {summary['peak_impact_date']}")
print(f"Duration: {summary['significant_impact_duration_days']} days")
```

### Access Regional Data
```python
regional = results['regional_impact']
top_states = sorted(regional['total_impact'].items(), 
                   key=lambda x: x[1], reverse=True)[:5]
```

### Access Time Series
```python
daily = results['daily_impact']
daily.plot(x='date', y='total_impact')
```

## 🎯 Common Tasks

| Task | Command |
|------|---------|
| First run | `python quick_start.py` |
| Full analysis | `python example_usage.py` |
| Different date | Change `POLICY_DATE` variable |
| Longer forecast | Change `FORECAST_DAYS` variable |
| Export CSV | `results['daily_impact'].to_csv('output.csv')` |
| Save results | `pickle.dump(results, open('results.pkl', 'wb'))` |

## 📁 Key Files

| File | Purpose |
|------|---------|
| `quick_start.py` | Fastest way to get predictions |
| `example_usage.py` | Complete example with visualizations |
| `policy_impact_analysis.ipynb` | Interactive tutorial |
| `README.md` | Main documentation |
| `USER_GUIDE.md` | Detailed usage guide |

## 🔧 Troubleshooting

| Problem | Solution |
|---------|----------|
| Module not found | `pip install -r requirements.txt` |
| File not found | Check data folders exist |
| Model not found | Run training first |
| Memory error | Close other apps, use smaller forecast |

## 📖 Documentation

- **Getting Started**: README.md
- **Usage Guide**: USER_GUIDE.md
- **How It Works**: METHODOLOGY.md
- **System Design**: ARCHITECTURE.md
- **All Docs**: INDEX.md

## 💡 Quick Tips

1. Start with `quick_start.py`
2. Use notebook for learning
3. Read USER_GUIDE.md for details
4. Check METHODOLOGY.md to understand approach
5. Customize in `prediction_system.py`

## 📞 Help

- **Errors**: USER_GUIDE.md → Troubleshooting
- **Questions**: USER_GUIDE.md → FAQ
- **Examples**: example_usage.py
- **API**: USER_GUIDE.md → Advanced Usage

## 🎓 Learning Path

1. Run `quick_start.py` (5 min)
2. Read PROJECT_SUMMARY.md (10 min)
3. Open policy_impact_analysis.ipynb (30 min)
4. Read USER_GUIDE.md (as needed)

---

**Need more help?** See INDEX.md for complete documentation guide.
