# GitHub Actions Test Configuration Update

## Overview

Updated GitHub Actions workflows to include comprehensive testing for the new Supabase haiku storage integration, with proper pre-commit hooks and credential management.

## 🚀 New Workflow Structure

### 1. Pre-commit Workflow (`.github/workflows/pre-commit.yml`)
- **Triggers**: Every push and pull request
- **Purpose**: Code quality and basic testing
- **Features**:
  - Runs pre-commit hooks (linting, formatting, etc.)
  - Executes unit tests with CI test runner
  - Ensures code quality before merge

### 2. Main Test Workflow (`.github/workflows/test.yml`)
- **Triggers**: Push to main/develop, pull requests to main
- **Purpose**: Comprehensive testing with current Python version
- **Features**:
  - Tests with Python 3.12 (current version)
  - Uses unified CI test runner
  - Handles both OpenAI and Supabase credentials
  - Uploads coverage to Codecov

### 3. Integration Test Workflow (`.github/workflows/integration.yml`)
- **Triggers**: Manual, changes to integration tests, main branch
- **Purpose**: Full integration testing with real APIs
- **Features**:
  - Tests with real OpenAI API (if credentials available)
  - Tests with real Supabase database (if credentials available)
  - Comprehensive integration test suite

## 🔧 New CI Test Runner (`run_ci_tests.py`)

### Features
- **Smart Credential Detection**: Automatically detects available API keys
- **Conditional Testing**: Runs appropriate tests based on available credentials
- **Unified Interface**: Single script for all test scenarios
- **Comprehensive Reporting**: Clear success/failure reporting
- **Coverage Integration**: Generates coverage reports with appropriate thresholds

## 🐍 Python Version Strategy

### Current Approach
- **Single Version Testing**: Uses Python 3.12 (current stable version)
- **Faster CI**: Eliminates matrix strategy for quicker feedback
- **Focused Testing**: Concentrates on the version you're actively using
- **Easier Maintenance**: Simpler workflow configuration

### Benefits
- **Faster Execution**: No need to test across multiple Python versions
- **Reduced Complexity**: Simpler workflow configuration
- **Focused Development**: Tests the version you're actually using
- **Lower Resource Usage**: Less GitHub Actions minutes consumed

### Usage
```bash
# Run locally
python run_ci_tests.py

# In GitHub Actions
python run_ci_tests.py
```

### Test Categories
1. **Unit Tests** (always run):
   - CLI functionality
   - Streamlit app components
   - Haiku validation
   - Repository layer
   - Service layer
   - Integration utilities

2. **OpenAI Integration Tests** (if API key available):
   - Real API calls
   - End-to-end workflows
   - Error handling

3. **Supabase Integration Tests** (if credentials available):
   - Database operations
   - Real data persistence
   - Search functionality

## 🔐 Credential Management

### Required Secrets
Add these to GitHub repository secrets:

1. **OPENAI_API_KEY**: Your OpenAI API key
2. **SUPABASE_URL**: Your Supabase project URL
3. **SUPABASE_KEY**: Your Supabase anon key

### How to Add Secrets
1. Go to repository Settings
2. Navigate to "Secrets and variables" → "Actions"
3. Click "New repository secret"
4. Add each secret with appropriate values

### Graceful Degradation
- Tests run with mock credentials when real ones aren't available
- Clear messaging about missing credentials
- No blocking failures for missing optional credentials

## 📊 Test Coverage

### Coverage Thresholds
- **Unit Tests Only**: 60% minimum coverage
- **With Integration Tests**: 80% minimum coverage
- **Coverage Reports**: Generated in XML and HTML formats

### Coverage Tracking
- Uploaded to Codecov for tracking
- Separate flags for different test types
- Historical coverage tracking

## 🎯 Pre-commit Integration

### Updated `.pre-commit-config.yaml`
- Added pytest unit tests to pre-commit hooks
- Runs tests on every commit attempt
- Ensures code quality before commits

### Pre-commit Hook Features
- **Code Formatting**: Black, isort
- **Linting**: Flake8 with docstring checks
- **Testing**: Unit tests execution
- **Quality Checks**: Trailing whitespace, large files, etc.

## 🔄 Workflow Dependencies

### Execution Order
1. **Pre-commit** runs first on every push/PR
2. **Main Test** runs after pre-commit passes
3. **Integration** runs manually or on specific triggers

### Failure Handling
- Pre-commit failures block commits
- Test failures provide detailed error messages
- Integration test failures don't block main workflow

## 📈 Benefits

### For Developers
- **Fast Feedback**: Pre-commit hooks catch issues early
- **Consistent Testing**: Same test runner everywhere
- **Clear Reporting**: Easy to understand test results
- **Flexible Credentials**: Works with or without API keys

### For CI/CD
- **Reliable Testing**: Comprehensive test coverage
- **Efficient Execution**: Only runs necessary tests
- **Clear Status**: Easy to see what's working/failing
- **Scalable**: Easy to add new test categories

## 🚀 Usage Examples

### Local Development
```bash
# Install pre-commit hooks
pre-commit install

# Run tests manually
python run_ci_tests.py

# Run specific test categories
pytest tests/test_repository.py -v
```

### GitHub Actions
- Workflows run automatically on push/PR
- Manual integration tests available
- Clear status checks in PR interface

## 🔧 Maintenance

### Adding New Tests
1. Add test files to appropriate directories
2. Update `run_ci_tests.py` if needed
3. Tests will automatically run in CI

### Updating Credentials
1. Update repository secrets
2. Re-run workflows to test
3. No code changes needed

### Monitoring
- Check Actions tab for workflow status
- Review coverage reports in Codecov
- Monitor test execution times

## 📝 Summary

The updated GitHub Actions configuration provides:
- ✅ Comprehensive testing for Supabase integration
- ✅ Pre-commit hooks for code quality
- ✅ Smart credential management
- ✅ Unified test runner
- ✅ Clear reporting and status checks
- ✅ Graceful degradation without credentials
- ✅ Easy maintenance and extension

This setup ensures high code quality and reliable testing while being flexible enough to work in different environments and credential configurations.
