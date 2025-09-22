"""Shared helpers for generating haikus with the OpenAI Responses API."""
from __future__ import annotations

import os

from dotenv import load_dotenv
from openai import OpenAI

DEFAULT_SUBJECT = "quiet mornings"
MODEL_NAME = "gpt-4.1-mini"
PROMPT_TEMPLATE = (
    "Write an English haiku (three lines, 5-7-5 syllable pattern) "
    "about the following subject: {subject}. "
    "Return the haiku as three lines, each line on its own line."
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
    """Return the haiku prompt for the given subject."""
    return PROMPT_TEMPLATE.format(subject=subject)


def generate_haiku(client: OpenAI, subject: str) -> str:
    """Request a haiku for the subject using the provided client."""
    prompt = build_prompt(subject)
    response = client.responses.create(model=MODEL_NAME, input=prompt)
    return response.output_text
