# API reference
Interactive docs: `http://localhost:8000/docs`. All routes except `/` and `/auth/*` need `Authorization: Bearer <token>`.

| Method | Path | Body | Notes |
|---|---|---|---|
| GET | `/` | | Health check |
| POST | `/auth/register` | `name, age (0-120), gender, phone_number (10-15 digits), password (8+)` | 201 + token; 409 if phone exists |
| POST | `/auth/login` | `phone_number, password` | 200 + token; 401 on failure |
| GET | `/patients/me` | | Own profile |
| GET | `/patients/me/history?session_id=` | | Own messages, oldest first |
| POST | `/chat` | `message (1-2000 chars), session_id?` | Returns `response, urgent, symptoms, followups, conditions, sources, disclaimer, session_id`. `urgent` is `null`, `urgent_review`, `emergency` or `crisis` |
| POST | `/reports` | `session_id` | PDF download of the caller's session |
| POST | `/voice/transcribe` | multipart `file` (wav, mp3, m4a, webm, ogg, flac; max `MAX_AUDIO_MB`) | `{transcript}`; 503 if the speech model is unavailable |
| WS | `/ws/chat?token=` | `{"message": "...", "session_id"?}` | Replies `{type:"response", ...}` or `{type:"error"}`; closes 4401 on a bad token |

Changes from v1: `POST /patients` was removed (use `/auth/register`); `/chat` and `/reports` now require sign-in; `/reports` takes a `session_id` instead of raw patient data and returns the PDF directly.
