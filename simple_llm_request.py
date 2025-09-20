"""Simple one-off LLM call using the official OpenAI Python client.

Setup steps when running from the repo root:
  1. source .venv/bin/activate
  2. Create a `.env` file (or export manually) with `OPENAI_API_KEY=sk-...`
  3. python simple_llm_request.py
"""
from __future__ import annotations

import os

from dotenv import load_dotenv
from openai import OpenAI


def main() -> None:
    """Fetch a short reply from a GPT-4.1 model and print the text."""
    load_dotenv()

    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise RuntimeError(
            "OPENAI_API_KEY not set; add it to .env or export it before running this script."
        )

    subject = input(
        "Enter a subject for the poem: ").strip() or "quiet mornings"
    prompt = (
        "Write a five-line Japanese-style poem about the following subject: "
        f"{subject}. Keep it vivid, gentle, and evocative."
    )

    client = OpenAI(api_key=api_key)

    response = client.responses.create(
        model="gpt-4.1-mini",
        input=prompt,
    )

    print("\nGenerated poem:\n")
    print(response.output_text)


if __name__ == "__main__":
    main()
