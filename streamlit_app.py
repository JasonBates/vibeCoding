"""Streamlit UI for generating poems with the OpenAI Responses API."""
from __future__ import annotations

import os

import streamlit as st
from dotenv import load_dotenv
from openai import OpenAI


def get_client() -> OpenAI:
    """Create an OpenAI client using the API key from the environment."""
    load_dotenv()
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        msg = "OPENAI_API_KEY not configured. Set it in .env or the environment."
        st.error(msg)
        st.stop()
    return OpenAI(api_key=api_key)


def generate_poem(client: OpenAI, subject: str) -> str:
    """Request a five-line poem about the given subject."""
    response = client.responses.create(
        model="gpt-4.1-mini",
        input=(
            "Write an English haiku (three lines, 5-7-5 syllable pattern) about the following subject: "
            f"{subject}. Use the word 'pipes' at least once. "
            "Return the haiku on a single line with each line separated by ' | '."
        ),
    )
    return response.output_text


def main() -> None:
    st.set_page_config(page_title="LLM Poem Generator", page_icon="📝")
    st.title("LLM Haiku Generator")
    st.write(
        "Generate an English haiku (5-7-5) that mentions pipes using OpenAI's official Python client."
    )

    default_subject = "quiet mornings"
    subject = st.text_input(
        "Subject", default_subject, help="What should the poem be about?"
    ).strip()

    if st.button("Generate Haiku"):
        if not subject:
            st.warning("Please enter a subject for the poem.")
            return

        client = get_client()
        with st.spinner("Summoning gentle verses..."):
            try:
                poem = generate_poem(client, subject)
            except Exception as exc:  # noqa: BLE001 - surface any API/runtime errors
                st.error(f"Failed to generate poem: {exc}")
                return

        st.subheader("Generated Haiku")
        st.code(poem, language="markdown")


if __name__ == "__main__":
    main()
