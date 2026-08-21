from app.config.settings import GEMINI_API_KEY
from app.utils.logger import logger

USE_GEMINI = bool(
    GEMINI_API_KEY and GEMINI_API_KEY != "dummy_key"
)

client = None
llm_pipeline = None


def _get_gemini_client():
    global client

    if client is None:
        from google import genai

        client = genai.Client(api_key=GEMINI_API_KEY)
        logger.info("Using Gemini API for LLM.")

    return client


def _get_local_pipeline():
    global llm_pipeline

    if llm_pipeline is None:
        from transformers import pipeline

        logger.info("Loading local TinyLlama model.")

        llm_pipeline = pipeline(
            "text-generation",
            model="TinyLlama/TinyLlama-1.1B-Chat-v1.0",
        )

    return llm_pipeline


def generate_answer(question, context):
    if USE_GEMINI:
        client = _get_gemini_client()

        prompt = (
            "Use only the context below to answer the user's question.\n\n"
            f"Context:\n{context}\n\n"
            f"Question:\n{question}\n\n"
            "Answer:\n"
        )

        interaction = client.models.generate_content(
            model="gemini-3.6-flash",
            contents=prompt,
        )

        return interaction.text

    llm = _get_local_pipeline()

    messages = [
        {
            "role": "system",
            "content": (
                "You are an AI Assistant. Answer the question using "
                f"ONLY the provided context.\n\nContext:\n{context}"
            ),
        },
        {
            "role": "user",
            "content": question,
        },
    ]

    prompt = llm.tokenizer.apply_chat_template(
        messages,
        tokenize=False,
        add_generation_prompt=True,
    )

    outputs = llm(
        prompt,
        max_new_tokens=256,
        do_sample=True,
        temperature=0.7,
        top_k=50,
        top_p=0.95,
    )

    result = outputs[0]["generated_text"]

    if "<|assistant|>" in result:
        return result.split("<|assistant|>")[-1].strip()

    return result.strip()