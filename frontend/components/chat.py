import streamlit as st
from datetime import datetime
from utils.api import ask_question


def render_chat():

    st.caption("Ask questions about your uploaded document.")

    if "messages" not in st.session_state:
        st.session_state.messages = []

    # -----------------------------
    # No document uploaded
    # -----------------------------

    if st.session_state.get("current_document") is None:

        st.info("👈 Upload a document to start chatting with OmniBrain.")

        st.markdown("### Example Questions")

        col1, col2 = st.columns(2)

        with col1:
            st.button(
                "📄 Summarize the document",
                disabled=True,
                use_container_width=True
            )

            st.button(
                "📊 Key insights",
                disabled=True,
                use_container_width=True
            )

        with col2:
            st.button(
                "⚠️ Risks",
                disabled=True,
                use_container_width=True
            )

            st.button(
                "💰 Financial highlights",
                disabled=True,
                use_container_width=True
            )

        return

    # -----------------------------
    # Welcome
    # -----------------------------

    if len(st.session_state.messages) == 0:

        st.markdown("""
### 👋 Welcome

Your document is ready.

Try asking:

- Summarize this document
- What are the key takeaways?
- Explain this report
- Find important risks
- Give me action items

---
""")

    # -----------------------------
    # Chat History
    # -----------------------------

    for message in st.session_state.messages:

        with st.chat_message(message["role"]):

            st.markdown(message["content"])

            st.caption(message["time"])

    # -----------------------------
    # Input
    # -----------------------------

    prompt = st.chat_input(
        "Ask OmniBrain anything..."
    )

    if prompt:

        current_time = datetime.now().strftime("%H:%M")

        st.session_state.messages.append(
            {
                "role": "user",
                "content": prompt,
                "time": current_time
            }
        )

        with st.chat_message("user"):

            st.markdown(prompt)

            st.caption(current_time)

        with st.chat_message("assistant"):

            with st.spinner("Thinking..."):

                answer = ask_question(prompt)
                response = f"### Response\n\n{answer}"

                st.markdown(response)

                st.caption(current_time)

        st.session_state.messages.append(
            {
                "role": "assistant",
                "content": response,
                "time": current_time
            }
        )