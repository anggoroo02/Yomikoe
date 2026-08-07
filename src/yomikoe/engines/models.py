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


@dataclass(slots=True)
class TranscriptionResult:
    """Result returned by a transcription engine."""

    language: str
    segments: list[TranscriptionSegment] = field(default_factory=list)
