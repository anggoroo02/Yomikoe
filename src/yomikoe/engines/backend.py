from enum import StrEnum

from yomikoe.engines.environment import detect_environment


class ComputeBackend(StrEnum):
    """Supported compute backends."""

    AUTO = "auto"
    CPU = "cpu"
    CUDA = "cuda"


def resolve_backend(
    requested: ComputeBackend = ComputeBackend.AUTO,
) -> ComputeBackend:
    """Resolve the compute backend from user preference and environment."""
    if requested is ComputeBackend.CPU:
        return ComputeBackend.CPU

    if requested is ComputeBackend.CUDA:
        return ComputeBackend.CUDA

    environment = detect_environment()

    if environment.has_cuda:
        return ComputeBackend.CUDA

    return ComputeBackend.CPU
