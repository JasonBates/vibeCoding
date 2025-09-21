# VibeCoding - Simple Haiku Generator

A basic "hello world" Python project that generates simple haikus using OpenAI's API. This is a learning project to explore LLM integration, not a serious application.

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
- **Command Line Tool**: A simple CLI script for haiku generation
- **Testing Examples**: Basic unit and integration test patterns
- **Project Structure**: How to organize a small Python project

**Note**: This is not production-ready code - it's just a fun way to learn about LLMs and Python development!

## Setup

1. **Clone the repository:**
   ```bash
   git clone <your-repo-url>
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
   ```
   
   Or export the environment variable:
   ```bash
   export OPENAI_API_KEY=your_api_key_here
   ```

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

### 💻 Command Line Interface

For a quick command-line experience:

```bash
python simple_llm_request.py
```

Enter a subject when prompted, and the script will generate a traditional English haiku about that subject.

## Requirements

- Python 3.8+
- OpenAI API key
- openai>=1.0,<2.0
- python-dotenv>=1.0,<2.0
- streamlit>=1.36,<2.0

## Examples

### Web UI Example
Visit `http://localhost:8501` and enter a subject like "coffee morning":

**Input:** `coffee morning`

**Output:**
```
Silent mind explored
Bound in trials of unknown
Truth in quiet waits
```

### Command Line Example
```bash
$ python simple_llm_request.py
Enter a subject for the poem: ocean waves

Generated haiku:
Ocean waves crash down
Against the ancient shoreline
Nature's endless song
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

4. Open `http://localhost:8501` and start creating haikus!

## 📸 Screenshots

The Streamlit app features:
- Beautiful gradient backgrounds
- Glassmorphism design elements
- Custom typography (Inter + Playfair Display)
- Smooth animations and transitions
- Mobile-responsive layout

## 🧪 Testing

This project includes basic testing examples to learn about:

### Test Types

- **Unit Tests**: Simple tests that mock external dependencies (good for learning)
- **Integration Tests**: Basic tests that call the real OpenAI API (costs money!)
- **End-to-End Tests**: Simple workflow tests from input to output

### Running Tests

#### Quick Start (Unit Tests Only)
```bash
# Run fast unit tests (recommended for development)
python run_tests.py unit

# Run with coverage
python run_tests.py unit --coverage
```

#### Integration Testing (Real OpenAI API)
```bash
# Set your API key
export OPENAI_API_KEY=your_api_key_here

# Run integration tests (calls real OpenAI API)
python run_tests.py integration

# Run end-to-end tests
python run_tests.py e2e
```

#### All Tests
```bash
# Run everything
python run_tests.py all
```

### Test Structure

```
tests/
├── unit/                    # Fast, isolated tests
│   ├── test_cli.py
│   ├── test_streamlit_app.py
│   └── test_haiku_validation.py
├── integration/             # Real API tests
│   ├── test_openai_api.py
│   ├── test_e2e_haiku.py
│   └── README.md
└── conftest.py
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

## 🤝 Contributing

This is a learning project, but feel free to fork it and experiment! It's a good starting point for understanding LLM integration.

## 📄 License

This project is open source and available under the [MIT License](LICENSE).
