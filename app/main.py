import logging
from typing import cast

import streamlit as st

from app.config.settings import ConfigurationError, get_settings
from app.prompts.qa_prompt import SYSTEM_PROMPT
from app.services.gemini_service import (
    ConversationMessage,
    GeminiService,
    GeminiServiceError,
)
from app.utils.logging_config import configure_logging


logger = logging.getLogger(__name__)


def run_app() -> None:
    """Render the Streamlit chat interface and coordinate answer generation."""
    configure_logging()

    st.set_page_config(page_title="AI Question & Answering System", page_icon="💬")
    st.title("AI Question & Answering System")
    st.caption(
        "Ask questions and continue with follow-ups using Google's Gemini model."
    )
    logger.info("Application started.")

    try:
        settings = get_settings()
    except ConfigurationError as error:
        st.error(str(error))
        st.stop()

    service = GeminiService(settings)
    st.sidebar.markdown(f"**Gemini model:** `{settings.gemini_model}`")

    if "messages" not in st.session_state:
        st.session_state.messages = []

    if st.sidebar.button("Clear Conversation"):
        st.session_state.messages = []
        logger.info("Conversation cleared.")
        st.rerun()

    question = st.chat_input("Ask a question")
    if question is not None:
        if not question.strip():
            st.warning("Please enter a question before submitting.")
        else:
            user_message = {"role": "user", "content": question.strip()}
            st.session_state.messages.append(user_message)
            request_messages = cast(
                list[ConversationMessage],
                [
                    {"role": "system", "content": SYSTEM_PROMPT},
                    *st.session_state.messages,
                    ],
            )
            try:
                with st.spinner("Thinking..."):
                    answer = service.generate_answer(request_messages)
                st.session_state.messages.append(
                    {"role": "assistant", "content": answer}
                )
                logger.info("Gemini response generated.")
            except GeminiServiceError as error:
                logger.error("Gemini request failed (%s).", type(error).__name__)
                st.error(str(error))

    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])


if __name__ == "__main__":
    run_app()
