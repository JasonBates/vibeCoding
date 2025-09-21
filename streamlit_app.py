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
            f"{subject}. "
            "Return the haiku as three lines, each line on its own line."
        ),
    )
    return response.output_text


def _poem_lines(poem: str) -> list[str]:
    """Return poem lines split on newlines with whitespace trimmed."""
    lines = [line.strip() for line in poem.splitlines()]
    cleaned_lines = [line for line in lines if line]
    return cleaned_lines or [poem]


def main() -> None:
    st.set_page_config(page_title="LLM Poem Generator", page_icon="📝")
    st.markdown(
        """
        <style>
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700&family=Playfair+Display:wght@500;600&display=swap');

        .stApp {
            background: radial-gradient(circle at top left, #fdf2ff 0%, #f6f9ff 40%, #dbeafe 100%);
            font-family: 'Inter', sans-serif;
            color: #0f172a;
        }

        .stApp header { visibility: hidden; }

        .block-container {
            padding-top: 4rem;
            padding-bottom: 4rem;
            max-width: 760px;
        }

        .hero-text {
            text-align: center;
            margin-bottom: 2.5rem;
        }

        .hero-text h1 {
            font-family: 'Playfair Display', serif;
            font-size: 3rem;
            margin-bottom: 0.65rem;
            color: #0f172a;
        }

        .hero-text p {
            font-size: 1.1rem;
            color: #334155;
        }

        .hero-text .accent {
            color: #6366f1;
            font-weight: 600;
        }

        div[data-testid="stForm"] {
            background: rgba(255, 255, 255, 0.78);
            border-radius: 26px;
            padding: 2.5rem 2.75rem;
            box-shadow: 0 35px 60px rgba(15, 23, 42, 0.18);
            border: 1px solid rgba(255, 255, 255, 0.6);
            backdrop-filter: blur(18px);
        }

        div[data-testid="stForm"] label {
            font-weight: 600;
            font-size: 0.95rem;
            color: #1f2937;
            margin-bottom: 0.4rem;
        }

        div[data-testid="stTextInput"] input {
            border-radius: 14px;
            border: 1px solid rgba(148, 163, 184, 0.4);
            background: rgba(255, 255, 255, 0.9);
            padding: 0.8rem 1rem;
            box-shadow: inset 0 2px 8px rgba(15, 23, 42, 0.05);
            font-size: 1rem;
        }

        div[data-testid="stFormSubmitButton"] button {
            background: linear-gradient(135deg, #6366f1, #8b5cf6);
            color: #fff;
            border: none;
            border-radius: 999px;
            padding: 0.85rem 2.6rem;
            font-weight: 600;
            letter-spacing: 0.02em;
            box-shadow: 0 18px 35px rgba(99, 102, 241, 0.35);
            transition: transform 160ms ease, box-shadow 160ms ease;
        }

        div[data-testid="stFormSubmitButton"] button:hover {
            transform: translateY(-1px);
            box-shadow: 0 22px 40px rgba(99, 102, 241, 0.45);
        }

        div[data-testid="stFormSubmitButton"] button:focus {
            outline: none;
        }

        .haiku-display {
            margin-top: 2.8rem;
            padding: 2.2rem;
            border-radius: 26px;
            background: rgba(15, 23, 42, 0.8);
            color: #f8fafc;
            box-shadow: 0 40px 70px rgba(15, 23, 42, 0.35);
            border: 1px solid rgba(148, 163, 184, 0.35);
            backdrop-filter: blur(14px);
        }

        .haiku-display p {
            font-family: 'Playfair Display', serif;
            font-size: 1.85rem;
            line-height: 1.35;
            letter-spacing: 0.02em;
            margin: 0.35rem 0;
        }

        .stAlert {
            border-radius: 18px;
        }
        </style>
        """,
        unsafe_allow_html=True,
    )

    st.markdown(
        """
        <div class="hero-text">
            <h1>LLM Haiku Generator</h1>
            <p>Summon bespoke 5-7-5 verses that whisper about <span class="accent">pipes</span>.</p>
            <p>Type a subject, press Enter, and enjoy a refined haiku in seconds.</p>
        </div>
        """,
        unsafe_allow_html=True,
    )

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
        const focusSubject = () => {
            const doc = window.parent.document;
            const inputs = doc.querySelectorAll('input[type="text"]');
            for (const input of inputs) {
                const label = (input.getAttribute('aria-label') || '').trim().toLowerCase();
                if (label === 'subject') {
                    input.focus();
                    input.select();
                    return;
                }
            }
        };

        // Allow Streamlit DOM updates to settle before focusing.
        window.setTimeout(focusSubject, 100);
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
            f"<p>{html.escape(line)}</p>" for line in _poem_lines(poem_to_show)
        )
        st.markdown(
            f"<div class='haiku-display'>{lines_markup}</div>",
            unsafe_allow_html=True,
        )


if __name__ == "__main__":
    main()
