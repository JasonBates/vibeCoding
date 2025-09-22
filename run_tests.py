#!/usr/bin/env python3
"""Test runner script for different types of tests."""

import argparse
import os
import subprocess
import sys

from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()


def run_command(cmd, description):
    """Run a command and handle errors."""
    print(f"\n{'='*60}")
    print(f"Running: {description}")
    print(f"Command: {' '.join(cmd)}")
    print(f"{'='*60}")

    try:
        result = subprocess.run(cmd, check=True, capture_output=False)
        print(f"✅ {description} completed successfully")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ {description} failed with exit code {e.returncode}")
        return False


def main():
    parser = argparse.ArgumentParser(description="Run different types of tests")
    parser.add_argument(
        "test_type",
        choices=["unit", "integration", "e2e", "all", "fast"],
        help="Type of tests to run",
    )
    parser.add_argument(
        "--coverage", action="store_true", help="Run with coverage reporting"
    )
    parser.add_argument(
        "--verbose", action="store_true", help="Run with verbose output"
    )

    args = parser.parse_args()

    # Base pytest command
    base_cmd = ["python", "-m", "pytest"]

    if args.verbose:
        base_cmd.append("-v")

    if args.coverage:
        base_cmd.extend(["--cov=.", "--cov-report=html", "--cov-report=term"])

    # Test type specific commands
    if args.test_type == "unit":
        # Run only unit tests (exclude integration and e2e)
        cmd = base_cmd + ["tests/", "-m", "not integration and not e2e"]
        success = run_command(cmd, "Unit Tests")

    elif args.test_type == "integration":
        # Check for API key
        if not os.getenv("OPENAI_API_KEY"):
            print(
                "❌ OPENAI_API_KEY not found. Integration tests require a real API key."
            )
            print("   Set your API key: export OPENAI_API_KEY=your_key_here")
            return False

        # Run integration tests
        cmd = base_cmd + ["tests/integration/", "-m", "integration"]
        success = run_command(cmd, "Integration Tests")

    elif args.test_type == "e2e":
        # Check for API key
        if not os.getenv("OPENAI_API_KEY"):
            print("❌ OPENAI_API_KEY not found. E2E tests require a real API key.")
            print("   Set your API key: export OPENAI_API_KEY=your_key_here")
            return False

        # Run E2E tests
        cmd = base_cmd + ["tests/integration/", "-m", "e2e"]
        success = run_command(cmd, "End-to-End Tests")

    elif args.test_type == "all":
        # Run all tests
        cmd = base_cmd + ["tests/"]
        success = run_command(cmd, "All Tests")

    elif args.test_type == "fast":
        # Run only fast tests (unit tests)
        cmd = base_cmd + ["tests/", "-m", "not slow and not expensive"]
        success = run_command(cmd, "Fast Tests")

    if success:
        print(f"\n🎉 {args.test_type.title()} tests completed successfully!")
    else:
        print(f"\n💥 {args.test_type.title()} tests failed!")
        sys.exit(1)


if __name__ == "__main__":
    main()
