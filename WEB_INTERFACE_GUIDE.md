# 🌐 Policy Scenario Builder - Web Interface Guide

## Overview

The **Policy Scenario Builder** is an interactive web application that allows policymakers to define hypothetical Aadhaar policies and instantly see predicted regional impacts.

---

## 🚀 Quick Start

### Step 1: Install Dependencies

```bash
pip install -r requirements.txt
```

This will install Flask and all other required packages.

### Step 2: Start the Web Server

```bash
python app.py
```

You'll see:
```
Starting Policy Scenario Builder...
Open http://localhost:5000 in your browser
 * Running on http://0.0.0.0:5000
```

### Step 3: Open in Browser

Open your web browser and go to:
```
http://localhost:5000
```

### Step 4: Define Your Policy

Fill in the form with your policy details and click "Predict Impact"!

---

## 📋 Interface Features

### 1. Policy Input Section

#### Required Fields:

**Policy Name**
- Example: "Mandatory Biometric Update 2025"
- Purpose: Give your policy a descriptive name

**Policy Start Date**
- Format: YYYY-MM-DD
- Example: 2025-06-01
- Purpose: When will the policy be implemented?

**Policy Type**
- Options:
  - Both (Enrolment + Update)
  - Enrolment Only
  - Update Only
- Purpose: What type of Aadhaar action is required?

#### Optional Filters:

**Affected Age Group**
- Options: 0-5 years, 5-17 years, 18+ years
- Multi-select (hold Ctrl/Cmd)
- Purpose: Target specific age demographics

**Affected States**
- Options: All States, or select specific states
- Multi-select
- Purpose: Limit policy to certain regions

**Expected Compliance Level**
- Range: 0% to 100%
- Default: 80%
- Purpose: What percentage of affected people will comply?

**Forecast Period**
- Options: 30, 60, or 90 days
- Default: 60 days
- Purpose: How far ahead to predict?

---

### 2. Results Section

After clicking "Predict Impact", you'll see:

#### Summary Cards (6 metrics):

1. **Total People Affected** - Overall impact
2. **Peak Date** - When maximum load occurs
3. **Peak Volume** - Maximum daily volume
4. **Enrolments** - Total new enrolments
5. **Updates** - Total updates
6. **Duration** - Days of significant impact

#### Regional Impact Table:

| Column | Description |
|--------|-------------|
| State | State name |
| Enrolments | Predicted new enrolments |
| Updates | Predicted updates |
| Total Impact | Combined impact |
| % Increase | Percentage increase over baseline |
| Risk Level | High / Medium / Low |

#### Visual Analysis:

4 charts showing:
1. **Daily Impact Over Time** - Time series
2. **Top 10 Affected States** - Bar chart
3. **Enrolment vs Update Impact** - Comparison
4. **Risk Level Distribution** - Pie chart

---

## 🎯 Example Use Cases

### Use Case 1: Mandatory Biometric Update

**Scenario:** All citizens above 18 must update biometric data

**Input:**
```
Policy Name: Mandatory Biometric Update 2025
Policy Date: 2025-06-01
Policy Type: Update Only
Age Groups: 18+ years
States: All States
Compliance: 80%
Forecast: 60 days
```

**Expected Output:**
- Total affected: ~1.2M people
- Peak date: ~15 days after policy
- High-risk states: UP, Maharashtra, Bihar

### Use Case 2: Student Scholarship Program

**Scenario:** Scholarship requires Aadhaar for students aged 5-17

**Input:**
```
Policy Name: Student Scholarship 2025
Policy Date: 2025-07-01
Policy Type: Both
Age Groups: 5-17 years
States: All States
Compliance: 90%
Forecast: 90 days
```

**Expected Output:**
- Total affected: ~800K people
- Peak date: ~20 days after policy
- Focus on states with high student population

### Use Case 3: Regional Pilot Program

**Scenario:** Test policy in 3 states first

**Input:**
```
Policy Name: Regional Pilot - Biometric Update
Policy Date: 2025-05-01
Policy Type: Update Only
Age Groups: All
States: Uttar Pradesh, Maharashtra, Karnataka
Compliance: 70%
Forecast: 60 days
```

**Expected Output:**
- Total affected: ~400K people
- Regional focus on selected states
- Lower compliance = lower impact

---

## 🔧 Technical Details

### Architecture

```
┌─────────────────┐
│   Web Browser   │
│   (Frontend)    │
└────────┬────────┘
         │ HTTP
         ▼
┌─────────────────┐
│   Flask App     │
│   (Backend)     │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│  Prediction     │
│  System         │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│  ML Models      │
│  (Trained)      │
└─────────────────┘
```

### API Endpoints

#### 1. GET /
- Returns the main HTML page

#### 2. GET /api/states
- Returns list of available states
- Response:
```json
{
  "states": ["Andhra Pradesh", "Bihar", ...]
}
```

#### 3. POST /api/predict
- Accepts policy parameters
- Returns predictions
- Request:
```json
{
  "policy_name": "My Policy",
  "policy_date": "2025-06-01",
  "policy_type": "Both",
  "age_groups": ["18+"],
  "states": ["All States"],
  "compliance_level": 0.8,
  "forecast_days": 60
}
```
- Response:
```json
{
  "success": true,
  "summary": {
    "total_people_affected": 1234567,
    "total_enrolments": 789012,
    "total_updates": 445555,
    "peak_date": "2025-06-15",
    "peak_volume": 45678,
    "duration_days": 42
  },
  "regional_impact": [...],
  "daily_impact": [...],
  "risk_assessment": {...}
}
```

#### 4. POST /api/visualize
- Generates visualization charts
- Returns base64-encoded image

---

## 🎨 Customization

### Change Colors

Edit `templates/index.html`, find the CSS section:

```css
/* Primary gradient */
background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);

/* Change to your colors */
background: linear-gradient(135deg, #YOUR_COLOR1 0%, #YOUR_COLOR2 100%);
```

### Add New Fields

1. **Add HTML input** in `templates/index.html`:
```html
<div class="form-group">
    <label for="myNewField">My New Field</label>
    <input type="text" id="myNewField">
</div>
```

2. **Collect in JavaScript**:
```javascript
const formData = {
    // ... existing fields
    my_new_field: document.getElementById('myNewField').value
};
```

3. **Process in backend** (`app.py`):
```python
my_new_field = data.get('my_new_field')
# Use in prediction logic
```

### Modify Risk Levels

Edit `app.py`, find `apply_policy_filters()`:

```python
# Current thresholds
if pct_increase > 50:
    risk_level = 'High'
elif pct_increase > 25:
    risk_level = 'Medium'
else:
    risk_level = 'Low'

# Change to your thresholds
if pct_increase > 75:  # More strict
    risk_level = 'High'
elif pct_increase > 40:
    risk_level = 'Medium'
else:
    risk_level = 'Low'
```

---

## 🐛 Troubleshooting

### Issue 1: Port Already in Use

**Error:** `Address already in use`

**Solution:**
```bash
# Change port in app.py
app.run(debug=True, host='0.0.0.0', port=5001)  # Use 5001 instead
```

### Issue 2: Models Not Found

**Error:** `Model file not found`

**Solution:**
```bash
# Train models first
python quick_start.py
# Then start web app
python app.py
```

### Issue 3: Slow Predictions

**Cause:** First prediction trains models

**Solution:**
- First prediction takes 30-60 seconds (model training)
- Subsequent predictions are faster (5-10 seconds)
- Models are cached in memory

### Issue 4: Browser Can't Connect

**Error:** `Unable to connect`

**Solution:**
1. Check if server is running
2. Try `http://127.0.0.1:5000` instead of `localhost`
3. Check firewall settings

---

## 📊 Understanding Results

### Risk Levels

- **High Risk** (Red): >50% increase, needs immediate attention
- **Medium Risk** (Yellow): 25-50% increase, monitor closely
- **Low Risk** (Gray): <25% increase, normal capacity

### Peak Date

- Usually 10-20 days after policy start
- When system load is maximum
- Plan extra resources for this period

### Duration

- Number of days with above-average impact
- Typical range: 30-60 days
- Longer duration = sustained impact

### Compliance Level

- 100% = Everyone complies immediately
- 80% = Realistic for mandatory policies
- 50% = Voluntary or low-awareness policies
- Adjust based on policy enforcement

---

## 🚀 Deployment

### Local Network Access

To allow others on your network to access:

```python
# In app.py
app.run(debug=False, host='0.0.0.0', port=5000)
```

Then share: `http://YOUR_IP_ADDRESS:5000`

### Production Deployment

For production use, consider:

1. **Use Gunicorn** (production server):
```bash
pip install gunicorn
gunicorn -w 4 -b 0.0.0.0:5000 app:app
```

2. **Use Nginx** (reverse proxy)
3. **Enable HTTPS**
4. **Add authentication**
5. **Set up monitoring**

---

## 💡 Best Practices

### 1. Start with Realistic Compliance

- Don't assume 100% compliance
- Use 70-80% for mandatory policies
- Use 40-60% for voluntary policies

### 2. Compare Multiple Scenarios

- Test 2-3 different dates
- Try different compliance levels
- Compare regional vs national rollout

### 3. Focus on High-Risk States

- Allocate extra resources
- Plan capacity upgrades
- Set up monitoring

### 4. Use Appropriate Forecast Period

- 30 days: Immediate planning
- 60 days: Resource allocation (recommended)
- 90 days: Strategic planning

### 5. Validate with Historical Data

- Compare predictions with past policies
- Adjust compliance levels based on history
- Refine risk thresholds

---

## 📈 Advanced Features

### Export Results

Add export button in HTML:

```html
<button onclick="exportResults()">Export to CSV</button>

<script>
function exportResults() {
    // Convert table to CSV
    const table = document.getElementById('regionalTable');
    let csv = [];
    for (let row of table.rows) {
        let rowData = [];
        for (let cell of row.cells) {
            rowData.push(cell.textContent);
        }
        csv.push(rowData.join(','));
    }
    
    // Download
    const blob = new Blob([csv.join('\n')], { type: 'text/csv' });
    const url = window.URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = 'policy_impact.csv';
    a.click();
}
</script>
```

### Save Scenarios

Add scenario saving:

```javascript
function saveScenario() {
    const scenario = {
        name: document.getElementById('policyName').value,
        date: document.getElementById('policyDate').value,
        results: currentResults
    };
    
    localStorage.setItem('scenario_' + Date.now(), JSON.stringify(scenario));
    alert('Scenario saved!');
}
```

### Compare Scenarios

Add comparison view to show multiple scenarios side-by-side.

---

## 🎓 Training Materials

### For Policymakers

1. **Video Tutorial**: Record screen showing how to use interface
2. **Quick Reference Card**: Print-friendly one-page guide
3. **Example Scenarios**: Pre-filled examples to learn from

### For Technical Staff

1. **API Documentation**: Detailed endpoint specs
2. **Customization Guide**: How to modify and extend
3. **Troubleshooting**: Common issues and solutions

---

## 📞 Support

### Common Questions

**Q: How accurate are the predictions?**
A: Models achieve 80%+ accuracy. Use as decision support, not absolute truth.

**Q: Can I predict for past dates?**
A: Yes, for validation purposes.

**Q: How do I add new states?**
A: States are loaded from data automatically.

**Q: Can I run multiple predictions simultaneously?**
A: Yes, but each takes 5-10 seconds.

**Q: Is data saved?**
A: No, all predictions are in-memory only (privacy-preserving).

---

## 🎉 You're Ready!

Start the web interface:
```bash
python app.py
```

Open browser:
```
http://localhost:5000
```

Define your policy and see instant predictions!

---

**For more help, see:**
- `README.md` - System overview
- `USER_GUIDE.md` - Detailed usage
- `HOW_TO_ADD_POLICY.md` - Policy configuration
