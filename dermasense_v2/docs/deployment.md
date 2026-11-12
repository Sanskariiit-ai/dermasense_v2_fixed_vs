# Deployment

## Environment variables (`.env.example`)
`ENV`, `MONGO_URI`, `DATABASE_NAME`, `REDIS_URL` (optional), `JWT_SECRET` (**required when ENV=production**), `CORS_ORIGINS`, `OLLAMA_MODEL`, `OLLAMA_HOST`, `EMBEDDING_BACKEND` (`auto|sentence-transformers|hash`), `WHISPER_MODEL`, `MAX_AUDIO_MB`. Frontend: `BACKEND_URL` (build time, where `/api` is forwarded).

## Docker
`docker-compose.yml` runs mongo, redis, ollama, backend, frontend and nginx (port 8080). The backend indexes the reference documents on every start. Pull a model: `docker compose exec ollama ollama pull llama3`.

## Before real patients use it
- Serve over HTTPS (terminate TLS in front of nginx), set a strong `JWT_SECRET`, enable MongoDB authentication and encrypted backups, and never commit `.env`. Rotate any credential that was ever shared.
- Add rate limiting on `/auth/*` and `/chat` (for example at nginx or with a library such as slowapi); it is not built in.
- Have a qualified clinician review `data/medical_docs`, `data/red_flags.json` and the model's system prompt, and test with your chosen model.
- Health data is regulated. Review your obligations (for example India's Digital Personal Data Protection Act 2023) with a legal adviser; add consent, retention and deletion features as required.
- Confirm the emergency and helpline numbers in `services/safety_service.py` (112 and Tele-MANAS 14416 are used for India) for each region you serve.

## Known limits
- Not a medical device and not a diagnostic tool.
- Symptom coverage is small (14 symptoms, 4 conditions); extend `data/*.json` and `data/medical_docs` and re-run `python -m scripts.load_docs`.
- Refresh tokens, password reset, and account deletion are not implemented.
- `infra/kubernetes`, `infra/terraform` and `ai/*` are empty placeholders; no manifests were written because they could not be tested here.
- The WebSocket endpoint is not used by the web app (it uses HTTP).
