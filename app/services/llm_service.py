from google import genai

from app.config.settings import GEMINI_API_KEY


client = genai.Client(api_key=GEMINI_API_KEY)


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