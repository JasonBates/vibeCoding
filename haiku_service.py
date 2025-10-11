"""Shared helpers for generating two-paragraph poems with the OpenAI Chat Completions API."""
from __future__ import annotations

import os

from dotenv import load_dotenv
from openai import OpenAI

DEFAULT_SUBJECT = "quiet mornings"
MODEL_NAME = "gpt-4o-mini"
PROMPT_TEMPLATE = (
    "Write an English poem in two distinct paragraphs about the following "
    "subject: {subject}. Each paragraph should contain exactly three "
    "sentences and feel vivid yet concise. Return the poem as exactly two "
    "paragraphs separated by a single blank line."
)


class MissingAPIKeyError(RuntimeError):
    """Raised when the OpenAI API key is not configured."""


def load_api_key() -> str:
    """Load the OpenAI API key from the environment or raise an error."""
    load_dotenv()
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise MissingAPIKeyError(
            "OPENAI_API_KEY not set; add it to .env or export it before "
            "running this script."
        )
    return api_key


def get_client(api_key: str | None = None) -> OpenAI:
    """Create an OpenAI client using the configured API key."""
    if not api_key:
        api_key = load_api_key()
    return OpenAI(api_key=api_key)


def build_prompt(subject: str) -> str:
    """Return the poem prompt for the given subject."""
    return PROMPT_TEMPLATE.format(subject=subject)


def generate_haiku(client: OpenAI, subject: str) -> str:
    """Request a two-paragraph poem for the subject using the provided client."""
    prompt = build_prompt(subject)
    response = client.chat.completions.create(
        model=MODEL_NAME,
        messages=[{"role": "user", "content": prompt}],
        max_tokens=150,
        temperature=0.7,
    )
    return response.choices[0].message.content
