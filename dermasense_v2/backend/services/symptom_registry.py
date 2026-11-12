import json
from functools import lru_cache
from pathlib import Path

from config.settings import settings


@lru_cache(maxsize=1)
def _load() -> dict:
    with open(Path(settings.data_dir) / "symptoms.json", encoding="utf-8") as f:
        return json.load(f)


def get_symptom(name: str) -> dict | None:
    return _load().get(name.lower())


def get_all_symptoms() -> list[str]:
    return list(_load().keys())


def get_aliases() -> dict[str, list[str]]:
    return {k: v.get("aliases", [k]) for k, v in _load().items()}
