# Developer Instructions

Hello Everyone! 👋

Welcome to the project.

To make development, Docker setup, and GitHub Actions easier for everyone, please follow the instructions below while working on your module. This will help us maintain a consistent project structure and reduce setup issues across different systems.

---

# Required Files

Every developer should maintain the following two files in their project/module directory:

```
requirements.txt
info.md
```

---

# 1. requirements.txt

This file contains all the Python packages required to run your module.

Example:

```text
fastapi==0.116.1
uvicorn==0.35.0
langchain==0.3.27
torch==2.8.0
pandas==2.3.1
numpy==2.3.1
```

Please make sure package versions are included.

### How to Generate requirements.txt

Open your terminal inside your project directory and run:

```bash
pip freeze > requirements.txt
```

This command automatically lists all installed Python packages along with their versions.

Whenever you install a new package or remove an existing one, regenerate this file before pushing your code.

---

# 2. info.md

Create a file named `info.md` in your module directory.

This file should contain the basic information required to run your project.

Use the following template.

# Module Information

Developer Name:

Branch Name:

Module Name:

---

## Install Command

Example:

```bash
pip install -r requirements.txt
```

---

## Run Command

Example:

```bash
python main.py
```

or

```bash
python app.py
```

or

```bash
uvicorn app.main:app --reload
```

or any other command that starts your project.

---

## Port Number

Mention the port on which your application runs.

Example:

```
8000
```

or

```
8501
```

If your project doesn't use any port, simply write:

```
Not Applicable
```

---

## Environment Variables

Mention all environment variables required to run your project.

Example:

```
OPENAI_API_KEY

DATABASE_URL

SECRET_KEY
```

If your project doesn't require any environment variables, simply write:

```
None
```

---

## Additional Notes

Mention anything important that another developer should know before running your module.

Examples:

- Download a model before running.
- Install PostgreSQL first.
- Run Ollama locally.
- Requires GPU.
- Works only on Python 3.11.

If there are no additional notes, simply write:

```
None
```

---

# Best Practices

Before pushing your code, please make sure you have completed the following checklist.

- Your code runs successfully without errors.
- requirements.txt has been updated.
- info.md has been updated if anything has changed.
- Remove unnecessary files before committing.
- Do not commit virtual environments (`venv`, `.venv`, etc.).
- Do not commit cache folders (`__pycache__`).
- Do not commit API keys, passwords, tokens, or any sensitive information.
- Commit only the files related to your work.
- Write meaningful commit messages.

Examples of good commit messages:

```text
feat(frontend): add chat interface

feat(rag): implement FAISS retriever

fix(database): resolve connection timeout

docs: update setup instructions
```

Avoid commit messages like:

```text
update

changes

final

done

new
```

---

# Why Are We Following This?

Maintaining these files helps us:

- Run each module easily on different systems.
- Create Docker containers without repeatedly asking for setup information.
- Configure GitHub Actions for automated testing and builds.
- Reduce setup and dependency-related issues.
- Make it easier for everyone to understand and use each other's modules.

---

# Need Help?

If you face any issues related to:

- Git
- GitHub
- Python
- Dependencies
- Docker
- Project setup
- Environment variables

or anything else related to the project,

please feel free to message me anytime.

I'll be happy to help.

Happy Coding! 🚀