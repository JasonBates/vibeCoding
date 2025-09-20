"""Streamlit UI for generating poems with the OpenAI Responses API."""
from __future__ import annotations

import os
import html

import streamlit as st
import streamlit.components.v1 as components
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


def _poem_lines(poem: str) -> list[str]:
    """Return poem segments split on pipes with whitespace trimmed."""
    lines = [segment.strip() for segment in poem.split("|")]
    cleaned_lines = [line for line in lines if line]
    return cleaned_lines or [poem]


def main() -> None:
    st.set_page_config(page_title="LLM Poem Generator", page_icon="📝")
    st.title("LLM Haiku Generator")
    st.write(
        "Generate an English haiku (5-7-5) that mentions pipes using OpenAI's official Python client."
    )
    st.caption("Type a subject and press Enter to generate the haiku.")

    default_subject = "quiet mornings"
    if "subject_input" not in st.session_state:
        st.session_state["subject_input"] = default_subject

    with st.form("haiku_form", clear_on_submit=False):
        subject = st.text_input(
            "Subject",
            help="What should the poem be about?",
            key="subject_input",
        ).strip()
        submitted = st.form_submit_button("Generate Haiku")

    # Focus the subject input each run so users can type immediately.
    components.html(
        """
        <script>
        const doc = window.parent.document;
        const input = doc.querySelector('input[data-testid="stTextInput"][aria-label="Subject"]');
        if (input) {
            input.focus();
        }
        </script>
        """,
        height=0,
    )

    if submitted:
        if not subject:
            st.session_state.pop("generated_poem", None)
            st.warning("Please enter a subject for the poem.")
            return

        client = get_client()
        with st.spinner("Summoning gentle verses..."):
            try:
                poem = generate_poem(client, subject)
            except Exception as exc:  # noqa: BLE001 - surface any API/runtime errors
                st.error(f"Failed to generate poem: {exc}")
                return

        st.session_state["generated_poem"] = poem

    poem_to_show = st.session_state.get("generated_poem")
    if poem_to_show:
        lines_markup = "".join(
            f"<p style='font-size:1.6rem; margin:0.25rem 0;'>{html.escape(line)}</p>"
            for line in _poem_lines(poem_to_show)
        )
        st.markdown(f"<div style='margin-top:1rem;'>{lines_markup}</div>", unsafe_allow_html=True)


if __name__ == "__main__":
    main()
