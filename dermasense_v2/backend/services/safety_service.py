"""Rule-based safety checks that run BEFORE any language model is called."""
import json
import re
from functools import lru_cache
from pathlib import Path

from config.settings import settings

EMERGENCY_REPLY = (
    "{reason} Please get medical help right now: call your local emergency number "
    "(112 in India) or go to the nearest emergency department. Do not wait for an online chat."
)
URGENT_REPLY = (
    "{reason} Please arrange to see a doctor or dermatologist soon, ideally within a few days, "
    "and sooner if it is getting worse."
)
CRISIS_REPLY = (
    "{reason} You do not have to handle this alone. If you might act on thoughts of harming yourself, "
    "call your local emergency number now (112 in India). You can also contact a crisis line such as "
    "Tele-MANAS (14416 in India) or reach out to someone you trust. If skin problems are weighing on you, "
    "a doctor can help with that too."
)


@lru_cache(maxsize=1)
def _flags() -> dict:
    raw = json.loads((Path(settings.data_dir) / "red_flags.json").read_text(encoding="utf-8"))
    return {
        level: [(f["id"], [re.compile(p, re.I) for p in f["patterns"]], f["message"]) for f in items]
        for level, items in raw.items()
    }


def check_red_flags(text: str) -> dict | None:
    """Return {level, id, reply} for the most serious matching rule, or None."""
    flags = _flags()
    for level, template in (("crisis", CRISIS_REPLY), ("emergency", EMERGENCY_REPLY), ("urgent_review", URGENT_REPLY)):
        for flag_id, patterns, message in flags.get(level, []):
            if any(p.search(text) for p in patterns):
                return {"level": level, "id": flag_id, "reply": template.format(reason=message)}
    return None
