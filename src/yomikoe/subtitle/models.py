import math
from dataclasses import dataclass, field


@dataclass(slots=True)
class SubtitleCue:
    """A single subtitle cue."""

    start: float
    end: float
    text: str

    def __post_init__(self) -> None:
        if not isinstance(self.start, (int, float)):
            raise TypeError("start must be a number")

        if not isinstance(self.end, (int, float)):
            raise TypeError("end must be a number")

        if not math.isfinite(self.start):
            raise ValueError("start must be finite")

        if not math.isfinite(self.end):
            raise ValueError("end must be finite")

        if self.start < 0:
            raise ValueError("start must be >= 0")

        if self.end <= self.start:
            raise ValueError("end must be > start")

        if not isinstance(self.text, str):
            raise TypeError("text must be a string")

        if not self.text.strip():
            raise ValueError("text must not be empty or whitespace")


@dataclass(slots=True)
class Subtitle:
    """Subtitle document."""

    language: str
    cues: list[SubtitleCue] = field(default_factory=list)

    def __post_init__(self) -> None:
        if not isinstance(self.language, str):
            raise TypeError("language must be a string")

        if not self.language.strip():
            raise ValueError("language must not be empty or whitespace")

        for previous, current in zip(self.cues, self.cues[1:]):
            if current.start < previous.start:
                raise ValueError("cues must be ordered by start time")
