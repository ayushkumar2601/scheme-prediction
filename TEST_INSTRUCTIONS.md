# Testing Instructions

## Quick Test Steps

### 1. Clean Start (Recommended)
Delete these cached files to ensure fresh data:
```
del master_aadhaar_data.csv
del *.pkl
```

### 2. Start Web Interface
```
python start_web_interface.py
```

### 3. Test Duration Fix
1. Open http://localhost:5000
2. Fill in policy details:
   - Policy Name: Test Policy
   - Policy Date: Any future date
   - Policy Type: **Both**
   - Forecast Period: **30 days**
3. Click "Predict Impact"
4. Check results:
   - **Duration should show: 30 days** ✓

### 4. Test Updates Issue
1. Look at the console/terminal where you started the web interface
2. You should see DEBUG messages like:
   ```
   DEBUG - Raw values from model:
     Enrolment increase: 12345
     Update increase: 67890  <-- This should NOT be 0
     After compliance (0.8):
     Enrolments: 9876
     Updates: 54312  <-- This should NOT be 0
     Policy type 'Both' - keeping both values
   
   DEBUG - Daily data summary:
     Total days: 30
     Total daily updates: 54312  <-- This should NOT be 0
   
   DEBUG - Regional data summary:
     Total states: 36
     Total regional updates: 54312  <-- This should NOT be 0
   ```

3. Check the web results:
   - **Total Updates** should be non-zero
   - **Regional Impact table** should show non-zero updates

## What to Report

If updates are still 0, please copy and paste:
1. The DEBUG messages from the console
2. The values shown in the web interface

This will help identify exactly where the updates are being lost.

## Expected Behavior

✅ **Duration**: Should exactly match your selected forecast period (30 days → 30 days)
✅ **Updates**: Should show positive numbers when policy type is "Both" or "Update"

## Quick Data Check

To verify your data has updates, run:
```
python test_updates_data.py
```

Should show:
- Total updates: ~119 million
- Records with updates: ~89%
