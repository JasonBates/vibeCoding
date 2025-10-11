#!/usr/bin/env python3
"""
CI Test Runner for GitHub Actions.

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
    """Check which credentials are available and valid."""
    # Load environment variables from .env file
    from dotenv import load_dotenv

    load_dotenv()

    openai_key = os.getenv("OPENAI_API_KEY")
    supabase_url = os.getenv("SUPABASE_URL")
    supabase_key = os.getenv("SUPABASE_KEY")

    # Check OpenAI credentials
    openai_valid = bool(openai_key and openai_key != "test-key-for-mocking")

    # Check Supabase credentials and test connection
    supabase_valid = False
    if supabase_url and supabase_key:
        try:
            # Add current directory to Python path for imports
            import sys
            from pathlib import Path

            # Debug: Print current working directory and Python path
            print(f"🔍 Current working directory: {os.getcwd()}")
            print(f"🔍 Script location: {Path(__file__).parent.parent}")

            # Add multiple possible paths
            project_root = Path(__file__).parent.parent
            sys.path.insert(0, str(project_root))
            sys.path.insert(0, str(project_root.absolute()))

            # Try importing with different approaches
            try:
                from haiku_storage_service import HaikuStorageService
            except ImportError as ie:
                print(f"🔍 Import error: {ie}")
                print(f"🔍 Python path: {sys.path[:3]}")
                # Try alternative import
                import importlib.util

                spec = importlib.util.spec_from_file_location(
                    "haiku_storage_service", project_root / "haiku_storage_service.py"
                )
                if spec and spec.loader:
                    haiku_module = importlib.util.module_from_spec(spec)
                    spec.loader.exec_module(haiku_module)
                    HaikuStorageService = haiku_module.HaikuStorageService
                else:
                    raise ie

            print(f"🔍 Testing Supabase connection with URL: {supabase_url[:20]}...")
            print(f"🔍 Key starts with: {supabase_key[:10]}...")
            service = HaikuStorageService(supabase_url, supabase_key)
            supabase_valid = service.is_available()
            print(f"🔍 Supabase available: {supabase_valid}")
        except Exception as e:
            print(f"🔍 Supabase connection failed: {e}")
            print(f"🔍 Exception type: {type(e).__name__}")
            import traceback

            print(f"🔍 Traceback: {traceback.format_exc()}")
            supabase_valid = False

    return {
        "openai": openai_valid,
        "supabase": supabase_valid,
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

    # Build comprehensive test command (run all tests once with coverage)
    print("\n🧪 Running All Tests with Coverage")
    print("=" * 60)

    # Start with base pytest command
    test_cmd = [
        "pytest",
        "--cov=.",
        "--cov-report=term-missing",
        "--cov-report=xml",
        "--cov-fail-under=60",
        "-v",
        "--tb=short",
    ]

    # Add unit tests (always included)
    unit_tests = [
        "tests/test_cli.py",
        "tests/test_streamlit_app.py",
        "tests/test_haiku_validation.py",
        "tests/test_integration.py",
        "tests/test_repository.py",
        "tests/test_haiku_storage_service.py",
    ]
    test_cmd.extend(unit_tests)
    print("✅ Including Unit Tests")

    # Add integration tests based on available credentials
    if creds["openai"]:
        print("✅ Including OpenAI Integration Tests")
        test_cmd.extend(
            [
                "tests/integration/test_openai_api.py",
                "tests/integration/test_e2e_haiku.py",
            ]
        )
    else:
        print("⚠️  Skipping OpenAI Integration Tests (no valid API key)")

    if creds["supabase"]:
        print("✅ Including Supabase Integration Tests")
        test_cmd.append("tests/integration/test_supabase_integration.py")
    else:
        print("❌ Supabase Integration Tests - FAILED (no valid credentials)")
        print("   Set SUPABASE_URL and SUPABASE_KEY environment variables")
        all_passed = False

    # Run all tests once with coverage
    if all_passed:
        if not run_command(test_cmd, "All Tests with Coverage"):
            all_passed = False
    else:
        print("❌ Skipping test run due to missing Supabase credentials")

    # Check Supabase credentials and provide helpful error message
    if not creds["supabase"]:
        print("❌ Supabase integration tests require valid credentials")
        print("   Set SUPABASE_URL and SUPABASE_KEY environment variables")
        print("   In GitHub Actions, add these as repository secrets")
        print("   In local development, add them to .env file")

        # In CI, we should fail. In local dev, we might want to be more lenient
        if os.getenv("GITHUB_ACTIONS"):
            print("   This is running in GitHub Actions - failing build")
            all_passed = False
        else:
            print("   This is local development - you can continue without Supabase")
            print("   But integration tests will be skipped")
            all_passed = False  # Still fail to encourage proper setup

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
