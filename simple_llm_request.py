"""Simple one-off LLM call using the official OpenAI Python client.

Setup steps when running from the repo root:
  1. source .venv/bin/activate
  2. Create a `.env` file (or export manually) with `OPENAI_API_KEY=sk-...`
  3. python simple_llm_request.py
"""
from __future__ import annotations

import haiku_service


def main() -> None:
    """Fetch an English haiku from a GPT-4.1 model and print it."""
    # Get subject from user input or use default
    subject = (
        input("Enter a subject for the haiku: ").strip()
        or haiku_service.DEFAULT_SUBJECT
    )

    try:
        client = haiku_service.get_client()
    except haiku_service.MissingAPIKeyError as exc:  # Preserve existing CLI UX
        raise RuntimeError(str(exc)) from exc

    response_text = haiku_service.generate_haiku(client, subject)

    print("\nGenerated haiku:\n")
    print(response_text)


if __name__ == "__main__":
    main()
