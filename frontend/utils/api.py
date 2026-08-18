import requests

import os
BASE_URL = os.getenv("API_URL", "http://127.0.0.1:8000")


def check_health():
    try:
        response = requests.get(f"{BASE_URL}/health")
        return response.json()
    except requests.exceptions.RequestException:
        return {
            "status": "offline",
            "message": "Backend is unavailable."
        }


def upload_pdf(uploaded_file):
    try:
        files = {
            "file": (
                uploaded_file.name,
                uploaded_file.getvalue(),
                "application/pdf"
            )
        }

        response = requests.post(
            f"{BASE_URL}/upload",
            files=files
        )

        return response

    except requests.exceptions.RequestException:
        return None

def ask_question(question):
    try:
        response = requests.post(
            f"{BASE_URL}/ask",
            json={"question": question}
        )
        if response.status_code == 200:
            return response.json().get("answer")
        else:
            return f"Error: {response.text}"
    except requests.exceptions.RequestException as e:
        return f"Error connecting to backend: {e}"
    