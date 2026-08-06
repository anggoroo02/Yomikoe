from dataclasses import dataclass, field


@dataclass(slots=True)
class TranscriptionSegment:
    """A single transcription segment."""

    start: float
    end: float
    text: str


@dataclass(slots=True)
class TranscriptionResult:
    """Result returned by a transcription engine."""

    language: str
    segments: list[TranscriptionSegment] = field(default_factory=list)
