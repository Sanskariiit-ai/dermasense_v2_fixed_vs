import json
from pathlib import Path

DATA = Path(__file__).resolve().parents[2] / "data"
load = lambda n: json.loads((DATA / n).read_text(encoding="utf-8"))


def test_every_disease_symptom_is_defined_with_followups():
    symptoms, diseases = load("symptoms.json"), load("diseases.json")
    for disease, info in diseases.items():
        for s in info["symptoms"]:
            assert s in symptoms, f"{disease} uses undefined symptom {s!r}"
    for name, info in symptoms.items():
        assert info["followups"] and info["aliases"] and info["category"], name


def test_map_and_recommendations_match_diseases():
    diseases = load("diseases.json")
    assert {k: v["symptoms"] for k, v in diseases.items()} == load("disease_symptom_map.json")
    assert set(load("recommendations.json")) == set(diseases)


def test_red_flag_patterns_compile_and_match_examples():
    from services.safety_service import check_red_flags

    assert check_red_flags("swelling of my face and tongue")["level"] == "emergency"
    assert check_red_flags("a rash with fever and red streaks")["level"] == "emergency"
    assert check_red_flags("my skin is a bit dry") is None
