from dataclasses import dataclass

from yomikoe.engines.backend import ComputeBackend


@dataclass(frozen=True, slots=True)
class TranscriptionConfig:
    """Configuration for a transcription engine."""

    model: str = "small"
    language: str = "ja"
    backend: ComputeBackend = ComputeBackend.AUTO
    compute_type: str = "default"

    def __post_init__(self) -> None:
        if not isinstance(self.model, str):
            raise TypeError("model must be a string")

        if not self.model.strip():
            raise ValueError("model must not be empty or whitespace")

        if not isinstance(self.language, str):
            raise TypeError("language must be a string")

        if not self.language.strip():
            raise ValueError("language must not be empty or whitespace")

        if not isinstance(self.backend, ComputeBackend):
            raise TypeError("backend must be a ComputeBackend")

        if not isinstance(self.compute_type, str):
            raise TypeError("compute_type must be a string")

        if not self.compute_type.strip():
            raise ValueError("compute_type must not be empty or whitespace")
