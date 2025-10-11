#!/usr/bin/env python3.
"""
CI Test Runner for GitHub Actions

This script runs the appropriate tests based on available credentials and environment.
It's designed to be used in GitHub Actions workflows and can also be run locally.
"""

import os
import subprocess
import sys
from pathlib import Path


def run_command(cmd, description):
    """Run a command and return success status."""
    print(f"\n🔧 {description}")
    print("Running: " + " ".join(cmd))
    print("-" * 60)

    try:
        result = subprocess.run(cmd, check=True, capture_output=False)
        print(f"✅ {description} - PASSED")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ {description} - FAILED (exit code: {e.returncode})")
        return False


def check_credentials():
    """Check which credentials are available."""
    openai_key = os.getenv("OPENAI_API_KEY")
    supabase_url = os.getenv("SUPABASE_URL")
    supabase_key = os.getenv("SUPABASE_KEY")

    return {
        "openai": bool(openai_key and openai_key != "test-key-for-mocking"),
        "supabase": bool(supabase_url and supabase_key),
    }


def main():
    """Main test runner function."""
    print("🧪 CI Test Runner")
    print("=" * 60)

    # Check available credentials
    creds = check_credentials()
    print("📋 Available credentials:")
    print(f"   OpenAI: {'✅' if creds['openai'] else '❌'}")
    print(f"   Supabase: {'✅' if creds['supabase'] else '❌'}")

    # Set up environment
    os.environ.setdefault("PYTHONPATH", str(Path(__file__).parent))

    # Track overall success
    all_passed = True

    # 1. Run unit tests (always run these)
    print("\n📦 Running Unit Tests")
    print("=" * 60)

    unit_tests = [
        "tests/test_cli.py",
        "tests/test_streamlit_app.py",
        "tests/test_haiku_validation.py",
        "tests/test_integration.py",
        "tests/test_repository.py",
        "tests/test_haiku_storage_service.py",
    ]

    unit_cmd = ["pytest"] + unit_tests + ["-v", "--tb=short"]
    if not run_command(unit_cmd, "Unit Tests"):
        all_passed = False

    # 2. Run OpenAI integration tests (if credentials available)
    if creds["openai"]:
        print("\n🤖 Running OpenAI Integration Tests")
        print("=" * 60)

        openai_tests = [
            "tests/integration/test_openai_api.py",
            "tests/integration/test_e2e_haiku.py",
        ]

        openai_cmd = ["pytest"] + openai_tests + ["-v", "--tb=short"]
        if not run_command(openai_cmd, "OpenAI Integration Tests"):
            all_passed = False
    else:
        print("\n⚠️  Skipping OpenAI Integration Tests (no valid API key)")

    # 3. Run Supabase integration tests (if credentials available)
    if creds["supabase"]:
        print("\n🗄️  Running Supabase Integration Tests")
        print("=" * 60)

        supabase_cmd = [
            "pytest",
            "tests/integration/test_supabase_integration.py",
            "-v",
            "--tb=short",
        ]
        if not run_command(supabase_cmd, "Supabase Integration Tests"):
            all_passed = False
    else:
        print("\n⚠️  Skipping Supabase Integration Tests (no credentials)")

    # 4. Run coverage report (if all tests passed)
    if all_passed:
        print("\n📊 Running Coverage Report")
        print("=" * 60)

        coverage_cmd = [
            "pytest",
            "--cov=.",
            "--cov-report=term-missing",
            "--cov-report=xml",
            "--cov-fail-under=60",  # Lower threshold for unit tests only
        ] + unit_tests

        if creds["openai"]:
            coverage_cmd.extend(
                [
                    "tests/integration/test_openai_api.py",
                    "tests/integration/test_e2e_haiku.py",
                ]
            )

        if creds["supabase"]:
            coverage_cmd.append("tests/integration/test_supabase_integration.py")

        run_command(coverage_cmd, "Coverage Report")

    # Final result
    print("\n🎯 Test Results Summary")
    print("=" * 60)

    if all_passed:
        print("✅ All tests passed successfully!")
        sys.exit(0)
    else:
        print("❌ Some tests failed. Check the output above for details.")
        sys.exit(1)


if __name__ == "__main__":
    main()
