import io
import wave
from dataclasses import dataclass
from pathlib import Path
from typing import Optional

from django.core.files.base import ContentFile

from .models import Composition


@dataclass
class GenerationParams:
    title: str
    mood: str
    genre: str
    instruments: str
    tempo_bpm: int
    length_seconds: int


def _sine_stub(duration_seconds: int, sample_rate: int = 16000) -> bytes:
    # Generate a silent WAV as a placeholder to keep stack lightweight
    num_frames = duration_seconds * sample_rate
    with io.BytesIO() as buffer:
        with wave.open(buffer, "wb") as wav:
            wav.setnchannels(1)
            wav.setsampwidth(2)
            wav.setframerate(sample_rate)
            wav.writeframes(b"\x00\x00" * num_frames)
        return buffer.getvalue()


def generate_audio(owner, title: str, mood: str, genre: str, instruments: str, tempo_bpm: int, length_seconds: int) -> Composition:
    params = GenerationParams(
        title=title,
        mood=mood,
        genre=genre,
        instruments=instruments,
        tempo_bpm=tempo_bpm,
        length_seconds=length_seconds,
    )

    audio_bytes = _sine_stub(duration_seconds=params.length_seconds)

    composition = Composition(
        owner=owner,
        title=params.title,
        mood=params.mood,
        genre=params.genre,
        instruments=params.instruments,
        tempo_bpm=params.tempo_bpm,
        length_seconds=params.length_seconds,
        model_used="stub-generator",
    )
    filename = f"{params.title.replace(' ', '_').lower()}_{owner.id}.wav"
    composition.audio_file.save(filename, ContentFile(audio_bytes), save=False)
    composition.save()
    return composition


