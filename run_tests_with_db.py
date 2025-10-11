#!/usr/bin/env python3
"""
Test runner script that loads environment variables and runs all tests.

This ensures integration tests can access Supabase credentials.
"""

import os
import subprocess
import sys

from dotenv import load_dotenv


def main():
    """Run tests with proper environment variable loading."""
    print("🧪 Running tests with database integration...")
    print("=" * 60)

    # Load environment variables
    load_dotenv()

    # Check if Supabase credentials are available
    supabase_url = os.getenv("SUPABASE_URL")
    supabase_key = os.getenv("SUPABASE_KEY")

    if not supabase_url or not supabase_key:
        print("⚠️  Warning: Supabase credentials not found in .env")
        print("   Integration tests will be skipped")
        print("   Unit tests will still run")
    else:
        print("✅ Supabase credentials found - running all tests including integration")

    # Set environment variables for subprocess
    env = os.environ.copy()
    env["SUPABASE_URL"] = supabase_url or ""
    env["SUPABASE_KEY"] = supabase_key or ""

    # Run pytest with environment variables
    cmd = [sys.executable, "-m", "pytest", "tests/", "-v", "--tb=short"]

    try:
        result = subprocess.run(cmd, env=env, check=True)
        print("\n" + "=" * 60)
        print("🎉 All tests completed successfully!")
        return result.returncode
    except subprocess.CalledProcessError as e:
        print(f"\n❌ Tests failed with exit code {e.returncode}")
        return e.returncode


if __name__ == "__main__":
    sys.exit(main())
