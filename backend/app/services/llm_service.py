import os
from app.config.settings import GEMINI_API_KEY
from app.utils.logger import logger

USE_GEMINI = bool(GEMINI_API_KEY and GEMINI_API_KEY != "dummy_key")

if USE_GEMINI:
    from google import genai
    client = genai.Client(api_key=GEMINI_API_KEY)
    logger.info("Using Gemini API for LLM.")
else:
    logger.info("Using local HuggingFace model (TinyLlama) because GEMINI_API_KEY is missing or dummy.")
    from transformers import pipeline
    # Initialize pipeline on CPU
    llm_pipeline = pipeline(
        "text-generation",
        model="TinyLlama/TinyLlama-1.1B-Chat-v1.0"
    )

def generate_answer(question, context):
    if USE_GEMINI:
        prompt = f"Use only the context below to answer the user's question.\n\nContext:\n{context}\n\nQuestion:\n{question}\n\nAnswer:\n"
        interaction = client.models.generate_content(
            model="gemini-3.6-flash",
            contents=prompt
        )
        return interaction.text
    else:
        messages = [
            {"role": "system", "content": f"You are an AI Assistant. Answer the question using ONLY the provided context.\n\nContext:\n{context}"},
            {"role": "user", "content": question},
        ]
        prompt = llm_pipeline.tokenizer.apply_chat_template(messages, tokenize=False, add_generation_prompt=True)
        outputs = llm_pipeline(prompt, max_new_tokens=256, do_sample=True, temperature=0.7, top_k=50, top_p=0.95)

        # Parse output after the prompt
        result = outputs[0]["generated_text"]
        if "<|assistant|>" in result:
            return result.split("<|assistant|>")[-1].strip()
        return result.strip()
