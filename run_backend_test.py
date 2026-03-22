#!/usr/bin/env python3
"""
Run backend test from root directory
"""

import sys
import os
import subprocess

def run_test():
    """Run the backend test"""
    try:
        # Change to backend directory and run test
        backend_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'backend')
        test_file = os.path.join(backend_dir, 'test_fixed_backend.py')
        
        print(f"Running test from: {backend_dir}")
        print(f"Test file: {test_file}")
        
        # Run the test
        result = subprocess.run([
            sys.executable, 'test_fixed_backend.py'
        ], cwd=backend_dir, capture_output=True, text=True)
        
        print("=== Test Output ===")
        print(result.stdout)
        
        if result.stderr:
            print("=== Test Errors ===")
            print(result.stderr)
        
        return result.returncode == 0
        
    except Exception as e:
        print(f"Failed to run test: {e}")
        return False

if __name__ == "__main__":
    success = run_test()
    sys.exit(0 if success else 1)