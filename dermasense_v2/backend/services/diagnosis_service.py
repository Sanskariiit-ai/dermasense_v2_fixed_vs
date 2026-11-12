"""Rank skin conditions that *could* explain the reported symptoms.

This is a conversation aid, not a diagnosis. Results are always presented as
possibilities to discuss with a clinician."""
import json
from functools import lru_cache
from pathlib import Path

from config.settings import settings


@lru_cache(maxsize=1)
def _data() -> tuple[dict, dict]:
    base = Path(settings.data_dir)
    diseases = json.loads((base / "diseases.json").read_text(encoding="utf-8"))
    recs = json.loads((base / "recommendations.json").read_text(encoding="utf-8"))
    return diseases, recs


def rank_conditions(symptom_names: list[str], top_n: int = 3) -> list[dict]:
    diseases, recs = _data()
    reported = set(symptom_names)
    if not reported:
        return []
    results = []
    for name, info in diseases.items():
        needed = set(info["symptoms"])
        matched = sorted(reported & needed)
        if not matched:
            continue
        # Reward covering the condition's symptoms and explaining what the person reported.
        coverage = len(matched) / len(needed)
        explained = len(matched) / len(reported)
        results.append(
            {
                "condition": name,
                "score": round(0.6 * coverage + 0.4 * explained, 3),
                "matched_symptoms": matched,
                "confidence_note": "stronger match" if len(matched) >= 2 else "weak match: only one symptom in common",
                "description": info["description"],
                "recommendations": recs.get(name, []),
            }
        )
    results.sort(key=lambda r: (-r["score"], r["condition"]))
    return results[:top_n]
