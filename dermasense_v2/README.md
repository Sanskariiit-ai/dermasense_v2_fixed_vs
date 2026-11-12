# DermaSense v2

A skin-health chat assistant. Patients describe symptoms (by typing or voice); the app detects symptoms, asks
follow-up questions, retrieves reference material, replies with a local LLM, and produces a PDF summary to take to
a doctor. **It gives general information only and never diagnoses.**

## What it does
- Accounts with phone + password sign-in (scrypt hashing, JWT). Every endpoint that touches health data requires a token and only returns the caller's own data.
- Symptom detection (alias matching, plus semantic matching when a neural encoder is available), follow-up questions, and a *ranked list of conditions worth discussing with a doctor*.
- Safety rules that run **before** the language model: emergency signs (breathing trouble, swelling, widespread blistering, infection signs), crisis language, and concerning moles. These return fixed guidance and never reach the model.
- Retrieval-augmented replies from `data/medical_docs` (ChromaDB). If Ollama or the vector store is down, the chat still answers with a safe built-in reply.
- Voice: Whisper transcription (`/voice/transcribe`). The transcript goes into the message box for the patient to review before sending.
- PDF report for a conversation; WebSocket chat endpoint.

## Run it locally
```bash
cp .env.example .env                       # set JWT_SECRET for anything beyond local testing
docker run -d -p 27017:27017 mongo:7       # or use any MongoDB
ollama pull llama3                         # optional: without it the built-in fallback reply is used

cd backend
python -m venv .venv && source .venv/bin/activate      # Windows: .venv\Scripts\activate
pip install -r requirements-dev.txt
python -m scripts.load_docs                # index the reference documents (safe to re-run)
uvicorn main:app --reload                  # http://localhost:8000/docs

cd ../frontend
npm install && npm run dev                 # http://localhost:3000  (proxies /api to the backend)
```
No internet for model downloads? Set `EMBEDDING_BACKEND=hash` for a lightweight offline fallback.

Full stack in containers: `JWT_SECRET=$(python -c "import secrets;print(secrets.token_urlsafe(48))") docker compose up --build`, then open http://localhost:8080. Pull a model once with `docker compose exec ollama ollama pull llama3`.

## Tests
```bash
pip install -r backend/requirements-dev.txt && pytest          # backend: 29 tests, no external services needed
cd frontend && npm test && npm run typecheck && npm run build   # frontend
```

## Docs
`docs/architecture.md`, `docs/api_reference.md`, `docs/deployment.md`. See *Known limits* in the deployment guide before using this with real patients.
