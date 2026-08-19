import base64

from google import genai

from app.config.settings import GEMINI_API_KEY


# ---------------------------------------------------------
# Gemini Client
# ---------------------------------------------------------

client = genai.Client(api_key=GEMINI_API_KEY)


# ---------------------------------------------------------
# RAG / Text Question
# ---------------------------------------------------------

def generate_answer(question, context):

    prompt = f"""
You are an AI Assistant.

Use only the context below to answer the user's question.

Context:
{context}

Question:
{question}

Answer:
"""

    interaction = client.interactions.create(
        model="gemini-3.7-flash",
        input=prompt
    )

    return interaction.output_text


# ---------------------------------------------------------
# General Image Analysis
# Used by: POST /vision
# ---------------------------------------------------------

def analyze_image(
    image_bytes: bytes,
    mime_type: str
):

    prompt = """
Analyze this image carefully and provide useful information about it.

Include:

1. A clear description of the image.
2. The main objects, people, or items visible.
3. Any visible text.
4. Important details, labels, numbers, or symbols.
5. The overall context or purpose of the image.
6. Describe the visual style if it is an illustration, artwork,
   diagram, screenshot, photograph, or other visual content.

If text is present, reproduce the important text accurately.

Do not invent information that is not visible in the image.
"""

    # Convert image bytes to Base64
    image_data = base64.b64encode(image_bytes).decode("utf-8")

    # Send image + prompt to Gemini
    interaction = client.interactions.create(
        model="gemini-3.7-flash",
        input=[
            {
                "type": "image",
                "data": image_data,
                "mime_type": mime_type
            },
            {
                "type": "text",
                "text": prompt
            }
        ]
    )

    return interaction.output_text


# ---------------------------------------------------------
# Vision Question & Answer
# Used by: POST /vision/analyze
# ---------------------------------------------------------

def ask_image_question(
    image_bytes: bytes,
    mime_type: str,
    question: str
):

    prompt = f"""
You are an AI assistant capable of understanding images.

Analyze the provided image and answer the user's question
using only information that can be determined from the image.

User question:
{question}

Instructions:

- Give a clear and useful answer.
- Focus specifically on the user's question.
- If the question asks about visible text, read the text from the image.
- If the question asks about objects, describe only objects that are
  actually visible.
- If the question asks about colors, shapes, numbers, labels, or
  other visual details, inspect the image carefully.
- If the requested information is not visible or cannot be determined,
  clearly say that it cannot be determined from the image.
- Do not invent information.
"""

    # Convert image bytes to Base64
    image_data = base64.b64encode(image_bytes).decode("utf-8")

    # Send image + question to Gemini
    interaction = client.interactions.create(
        model="gemini-3.7-flash",
        input=[
            {
                "type": "image",
                "data": image_data,
                "mime_type": mime_type
            },
            {
                "type": "text",
                "text": prompt
            }
        ]
    )

    return interaction.output_text