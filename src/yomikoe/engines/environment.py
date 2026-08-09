from yomikoe.engines.models import ComputeEnvironment

import ctranslate2


def detect_environment() -> ComputeEnvironment:
    """Inspect available compute capabilities."""

    try:
        cuda_device_count = ctranslate2.get_cuda_device_count()

        supported_compute_types = (
            frozenset(ctranslate2.get_supported_compute_types("cuda"))
            if cuda_device_count > 0
            else frozenset()
        )

    except Exception:
        cuda_device_count = 0
        supported_compute_types = frozenset()

    return ComputeEnvironment(
        cuda_device_count=cuda_device_count,
        supported_compute_types=supported_compute_types,
    )