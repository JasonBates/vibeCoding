"""Streamlit UI for generating poems with the OpenAI Chat Completions API."""
from __future__ import annotations

import html
import os
from datetime import datetime, timezone

import streamlit as st
import streamlit.components.v1 as components
from dotenv import load_dotenv
from openai import OpenAI

import haiku_service
from haiku_storage_service import HaikuStorageService
from models import Haiku

# Load environment variables
load_dotenv()


def get_client() -> OpenAI:
    """Create an OpenAI client and surface configuration issues in the UI."""
    try:
        return haiku_service.get_client()
    except haiku_service.MissingAPIKeyError as exc:
        st.error(str(exc))
        st.stop()


def get_storage_service() -> HaikuStorageService | None:
    """Create a haiku storage service if Supabase is configured."""
    supabase_url = os.getenv("SUPABASE_URL")
    supabase_key = os.getenv("SUPABASE_KEY")

    if not supabase_url or not supabase_key:
        return None

    try:
        return HaikuStorageService(supabase_url, supabase_key)
    except Exception:
        return None


def format_relative_time(dt: datetime) -> str:
    """Format datetime as relative time (e.g., '2 hours ago')."""
    now = datetime.now(timezone.utc)

    # Ensure both datetimes are timezone-aware
    if dt.tzinfo is None:
        dt = dt.replace(tzinfo=timezone.utc)

    diff = now - dt

    if diff.days > 0:
        return f"{diff.days} day{'s' if diff.days != 1 else ''} ago"
    elif diff.seconds > 3600:
        hours = diff.seconds // 3600
        return f"{hours} hour{'s' if hours != 1 else ''} ago"
    elif diff.seconds > 60:
        minutes = diff.seconds // 60
        return f"{minutes} minute{'s' if minutes != 1 else ''} ago"
    else:
        return "Just now"


def render_haiku_card(haiku: Haiku) -> None:
    """Render a haiku as a card in the sidebar."""
    with st.container():
        st.markdown(
            f"""
            <div class="haiku-card">
                <div class="haiku-subject">
                    {haiku.subject.upper()}
                </div>
                <div class="haiku-timestamp">
                    {format_relative_time(haiku.created_at)}
                </div>
                <div class="haiku-text">
                    {html.escape(haiku.haiku_text).replace(chr(10), '<br>')}
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )


def generate_poem(client: OpenAI, subject: str) -> str:
    """Request a haiku about the given subject."""
    return haiku_service.generate_haiku(client, subject)


def _poem_lines(poem: str) -> list[str]:
    """Return poem lines split on newlines with whitespace trimmed."""
    lines = [line.strip() for line in poem.splitlines()]
    cleaned_lines = [line for line in lines if line]
    return cleaned_lines or [poem]


def main() -> None:
    st.set_page_config(page_title="LLM Poem Generator", page_icon="📝", layout="wide")

    # Force light theme to maintain our custom design
    st.markdown(
        """
        <style>
        @import url("https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700&family=Playfair+Display:wght@500;600&display=swap");  # noqa: E501

        .stApp {
            background: radial-gradient(circle at top left, #fdf2ff 0%, #f6f9ff 40%, #dbeafe 100%);  # noqa: E501
            font-family: 'Inter', sans-serif;
            color: #0f172a;
        }


        .block-container {
            padding-top: 4rem;
            padding-bottom: 4rem;
            max-width: 760px;
        }

        .main-container {
            max-width: 760px;
        }

        /* Sidebar haiku card styling - more specific selectors */
        .stSidebar .haiku-card {
            background: rgba(255, 255, 255, 0.9) !important;
            border-radius: 12px !important;
            padding: 1rem !important;
            margin-bottom: 1rem !important;
            border: 1px solid rgba(99, 102, 241, 0.3) !important;
            box-shadow: 0 2px 8px rgba(0, 0, 0, 0.15) !important;
            transition: all 0.3s ease !important;
            display: block !important;
        }

        .stSidebar .haiku-card:hover {
            transform: translateY(-2px) !important;
            box-shadow: 0 4px 12px rgba(0, 0, 0, 0.2) !important;
            border-color: rgba(99, 102, 241, 0.5) !important;
        }

        .stSidebar .haiku-subject {
            font-size: 0.9rem !important;
            color: #6366f1 !important;
            margin-bottom: 0.3rem !important;
            font-weight: 700 !important;
            text-transform: uppercase !important;
            letter-spacing: 0.8px !important;
            display: block !important;
        }

        .stSidebar .haiku-timestamp {
            font-size: 0.75rem !important;
            color: #64748b !important;
            margin-bottom: 0.6rem !important;
            font-weight: 500 !important;
            display: block !important;
        }

        .stSidebar .haiku-text {
            font-family: 'Playfair Display', serif !important;
            font-size: 0.9rem !important;
            line-height: 1.4 !important;
            color: #1e293b !important;
            font-weight: 500 !important;
            display: block !important;
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
            background: linear-gradient(135deg, rgba(255, 255, 255, 0.9) 0%, rgba(255, 255, 255, 0.8) 100%);
            color: #1e293b;
            box-shadow: 0 25px 50px rgba(99, 102, 241, 0.15), 0 8px 32px rgba(0, 0, 0, 0.1);
            border: 1px solid rgba(99, 102, 241, 0.2);
            backdrop-filter: blur(20px);
            transition: all 0.3s ease;
        }

        .haiku-display:hover {
            transform: translateY(-2px);
            box-shadow: 0 30px 60px rgba(99, 102, 241, 0.2), 0 12px 40px rgba(0, 0, 0, 0.15);
            border-color: rgba(99, 102, 241, 0.3);
        }

        .haiku-display p {
            font-family: 'Playfair Display', serif;
            font-size: 1.85rem;
            line-height: 1.35;
            letter-spacing: 0.02em;
            margin: 0.35rem 0;
            color: #1e293b;
        }

        .stAlert {
            border-radius: 18px;
        }
        </style>
        """,
        unsafe_allow_html=True,
    )

    # Initialize storage service
    storage_service = get_storage_service()

    # Create sidebar for haiku history
    with st.sidebar:
        st.markdown("### 📚 Haiku History")

        if storage_service and storage_service.is_available():
            # Add refresh button and search
            st.markdown("**Search by subject**")
            col1, col2 = st.columns([3, 1])
            with col1:
                search_query = st.text_input(
                    "Search haikus",
                    placeholder="Type to filter haikus...",
                    key="search_query",
                    label_visibility="collapsed",
                )
            with col2:
                if st.button("🔄", help="Refresh haiku list", key="refresh_button"):
                    st.rerun()

            # Get haikus based on search
            if search_query:
                haikus = storage_service.search_haikus(search_query, limit=20)
            else:
                haikus = storage_service.get_recent_haikus(limit=10)

            if haikus:
                st.markdown(
                    f"**{len(haikus)} haiku{'s' if len(haikus) != 1 else ''} found**"
                )
                for haiku in haikus:
                    render_haiku_card(haiku)
            else:
                st.markdown("*No haikus found*")
        else:
            st.markdown("*Storage not available*")
            st.markdown(
                "Add `SUPABASE_URL` and `SUPABASE_KEY` to your `.env` file "
                "to enable haiku storage."
            )

    # Main content area
    with st.container():
        st.markdown(
            """
            <div class="hero-text">
                <h1>LLM Haiku Generator</h1>
                <p>Summon bespoke 5-7-5 verses that capture the essence of your chosen subject.</p>  # noqa: E501
                <p>Type a subject, press Enter, and enjoy a refined haiku in seconds.</p>  # noqa: E501
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
                    const label = (input.getAttribute('aria-label') || '')
                        .trim().toLowerCase();
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
                except (
                    Exception
                ) as exc:  # noqa: BLE001 - surface any API/runtime errors
                    st.error(f"Failed to generate poem: {exc}")
                    return

            st.session_state["generated_poem"] = poem

            # Auto-save to Supabase if available
            if storage_service and storage_service.is_available():
                saved_haiku = storage_service.save_haiku(subject, poem)
                if saved_haiku:
                    st.success("✨ Haiku saved to history!")
                    # Store success message in session state to persist across reruns
                    st.session_state["save_success"] = True
                    # Refresh to show the new haiku in sidebar
                    st.rerun()
                else:
                    st.warning("⚠️ Generated haiku but couldn't save to history")

        # Show persistent success message if haiku was just saved
        if st.session_state.get("save_success", False):
            st.success("✨ Haiku saved to history!")
            # Clear the flag so message doesn't persist forever
            st.session_state["save_success"] = False

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
