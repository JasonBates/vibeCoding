# VibeCoding - Simple Haiku Generator

A basic "hello world" Python project that generates vivid two-paragraph poems using OpenAI's API. This is a learning project to explore LLM integration, not a serious application.

## 🧪 Testing Purpose

This project was created to test and learn about:
- **VibeCoding**: AI-powered coding assistance and pair programming
- **CLI:** Command-line AI interactions
- **Streamlit**: Streamlit application development and deployment
- **Test Suite**: Comprehensive testing with pytest, unit tests, and integration tests
- **GitHub Actions**: CI/CD workflows and automated testing
- **Version Control**: Git workflows, branching, and collaboration patterns

It serves as a practical example for understanding modern Python development practices and AI tooling.

## What This Is

This is a simple learning project that demonstrates:
- **Basic LLM Integration**: How to call OpenAI's API from Python
- **Simple Web UI**: A basic Streamlit interface for user interaction
- **Command Line Tool**: A simple CLI script for poem generation
- **Testing Examples**: Basic unit and integration test patterns
- **Project Structure**: How to organize a small Python project

**Note**: This is not production-ready code - it's just a fun way to learn about LLMs and Python development!

## Setup

1. **Clone the repository:**
   ```bash
   git clone https://github.com/JasonBates/vibeCoding.git
   cd vibeCoding
   ```

2. **Create and activate a virtual environment:**
   ```bash
   python -m venv .venv
   source .venv/bin/activate  # On Windows: .venv\Scripts\activate
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up environment variables:**
   Create a `.env` file in the project root:
   ```bash
   echo "OPENAI_API_KEY=your_api_key_here" > .env
   echo "SUPABASE_URL=your_supabase_project_url" >> .env
   echo "SUPABASE_KEY=your_supabase_anon_key" >> .env
   ```

   Or export the environment variables:
   ```bash
   export OPENAI_API_KEY=your_api_key_here
   export SUPABASE_URL=your_supabase_project_url
   export SUPABASE_KEY=your_supabase_anon_key
   ```

   **Note:** Supabase credentials are optional. The app will work without them, but poem history won't be saved.

### 🗄️ Supabase Setup (Optional)

To enable poem storage and history features:

1. **Create a Supabase account:**
   - Go to [supabase.com](https://supabase.com)
   - Sign up for a free account
   - Create a new project

2. **Set up the database:**
   - Go to the SQL Editor in your Supabase dashboard
   - Run this SQL to create the haikus table:
   ```sql
   CREATE TABLE haikus (
     id UUID DEFAULT gen_random_uuid() PRIMARY KEY,
     subject TEXT NOT NULL,
     haiku_text TEXT NOT NULL,
     created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
     user_id UUID
   );

   CREATE INDEX idx_haikus_created_at ON haikus(created_at DESC);
   CREATE INDEX idx_haikus_subject ON haikus(subject);
   ```

3. **Get your credentials:**
   - Go to Settings > API in your Supabase dashboard
   - Copy the Project URL and anon/public key
   - Add them to your `.env` file as shown above

## Usage

### 🌐 Streamlit Web UI (Recommended)

Start the beautiful web interface:

```bash
# Activate virtual environment
source .venv/bin/activate  # On Windows: .venv\Scripts\activate

# Launch the app
streamlit run streamlit_app.py
```

Then open your browser to `http://localhost:8501` and enjoy the modern interface!

**Features:**
- Elegant gradient background with glassmorphism design
- Auto-focus input field for immediate typing
- Real-time poem generation with loading animations
- Beautiful typography with custom fonts
- Responsive design that works on all devices
- **🗄️ Poem Library Sidebar** - Browse and search your generated poems
- **💾 Automatic Saving** - Haikus are automatically saved to Supabase
- **🔍 Search & Filter** - Find poems by subject with real-time search
- **🎨 Glassmorphism Design** - Consistent modern UI throughout
- **⚡ Real-time Updates** - Sidebar updates immediately after generation

### 💻 Command Line Interface

For a quick command-line experience:

```bash
python simple_llm_request.py
```

Enter a subject when prompted, and the script will generate a vivid two-paragraph poem about that subject.

## Requirements

- Python 3.8+
- OpenAI API key
- Supabase account (optional, for poem storage)
- openai>=1.0,<2.0
- python-dotenv>=1.0,<2.0
- streamlit>=1.36,<2.0
- supabase>=2.0,<3.0

## Examples

### Web UI Example
Visit `http://localhost:8501` and enter a subject like "coffee morning":

**Input:** `coffee morning`

**Output:**
```
Silent mind explored in hush of dawn. Dreams wander through lavender air. We breathe the promise of morning.

Moonlight drifts across the quiet lake. Memories ripple in silver whispers. We hold the night between our hands.
```

### Command Line Example
```bash
$ python simple_llm_request.py
Enter a subject for the poem: ocean waves

Generated poem:
Ocean waves inherit the hush of dawn. Silver foam sketches patient signatures. Sunlight drapes the tide in glass.

Saltwind teaches slow devotion. Cliffside cedars lean to listen. Evening gathers every gleam.
```

## 🚀 Quick Start

1. Clone and setup:
   ```bash
   git clone https://github.com/JasonBates/vibeCoding.git
   cd vibeCoding
   python -m venv .venv
   source .venv/bin/activate
   pip install -r requirements.txt
   ```

2. Add your OpenAI API key:
   ```bash
   echo "OPENAI_API_KEY=your_key_here" > .env
   ```

3. Launch the app:
   ```bash
   streamlit run streamlit_app.py
   ```

4. Open `http://localhost:8501` and start creating poems!

## 📸 Screenshots

The Streamlit app features:
- Beautiful gradient backgrounds
- Glassmorphism design elements
- Custom typography (Inter + Playfair Display)
- Smooth animations and transitions
- Mobile-responsive layout

## 🏗️ Architecture

This project demonstrates modern Python architecture patterns. For detailed architecture documentation, see [docs/ARCHITECTURE.md](docs/ARCHITECTURE.md).

### **Key Patterns**
- **Repository Pattern** - Clean data access layer (`repository.py`)
- **Service Layer** - Business logic encapsulation (`haiku_storage_service.py`)
- **Data Models** - Type-safe dataclasses (`models.py`)
- **Graceful Degradation** - Works with/without external services

### **Quick Overview**
- `repository.py` - Isolates database operations from business logic
- `haiku_storage_service.py` - Business logic and error handling
- `models.py` - Type-safe data structures with serialization
- App works with or without Supabase (automatic fallback)

## 🧪 Testing

This project includes comprehensive testing examples to learn about:

### Test Types

- **Unit Tests**: Mock external dependencies for fast, isolated testing
- **Integration Tests**: Test real Supabase database operations
- **End-to-End Tests**: Complete workflow tests from UI to database
- **Repository Tests**: Test data access layer with mocked Supabase client
- **Service Tests**: Test business logic with mocked dependencies

### Running Tests

#### Quick Start (Unit Tests Only)
```bash
# Run fast unit tests (recommended for development)
python run_tests.py unit

# Run with coverage
python run_tests.py unit --coverage
```

#### Database Integration Tests
```bash
# Run tests with Supabase integration
python scripts/run_tests_with_db.py

# Or run specific test categories
python -m pytest tests/test_repository.py -v
python -m pytest tests/integration/test_supabase_integration.py -v
```

#### All Tests
```bash
# Run everything (requires API keys)
python scripts/run_tests.py all

# Or use the CI test runner (recommended)
python scripts/run_ci_tests.py
```

### Test Structure

```
tests/
├── test_cli.py              # CLI functionality tests
├── test_streamlit_app.py    # Streamlit UI tests
├── test_haiku_validation.py # Haiku format validation tests
├── test_repository.py       # Database repository tests
├── test_haiku_storage_service.py # Service layer tests
├── test_integration.py      # General integration tests
├── integration/             # Real API and database tests
│   ├── test_openai_api.py   # OpenAI API integration tests
│   ├── test_e2e_haiku.py    # End-to-end workflow tests
│   ├── test_supabase_integration.py # Supabase database tests
│   └── README.md
└── conftest.py              # Pytest configuration
```

### GitHub Actions

- **Unit Tests**: Run automatically on every push
- **Integration Tests**: Run manually or when integration files change
- **Coverage**: Uploaded to Codecov for tracking

### Test Markers

- `@pytest.mark.unit` - Unit tests
- `@pytest.mark.integration` - Integration tests
- `@pytest.mark.e2e` - End-to-end tests
- `@pytest.mark.slow` - Slow tests
- `@pytest.mark.expensive` - Expensive tests (cost money)

## 🎓 Learning Goals

This project was created to learn about:
- OpenAI API integration
- Streamlit web development
- Python testing patterns
- Project organization
- Git and GitHub workflows

## 📚 Documentation

Comprehensive documentation is available in the [`docs/`](docs/) directory:

- **[Architecture Details](docs/ARCHITECTURE.md)** - Design patterns and implementation approaches
- **[Branch Review](docs/BRANCH_REVIEW.md)** - Feature implementation review
- **[GitHub Actions](docs/GITHUB_ACTIONS_UPDATE.md)** - CI/CD configuration and testing setup
- **[Documentation Index](docs/README.md)** - Complete documentation overview

## 🤝 Contributing

This is a learning project, but feel free to fork it and experiment! It's a good starting point for understanding LLM integration.

## 📄 License

This project is open source and available under the [MIT License](LICENSE).
