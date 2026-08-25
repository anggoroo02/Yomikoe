import math
from dataclasses import dataclass, field


@dataclass(slots=True, frozen=True)
class ComputeEnvironment:
    """Available compute capabilities detected from CTranslate2."""

    cuda_device_count: int
    supported_compute_types: frozenset[str]

    @property
    def has_cuda(self) -> bool:
        """Return True when at least one CUDA device is available."""
        return self.cuda_device_count > 0


@dataclass(slots=True)
class TranscriptionSegment:
    """A single transcription segment."""

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
class TranscriptionResult:
    """Result returned by a transcription engine."""

    language: str
    segments: list[TranscriptionSegment] = field(default_factory=list)

    def __post_init__(self) -> None:
        if not isinstance(self.language, str):
            raise TypeError("language must be a string")

        if not self.language.strip():
            raise ValueError("language must not be empty or whitespace")

        for previous, current in zip(self.segments, self.segments[1:]):
            if current.start < previous.start:
                raise ValueError("segments must be ordered by start time")


@dataclass(slots=True)
class TranscriptionProgress:
    """Represent transcription progress."""

    current_seconds: float
    total_seconds: float
