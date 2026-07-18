import streamlit as st
from datetime import datetime


def render_chat():

    st.header("💬 OmniBrain Assistant")
    st.caption(
        "Upload a financial report and ask questions about it. The assistant will provide insights and analysis based on the content of the uploaded PDF."
    )

    if "messages" not in st.session_state:
        st.session_state.messages = []

    # Welcome Screen
    if len(st.session_state.messages) == 0:

        st.success("👋 Welcome to OmniBrain!")

        st.markdown("""
            ### You can ask things like:

            - 📈 Summarize this financial report
            - 📊 Explain the revenue trend
            - 💰 What are the major expenses?
            - ⚠️ Identify investment risks
            - 📄 Give me key takeaways
        """)

    st.markdown("---")    

    # Display previous messages
    for message in st.session_state.messages:

        with st.chat_message(message["role"]):
            st.markdown(message["content"])

            if message["role"] == "assistant":
                st.caption(
                    f"📄 Citation: Demo PDF | 🕒 {message['time']}"
                )
            st.divider()    
    
    st.markdown("### 🚀 Suggested Questions")

    col1, col2 = st.columns(2)

    suggested_prompt = None

    with col1:

        if st.button("📄 Summarize Document"):
            suggested_prompt = "Summarize the uploaded document."

        if st.button("📈 Revenue Growth"):
            suggested_prompt = "Explain the revenue growth."

    with col2:

        if st.button("💰 EBITDA"):
            suggested_prompt = "Explain EBITDA."

        if st.button("⚠️ Investment Risks"):
            suggested_prompt = "List the investment risks."
    prompt = st.chat_input(
        "Ask a question about the uploaded PDF..."
    )

    if not prompt and suggested_prompt:
        prompt = suggested_prompt

    if prompt:

        current_time = datetime.now().strftime("%H:%M")

        st.session_state.messages.append(
            {
                "role": "user",
                "content": prompt,
                "time": current_time,
            }
        )

        with st.chat_message("user"):
            st.markdown(prompt)

        with st.chat_message("assistant"):

            with st.spinner("Analyzing document..."):

                response = f"""
### 📊 Analysis

**Question**

> {prompt}

---

✅ Placeholder response generated successfully.

---

📄 **Citation**

Page 12 (Demo)

---

⚠️ This is currently a placeholder response.
FastAPI and the Agentic AI backend will be connected in the upcoming development phase.

"""

                st.markdown(response)

                st.caption(
                    
                    f"📄 Demo PDF | 🕒 {current_time}"
                )

        st.session_state.messages.append(
            {
                "role": "assistant",
                "content": response,
                "time": current_time,
            }
        )