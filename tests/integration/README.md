# Integration Tests

This directory contains integration tests that test the haiku generator with real external services (like OpenAI).

## ⚠️ Important Notes

- **These tests cost money** - they make real API calls to OpenAI
- **These tests are slow** - they depend on external network services
- **These tests may fail** - they depend on external services being available

## 🚀 Running Integration Tests

### Prerequisites

1. Set your OpenAI API key:
   ```bash
   export OPENAI_API_KEY=your_api_key_here
   ```

2. Make sure you have the required dependencies:
   ```bash
   pip install -r requirements.txt
   ```

### Running Tests

#### Option 1: Using the test runner script
```bash
# Run integration tests
python run_tests.py integration

# Run E2E tests
python run_tests.py e2e

# Run with coverage
python run_tests.py integration --coverage
```

#### Option 2: Using pytest directly
```bash
# Run all integration tests
pytest tests/integration/ -v

# Run only OpenAI API tests
pytest tests/integration/test_openai_api.py -v

# Run only E2E tests
pytest tests/integration/ -m e2e -v

# Run with coverage
pytest tests/integration/ -v --cov=. --cov-report=html
```

#### Option 3: Run specific test classes
```bash
# Test OpenAI API integration
pytest tests/integration/test_openai_api.py::TestOpenAIIntegration -v

# Test E2E workflow
pytest tests/integration/test_e2e_haiku.py::TestEndToEndHaiku -v
```

## 📁 Test Files

- `test_openai_api.py` - Tests direct integration with OpenAI API
- `test_e2e_haiku.py` - Tests complete end-to-end workflows

## 🏷️ Test Markers

Tests are marked with pytest markers for easy filtering:

- `@pytest.mark.integration` - Integration tests
- `@pytest.mark.e2e` - End-to-end tests
- `@pytest.mark.slow` - Slow tests
- `@pytest.mark.expensive` - Expensive tests (cost money)

## 🔧 GitHub Actions

Integration tests are available via a manual workflow (`workflow_dispatch`). The main test workflow already runs the full suite using a unified runner; use the manual integration workflow only when you specifically need to validate integrations independently.

**Note:** Integration tests only run if the appropriate secrets are available (e.g., `OPENAI_API_KEY`, `SUPABASE_URL`, `SUPABASE_KEY`).

## 💡 Best Practices

1. **Run locally first** - Test integration changes locally before pushing
2. **Use specific test selection** - Don't run all integration tests unless necessary
3. **Monitor costs** - Integration tests make real API calls
4. **Check network** - Ensure stable internet connection
5. **Handle failures gracefully** - Integration tests may fail due to external factors

## 🐛 Troubleshooting

### "No OPENAI_API_KEY found"
- Set your API key: `export OPENAI_API_KEY=your_key_here`
- Check that the key is valid and has sufficient credits

### "Connection timeout" or "API error"
- Check your internet connection
- Verify OpenAI API status
- Check if you've hit rate limits

### "Import errors"
- Make sure you're in the project root directory
- Activate your virtual environment: `source .venv/bin/activate`
- Install dependencies: `pip install -r requirements.txt`
