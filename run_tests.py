#!/usr/bin/env python3
"""
Test runner for SecureApp
Runs all tests and reports results
"""
import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))

def run_tests():
    """Run all test modules"""
    print("=" * 60)
    print("Running SecureApp Test Suite")
    print("=" * 60)
    print()
    
    test_modules = [
        'tests.test_password_utils',
        'tests.test_sanitizer',
        'tests.test_encryption',
        'tests.test_auth'
    ]
    
    failed = []
    passed = []
    
    for module_name in test_modules:
        print(f"\n{'=' * 60}")
        print(f"Testing: {module_name}")
        print('=' * 60)
        
        try:
            module = __import__(module_name, fromlist=[''])
            
            # Get all test functions
            test_functions = [
                getattr(module, name) 
                for name in dir(module) 
                if name.startswith('test_') and callable(getattr(module, name))
            ]
            
            for test_func in test_functions:
                try:
                    test_func()
                    print(f"  ✓ {test_func.__name__}")
                    passed.append(f"{module_name}.{test_func.__name__}")
                except Exception as e:
                    print(f"  ✗ {test_func.__name__}: {str(e)}")
                    failed.append(f"{module_name}.{test_func.__name__}")
        
        except Exception as e:
            print(f"  ✗ Failed to import module: {str(e)}")
            failed.append(module_name)
    
    # Print summary
    print("\n\n" + "=" * 60)
    print("Test Summary")
    print("=" * 60)
    print(f"Passed: {len(passed)}")
    print(f"Failed: {len(failed)}")
    
    if failed:
        print("\nFailed tests:")
        for test in failed:
            print(f"  ✗ {test}")
        sys.exit(1)
    else:
        print("\n✓ All tests passed!")
        sys.exit(0)


if __name__ == "__main__":
    run_tests()
