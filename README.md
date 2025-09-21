# VibeCoding - LLM Haiku Generator

A beautiful Python application that generates traditional English haikus using OpenAI's GPT-4.1-mini model. Features both a command-line interface and a modern Streamlit web UI with elegant styling.

## Features

- **🎨 Beautiful Streamlit UI**: Modern, responsive web interface with gradient backgrounds and custom typography
- **📝 Traditional Haiku Generation**: Creates authentic 5-7-5 syllable English haikus
- **⚡ Real-time Generation**: Instant poem creation with loading animations
- **🖥️ Dual Interface**: Both command-line and web-based interfaces
- **🔧 Easy Setup**: Simple configuration with environment variables
- **📱 Responsive Design**: Works perfectly on desktop and mobile devices

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

This project includes a comprehensive testing suite with both unit tests and integration tests.

### Test Types

- **Unit Tests**: Fast, isolated tests that verify code logic without external dependencies
- **Integration Tests**: Real API tests that call OpenAI and generate actual haikus (costs money)
- **End-to-End Tests**: Complete workflow tests from input to output

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

## 🤝 Contributing

Feel free to submit issues and enhancement requests! This project is open to contributions.

## 📄 License

This project is open source and available under the [MIT License](LICENSE).
