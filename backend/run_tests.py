#!/usr/bin/env python3
"""
Test runner script for the backend services
"""
import os
import sys
import subprocess

def run_tests():
    """Run all tests with coverage"""
    print("🧪 Running Backend Unit Tests...")
    
    # Change to backend directory
    backend_dir = os.path.dirname(os.path.abspath(__file__))
    os.chdir(backend_dir)
    

    # Run tests
    test_commands = [
        # Run all service tests
        [sys.executable, '-m', 'pytest', 'tests/unit/', '-v'],
        
        # Run with coverage
        [sys.executable, '-m', 'pytest', 'tests/unit/', '--cov=app/services', '--cov-report=html', '--cov-report=term-missing'],
        
        # Run specific service tests (examples)
        # [sys.executable, '-m', 'pytest', 'tests/unit/test_auth_service.py', '-v'],
        # [sys.executable, '-m', 'pytest', 'tests/unit/test_post_service.py', '-v'],
    ]
    
    for cmd in test_commands:
        print(f"Running: {' '.join(cmd)}")
        result = subprocess.run(cmd)
        if result.returncode != 0:
            print(f"❌ Test command failed: {' '.join(cmd)}")
            return False
    
    print("✅ All tests completed successfully!")
    return True

if __name__ == '__main__':
    success = run_tests()
    sys.exit(0 if success else 1)