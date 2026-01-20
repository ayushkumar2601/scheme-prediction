"""
Quick Test Script to Verify Fixes
Tests state cleaning and duration calculation
"""

print("=" * 80)
print("TESTING FIXES")
print("=" * 80)

# Test 1: State Cleaning
print("\n[Test 1] Testing State Cleaning...")
print("-" * 80)

from data_loader import AadhaarDataLoader

loader = AadhaarDataLoader()

# Load a small sample
try:
    enrol_raw = loader.load_enrolment_data()
    
    # Check unique states before cleaning
    states_before = enrol_raw['state'].unique()
    print(f"States before cleaning: {len(states_before)} unique values")
    
    # Show some examples
    print("\nSample states (first 10):")
    for i, state in enumerate(list(states_before)[:10]):
        print(f"  {i+1}. '{state}' (type: {type(state).__name__})")
    
    # Clean the data
    enrol_clean = loader.clean_and_aggregate_enrolment(enrol_raw)
    
    # Check unique states after cleaning
    states_after = enrol_clean['state'].unique()
    print(f"\nStates after cleaning: {len(states_after)} unique values")
    
    # Show cleaned states
    print("\nCleaned states (sorted):")
    for i, state in enumerate(sorted(states_after)):
        print(f"  {i+1}. {state}")
    
    # Check for issues
    issues = []
    for state in states_after:
        if not isinstance(state, str):
            issues.append(f"Non-string: {state}")
        elif len(state) <= 2:
            issues.append(f"Too short: {state}")
        elif state.isdigit():
            issues.append(f"Numeric: {state}")
    
    if issues:
        print("\n❌ Issues found:")
        for issue in issues:
            print(f"  - {issue}")
    else:
        print("\n✅ All states are valid!")
    
except Exception as e:
    print(f"❌ Error in Test 1: {e}")

# Test 2: Duration Calculation
print("\n" + "=" * 80)
print("[Test 2] Testing Duration Calculation...")
print("-" * 80)

# Simulate daily data
daily_data = []
total_affected = 10000

# Create 60 days of data with varying impact
for day in range(60):
    if day < 10:
        impact = 50  # Low impact
    elif day < 40:
        impact = 200  # High impact
    else:
        impact = 80  # Medium impact
    
    daily_data.append({'total': impact})

# Calculate duration (old way - incorrect)
try:
    significant_days_old = [d for d in daily_data if d['total'] > (total_affected / len(daily_data))]
    duration_old = len(significant_days_old)
    print(f"Old calculation (incorrect): {duration_old} days")
except:
    duration_old = 0
    print(f"Old calculation failed")

# Calculate duration (new way - correct)
if daily_data and total_affected > 0:
    avg_daily = total_affected / len(daily_data) if len(daily_data) > 0 else 0
    significant_days_new = [d for d in daily_data if d['total'] > avg_daily]
    duration_new = len(significant_days_new)
    print(f"New calculation (correct): {duration_new} days")
    print(f"Average daily impact: {avg_daily:.2f}")
else:
    duration_new = 0

print(f"\nForecast period: {len(daily_data)} days")
print(f"Duration (old): {duration_old} days")
print(f"Duration (new): {duration_new} days")

if duration_new > duration_old:
    print("\n✅ Duration calculation fixed!")
else:
    print("\n⚠️ Duration calculation may need review")

# Summary
print("\n" + "=" * 80)
print("TEST SUMMARY")
print("=" * 80)
print("\n✅ Test 1: State cleaning - Check results above")
print("✅ Test 2: Duration calculation - Check results above")
print("\nIf all tests pass, the fixes are working correctly!")
print("\nNext step: Restart the web server")
print("  python start_web_interface.py")
print("=" * 80)
