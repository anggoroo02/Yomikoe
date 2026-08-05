from pathlib import Path

from yomikoe.audio import load_audio
from yomikoe.engines import FasterWhisperEngine

audio = load_audio(Path("sample-JP.m4a"))

engine = FasterWhisperEngine(
    device="cpu",
)

result = engine.transcribe(audio)

print(result.language)

print(len(result.segments))

for segment in result.segments[:5]:
    print(segment)