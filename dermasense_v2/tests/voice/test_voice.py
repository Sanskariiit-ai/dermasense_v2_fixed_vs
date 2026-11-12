import array
import struct

from voice import whisper_engine
from voice.vad import is_speech


def pcm(amplitude: int, n: int = 480) -> bytes:
    return array.array("h", [amplitude if i % 2 else -amplitude for i in range(n)]).tobytes()


def test_vad_energy_fallback():
    assert is_speech(pcm(8000)) is True
    assert is_speech(pcm(0)) is False
    assert is_speech(b"") is False


class FakeModel:
    def transcribe(self, path):
        class Seg:
            text = " my skin itches "
        return [Seg(), Seg()], None


def test_transcribe_endpoint(client, auth, monkeypatch):
    monkeypatch.setattr(whisper_engine, "_model", FakeModel())
    headers, _ = auth
    r = client.post("/voice/transcribe", files={"file": ("a.wav", b"RIFFxxxx", "audio/wav")}, headers=headers)
    assert r.status_code == 200 and r.json()["transcript"] == "my skin itches my skin itches"


def test_transcribe_validation(client, auth, monkeypatch):
    monkeypatch.setattr(whisper_engine, "_model", FakeModel())
    headers, _ = auth
    assert client.post("/voice/transcribe", files={"file": ("a.exe", b"x", "x/y")}, headers=headers).status_code == 415
    assert client.post("/voice/transcribe", files={"file": ("a.wav", b"", "audio/wav")}, headers=headers).status_code == 400
    monkeypatch.setattr("config.settings.settings.max_audio_mb", 0)
    assert client.post("/voice/transcribe", files={"file": ("a.wav", b"xx", "audio/wav")}, headers=headers).status_code == 413
    assert client.post("/voice/transcribe", files={"file": ("a.wav", b"x", "audio/wav")}).status_code == 401


def test_hostile_filename_never_touches_disk_path(client, auth, monkeypatch):
    monkeypatch.setattr(whisper_engine, "_model", FakeModel())
    headers, _ = auth
    r = client.post("/voice/transcribe", files={"file": ("../../evil.wav", b"RIFF", "audio/wav")}, headers=headers)
    assert r.status_code == 200
