from pathlib import Path

from yomikoe.audio import load_audio
from yomikoe.engines import FasterWhisperEngine
from yomikoe.subtitle import generate_subtitle

audio = load_audio(Path("sample-JP.m4a"))

engine = FasterWhisperEngine(
    device="cpu",
)

result = engine.transcribe(audio)


subtitle = generate_subtitle(result)

print(subtitle.language)
print(len(subtitle.cues))

for cue in subtitle.cues[:5]:
    print(cue)

for segment in result.segments[:5]:
    print(segment)