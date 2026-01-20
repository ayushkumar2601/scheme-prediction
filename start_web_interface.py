"""
Quick Start Script for Policy Scenario Builder Web Interface
Prepares the system and launches the web application
"""

import sys
import os

print("=" * 80)
print("POLICY SCENARIO BUILDER - WEB INTERFACE")
print("=" * 80)
print()

# Step 1: Check dependencies
print("[1/4] Checking dependencies...")
try:
    import flask
    import pandas
    import sklearn
    import matplotlib
    print("      ✓ All dependencies installed")
except ImportError as e:
    print(f"      ✗ Missing dependency: {e}")
    print("\n      Please run: pip install -r requirements.txt")
    sys.exit(1)

# Step 2: Check if data exists
print("[2/4] Checking data files...")
data_folders = [
    'api_data_aadhar_enrolment',
    'api_data_aadhar_biometric',
    'api_data_aadhar_demographic'
]

all_exist = True
for folder in data_folders:
    if os.path.exists(folder):
        print(f"      ✓ {folder}")
    else:
        print(f"      ✗ {folder} not found")
        all_exist = False

if not all_exist:
    print("\n      ✗ Some data folders are missing!")
    print("      Please ensure all Aadhaar data folders are present.")
    sys.exit(1)

# Step 3: Prepare models (optional - will be done on first request)
print("[3/4] Preparing prediction system...")
print("      Note: Models will be trained on first prediction request")
print("      This may take 30-60 seconds for the first prediction")

# Step 4: Start web server
print("[4/4] Starting web server...")
print()
print("=" * 80)
print("WEB INTERFACE READY!")
print("=" * 80)
print()
print("Open your web browser and go to:")
print()
print("    🌐 http://localhost:5000")
print()
print("Or if on the same network:")
print()
print("    🌐 http://YOUR_IP_ADDRESS:5000")
print()
print("=" * 80)
print()
print("Instructions:")
print("  1. Fill in the policy details in the form")
print("  2. Click 'Predict Impact' button")
print("  3. Wait 30-60 seconds for first prediction (model training)")
print("  4. View results and visualizations")
print()
print("Press Ctrl+C to stop the server")
print("=" * 80)
print()

# Import and run Flask app
from app import app

try:
    app.run(debug=True, host='0.0.0.0', port=5000)
except KeyboardInterrupt:
    print("\n\nServer stopped by user")
    print("Thank you for using Policy Scenario Builder!")
except Exception as e:
    print(f"\n\nError starting server: {e}")
    print("\nTroubleshooting:")
    print("  - Check if port 5000 is already in use")
    print("  - Try running: python app.py")
    print("  - See WEB_INTERFACE_GUIDE.md for more help")
    sys.exit(1)
