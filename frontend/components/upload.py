import streamlit as st
from utils.api import upload_pdf


def render_upload():
    st.error("THIS IS MY UPLOAD PAGE")
    st.header("📄 Upload PDF")

    uploaded_file = st.file_uploader(
        "Choose a PDF",
        type=["pdf"]
    )

    if uploaded_file:

        st.success("PDF Selected Successfully")

        col1, col2 = st.columns(2)

        with col1:
            st.metric(
                "Size",
                f"{uploaded_file.size/(1024*1024):.2f} MB"
            )

        with col2:
            st.metric(
                "Format",
                "PDF"
            )

        st.write("**Filename:**", uploaded_file.name)

        if st.button(
            "Upload PDF",
            use_container_width=True
        ):

            with st.spinner("Uploading PDF..."):

                response = upload_pdf(uploaded_file)

            if response is None:

                st.error("❌ Unable to connect to the backend.")

            elif response.status_code == 200:

                data = response.json()

                st.success("✅ PDF uploaded successfully!")

                progress = st.progress(0)

                status = st.empty()

                import time

                status.info("📤 Upload Complete")
                progress.progress(25)
                time.sleep(0.6)

                status.info("📄 Processing PDF...")
                progress.progress(50)
                time.sleep(0.8)

                status.info("📝 Extracting Text...")
                progress.progress(75)
                time.sleep(0.8)

                status.success("🤖 Ready for Chat!")
                progress.progress(100)

                st.markdown("### 📄 Upload Details")

                st.write(f"**Filename:** {data['filename']}")
                st.write(f"**Content Type:** {data['content_type']}")
                st.write(f"**Size:** {data['size']} bytes")