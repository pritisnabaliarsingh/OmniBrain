from transformers import pipeline
generator = pipeline("text-generation", model="gpt2")
response = generator("Say hello in one line", max_new_tokens=20)
print("LLM environment set up successfully.")
print(response[0]['generated_text'])
