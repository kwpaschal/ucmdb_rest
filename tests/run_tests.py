"""
Test runner for ucmdb_rest library

Usage:
    python run_tests.py              # Run all tests in mock mode
    python run_tests.py --live       # Run all tests including live server tests
    python run_tests.py --coverage   # Run with coverage report
"""

import sys
import os
import unittest
import argparse

# Add parent directory to path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))


def main():
    parser = argparse.ArgumentParser(description='Run ucmdb_rest tests')
    parser.add_argument('--live', action='store_true',
                        help='Run live tests against real UCMDB server')
    parser.add_argument('--coverage', action='store_true',
                        help='Run with coverage report')
    parser.add_argument('--verbose', '-v', action='store_true',
                        help='Verbose output')
    args = parser.parse_args()

    # Set environment variable for live tests
    if args.live:
        os.environ['UCMDB_TEST_LIVE'] = 'true'
        print("Running tests in LIVE mode (requires credentials.json)")
    else:
        os.environ['UCMDB_TEST_LIVE'] = 'false'
        print("Running tests in MOCK mode")

    # Discover and run tests
    loader = unittest.TestLoader()
    start_dir = os.path.dirname(__file__)
    suite = loader.discover(start_dir, pattern='test*.py')

    # Run tests
    verbosity = 2 if args.verbose else 1
    runner = unittest.TextTestRunner(verbosity=verbosity)

    if args.coverage:
        try:
            import coverage
            cov = coverage.Coverage()
            cov.start()

            result = runner.run(suite)

            cov.stop()
            cov.save()

            print("\n" + "="*80)
            print("Coverage Report")
            print("="*80)
            cov.report()

            # Generate HTML report
            cov.html_report(directory='htmlcov')
            print("\nHTML coverage report generated in htmlcov/")

        except ImportError:
            print("\nWarning: coverage module not installed.")
            print("Install with: pip install coverage")
            print("Running tests without coverage...\n")
            result = runner.run(suite)
    else:
        result = runner.run(suite)

    # Exit with appropriate code
    sys.exit(0 if result.wasSuccessful() else 1)


if __name__ == '__main__':
    main()
