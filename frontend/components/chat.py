import streamlit as st

from utils.api import ask_question


def render_chat():
    st.subheader("💬 Ask Questions About Your PDF")

    question = st.text_area(
        "Enter your question",
        placeholder="Example: What is this PDF about?",
        height=100,
    )

    if st.button(
        "Ask Question",
        type="primary",
        use_container_width=True,
    ):
        if not question.strip():
            st.warning("Please enter a question.")
            return

        with st.spinner("Thinking..."):
            status_code, result = ask_question(question.strip())

        if status_code == 200:
            st.success("Answer")

            answer = result.get("answer")

            if answer:
                st.markdown(answer)
            else:
                st.json(result)

        else:
            st.error("Question failed.")
            st.error(result.get("detail", str(result)))