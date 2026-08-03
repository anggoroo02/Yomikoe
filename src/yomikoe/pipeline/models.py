from typing import TypedDict

from yomikoe.audio import LoadedAudio
from yomikoe.engines import TranscriptionResult


class PipelineResult(TypedDict):
    audio: LoadedAudio
    transcription: TranscriptionResult