# Architecture

```
Browser (Next.js)  --/api-->  FastAPI  -->  MongoDB      patients, chat history
  chat, voice, PDF              |  -->  Redis/in-memory   session state (symptoms, questions asked)
                                |  -->  ChromaDB          reference passages (RAG)
                                |  -->  Ollama            language model
                                |  -->  faster-whisper    speech to text
```

## One chat turn (`services/chat_service.py`)
1. Save the user message.
2. **Safety check** (`safety_service`, rules in `data/red_flags.json`). Crisis and emergency matches return a fixed reply immediately; the model is never called. "Urgent review" matches add guidance to the reply.
3. Detect symptoms (`symptom_service`): whole-word alias matches from `data/symptoms.json`, plus embedding similarity when a neural encoder is loaded.
4. Merge into the session (Redis, 1 hour), pick up to 3 follow-up questions not yet asked.
5. Rank conditions (`diagnosis_service`) using `data/diseases.json`. Results are labelled possibilities.
6. Retrieve passages (`rag/retriever`), then ask the model with a system prompt that forbids diagnoses and drug advice. On failure, `llm_service.fallback_response` answers instead.
7. Save the reply and return reply, symptoms, follow-ups, conditions, sources, disclaimer.

## Design decisions
- **Safety is rule-based and runs first.** A model cannot be trusted to always escalate.
- **Per-patient isolation.** The patient id comes only from the verified token; session keys and history queries include it.
- **Lazy heavy dependencies.** Whisper, sentence-transformers and Ollama load on first use, so the API starts fast and degrades gracefully.
- **One vector collection per embedding backend**, because vectors from different encoders are not comparable.
- **Idempotent indexing.** Chunk ids are hashes, so `load_docs` can be re-run.
- Uploaded audio is written to a private temp file, size/type checked, and deleted; client filenames are never used on disk.
