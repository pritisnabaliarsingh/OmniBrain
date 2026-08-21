import requests


BASE_URL = "http://127.0.0.1:8000"


def check_backend():
    try:
        response = requests.get(
            f"{BASE_URL}/health",
            timeout=10,
        )

        if response.status_code == 200:
            return True, response.json()

        return False, response.text

    except requests.RequestException as e:
        return False, str(e)


def upload_pdf(file):
    try:
        files = {
            "file": (
                file.name,
                file.getvalue(),
                "application/pdf",
            )
        }

        response = requests.post(
            f"{BASE_URL}/upload",
            files=files,
            timeout=120,
        )

        return response.status_code, response.json()

    except requests.RequestException as e:
        return 500, {"detail": str(e)}


def ask_question(question):
    try:
        response = requests.post(
            f"{BASE_URL}/ask",
            json={
                "question": question,
            },
            timeout=180,
        )

        try:
            data = response.json()
        except ValueError:
            data = {
                "detail": response.text,
            }

        return response.status_code, data

    except requests.RequestException as e:
        return 500, {"detail": str(e)}


def analyze_image(image, question):
    try:
        files = {
            "file": (
                image.name,
                image.getvalue(),
                image.type,
            )
        }

        data = {
            "question": question,
        }

        response = requests.post(
            f"{BASE_URL}/vision/analyze",
            files=files,
            data=data,
            timeout=180,
        )

        try:
            result = response.json()
        except ValueError:
            result = {
                "detail": response.text,
            }

        return response.status_code, result

    except requests.RequestException as e:
        return 500, {"detail": str(e)}