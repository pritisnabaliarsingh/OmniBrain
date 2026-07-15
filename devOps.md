# DevOps Notes — OmniBrain

Quick guide on how to run the project locally, test your code, and commit properly. Read this before you push.

## Project structure (so far)

```
omnibrain/
├── app/                # FastAPI backend (Member 1)
├── streamlit_app.py     # Streamlit frontend (Member 2)
├── parser/               # PDF/document parsing (Member 3)
├── rag/                  # LangChain / agents (Member 4)
├── db/                   # DB models, schema (Member 5)
├── tests/                # Pytest tests (Member 6)
├── Dockerfile             # backend container
├── Dockerfile.frontend    # frontend container
├── docker-compose.yml
└── requirements.txt
```

If your folder names differ from this, let me know and I'll update it.

## Running the project

Easiest way — spin up everything at once (it will be added shortly):

```bash
docker-compose up --build
```

- Backend: http://localhost:8000
- Frontend: http://localhost:8501

If you just want to run your own piece without Docker, that's fine too — just make sure it also works in Docker before you open a PR, since that's what CI will check.

## Before you push

1. **Run your code and make sure it starts without errors.**
2. **Run the tests:**
   ```bash
   pytest
   ```
3. If you added a new dependency, add it to `requirements.txt` (or `requirements-frontend.txt` if it's frontend-only).

## Branching

- Work on your own `feature/<yourpart>` branch (e.g. `feature/backend`, `feature/rag`).
- Open a PR into `develop` when your piece is ready — don't push directly to `main` or `develop`.
- Small, frequent PRs are easier to review than one giant one at the end.

## Commits

- One commit = one logical change. Doesn't need to be huge, just needs to make sense on its own.
- Write what you actually did: `add pdf text extraction` not `update files`.

## What CI checks automatically

Every PR will run:
- Linting (basic formatting checks)
- Pytest (whatever tests exist at that point)
- A Docker build, to make sure your code doesn't break the container

If CI fails on your PR, check the logs first — it'll usually tell you exactly what broke.

## Questions / stuck?

Ping me directly if:
- Docker won't build for you locally
- You're not sure where your code should live
- You want me to add something to `docker-compose.yml` (new service, new port, etc.)

I'd rather you ask early than push something that breaks the build for everyone else.