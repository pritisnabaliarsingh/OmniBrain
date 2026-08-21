import streamlit as st

from utils.api import analyze_image


def render_vision():
    st.subheader("🖼️ Analyze an Image")

    image = st.file_uploader(
        "Choose an image",
        type=[
            "png",
            "jpg",
            "jpeg",
            "webp",
        ],
        key="image_uploader",
    )

    if image is not None:
        st.image(
            image,
            caption=image.name,
            use_container_width=True,
        )

        question = st.text_area(
            "What do you want to know about this image?",
            placeholder="Example: Describe everything visible in this image.",
            height=100,
            key="vision_question",
        )

        if st.button(
            "Analyze Image",
            type="primary",
            use_container_width=True,
        ):
            if not question.strip():
                st.warning("Please enter a question about the image.")
                return

            with st.spinner("Analyzing image with Gemini..."):
                status_code, result = analyze_image(
                    image,
                    question.strip(),
                )

            if status_code == 200:
                st.success("Image analyzed successfully!")

                answer = result.get("answer")

                if answer:
                    st.markdown("### Analysis")
                    st.markdown(answer)

                with st.expander("Analysis details"):
                    st.json(result)

            else:
                st.error("Image analysis failed.")
                st.error(result.get("detail", str(result)))