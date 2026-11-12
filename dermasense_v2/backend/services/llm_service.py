import asyncio
import logging

from config.settings import settings

log = logging.getLogger("dermasense")

DISCLAIMER = (
    "This is general information, not a medical diagnosis. "
    "A doctor or dermatologist can examine your skin and advise on treatment."
)

SYSTEM_PROMPT = """You are DermaSense, a friendly skin-health information assistant.
Rules:
- You are not a doctor. Never state a diagnosis. Talk about possibilities and say a clinician needs to confirm.
- Use ONLY the provided context for medical facts. If the context does not cover the question, say you are not sure.
- Do not recommend prescription drugs or doses.
- Keep answers short (under 150 words), in plain language, and ask at most two follow-up questions.
- If symptoms sound severe or are worsening, advise seeing a doctor promptly.
- Never ask for or repeat personal identifiers such as phone numbers."""


def build_messages(query: str, context: str, symptoms: list[str], conditions: list[str], history: list[dict]) -> list[dict]:
    facts = (
        f"Symptoms noticed so far: {', '.join(symptoms) or 'none yet'}.\n"
        f"Conditions that might be discussed with a doctor (possibilities only): {', '.join(conditions) or 'none'}.\n"
        f"Reference material:\n{context or '(none available)'}"
    )
    msgs = [{"role": "system", "content": SYSTEM_PROMPT + "\n\n" + facts}]
    msgs += [{"role": m["role"], "content": m["content"]} for m in history[-6:] if m["role"] in ("user", "assistant")]
    msgs.append({"role": "user", "content": query})
    return msgs


def _chat_blocking(messages: list[dict]) -> str:
    import ollama

    client = ollama.Client(host=settings.ollama_host) if settings.ollama_host else ollama
    return client.chat(model=settings.ollama_model, messages=messages)["message"]["content"]


async def generate_response(query: str, context: str = "", symptoms=None, conditions=None, history=None) -> str | None:
    """Ask the local model. Returns None if the model is unavailable so callers can fall back."""
    messages = build_messages(query, context, symptoms or [], conditions or [], history or [])
    try:
        return (await asyncio.to_thread(_chat_blocking, messages)).strip() or None
    except Exception as exc:
        log.warning("LLM unavailable: %s", exc)
        return None


def fallback_response(symptoms: list[str], followups: list[str], conditions: list[dict]) -> str:
    """Deterministic reply used when the language model is not reachable."""
    parts = []
    if symptoms:
        parts.append(f"Thanks for sharing. I noticed: {', '.join(symptoms)}.")
    else:
        parts.append("Thanks for sharing. Could you describe what you are seeing or feeling on your skin?")
    if conditions:
        top = conditions[0]
        parts.append(f"Some people with these symptoms have {top['condition']}, though only a clinician can tell.")
        if top.get("recommendations"):
            parts.append("General tips: " + "; ".join(top["recommendations"][:3]) + ".")
    if followups:
        parts.append("To understand better: " + " ".join(followups[:2]))
    return " ".join(parts)
