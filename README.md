# Simple LLM Request

A simple Python script that generates Japanese-style poems using OpenAI's GPT-4o-mini model.

## Features

- Interactive prompt for poem subject
- Generates 5-line Japanese-style poems
- Uses OpenAI's official Python client
- Environment variable configuration

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
   pip install openai python-dotenv
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

Run the script:
```bash
python simple_llm_request.py
```

Enter a subject when prompted, and the script will generate a 5-line Japanese-style poem about that subject.

## Requirements

- Python 3.7+
- OpenAI API key
- openai
- python-dotenv

## Example

```
Enter a subject for the poem: cherry blossoms

Generated poem:

Pink petals dance on spring breeze,
Soft whispers in morning light,
Fleeting beauty graces the trees,
Nature's canvas pure and bright,
Cherry dreams bloom in the night.
```
