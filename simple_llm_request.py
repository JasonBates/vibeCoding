"""Simple one-off LLM call using the official OpenAI Python client.

Setup steps when running from the repo root:
  1. source .venv/bin/activate
  2. Create a `.env` file (or export manually) with `OPENAI_API_KEY=sk-...`
  3. python simple_llm_request.py
"""
from __future__ import annotations

import sys

import haiku_service


def main() -> int:
    """Fetch a two-paragraph English poem from a GPT-4.1 model and print it."""
    # Get subject from user input or use default
    subject = (
        input("Enter a subject for the poem: ").strip()
        or haiku_service.DEFAULT_SUBJECT
    )

    try:
        client = haiku_service.get_client()
        response_text = haiku_service.generate_haiku(client, subject)

        print("\nGenerated poem:\n")
        print(response_text)

    except haiku_service.MissingAPIKeyError as exc:
        print(f"Error: {exc}")
        print("Please set your OPENAI_API_KEY environment variable.")
        return 1
    except Exception as exc:
        print(f"Unexpected error: {exc}")
        return 1

    return 0


if __name__ == "__main__":
    sys.exit(main())
