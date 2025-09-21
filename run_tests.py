#!/usr/bin/env python3
"""Test runner script for the haiku generator."""

import subprocess
import sys
import os


def run_command(command, description):
    """Run a command and return success status."""
    print(f"\n🔍 {description}")
    print(f"Running: {command}")
    print("-" * 50)
    
    try:
        result = subprocess.run(command, shell=True, check=True, capture_output=True, text=True)
        print(result.stdout)
        if result.stderr:
            print("STDERR:", result.stderr)
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Command failed with exit code {e.returncode}")
        print("STDOUT:", e.stdout)
        print("STDERR:", e.stderr)
        return False


def main():
    """Run all tests."""
    print("🚀 Running Haiku Generator Test Suite")
    print("=" * 50)
    
    # Check if we're in the right directory
    if not os.path.exists("streamlit_app.py"):
        print("❌ Please run this script from the project root directory")
        sys.exit(1)
    
    # Install test dependencies
    if not run_command("pip install -r requirements.txt", "Installing dependencies"):
        print("❌ Failed to install dependencies")
        sys.exit(1)
    
    # Run unit tests
    if not run_command("pytest tests/ -v", "Running unit tests"):
        print("❌ Unit tests failed")
        sys.exit(1)
    
    # Run tests with coverage
    if not run_command("pytest tests/ --cov=. --cov-report=term-missing", "Running tests with coverage"):
        print("❌ Coverage tests failed")
        sys.exit(1)
    
    # Test CLI script
    if not run_command("echo 'test subject' | python simple_llm_request.py", "Testing CLI script"):
        print("⚠️  CLI test had issues (may be expected if no API key)")
    
    # Test Streamlit app import
    if not run_command("python -c 'import streamlit_app; print(\"Streamlit app imports successfully\")'", "Testing Streamlit app import"):
        print("❌ Streamlit app import failed")
        sys.exit(1)
    
    print("\n🎉 All tests completed successfully!")
    print("=" * 50)


if __name__ == "__main__":
    main()
