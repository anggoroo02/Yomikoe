from dataclasses import dataclass, field


@dataclass(slots=True)
class SubtitleCue:
    """A single subtitle cue."""

    start: float
    end: float
    text: str


@dataclass(slots=True)
class Subtitle:
    """Subtitle document."""

    language: str
    cues: list[SubtitleCue] = field(default_factory=list)
