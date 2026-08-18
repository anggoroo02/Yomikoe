from dataclasses import dataclass

from yomikoe.engines.backend import ComputeBackend


@dataclass(frozen=True, slots=True)
class TranscriptionConfig:
    model: str = "small"
    language: str = "ja"
    backend: ComputeBackend = ComputeBackend.AUTO
    compute_type: str = "default"
