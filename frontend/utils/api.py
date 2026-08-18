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
    