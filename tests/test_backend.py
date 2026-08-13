from unittest.mock import patch

from yomikoe.engines.backend import ComputeBackend, resolve_backend
from yomikoe.engines.models import ComputeEnvironment


def test_resolve_backend_cpu() -> None:
    assert resolve_backend(ComputeBackend.CPU) is ComputeBackend.CPU


def test_resolve_backend_cuda() -> None:
    assert resolve_backend(ComputeBackend.CUDA) is ComputeBackend.CUDA


def test_resolve_backend_auto_with_cuda() -> None:
    environment = ComputeEnvironment(
        cuda_device_count=1,
        supported_compute_types=frozenset({"float16"}),
    )

    with patch(
        "yomikoe.engines.backend.detect_environment",
        return_value=environment,
    ):
        assert resolve_backend() is ComputeBackend.CUDA


def test_resolve_backend_auto_without_cuda() -> None:
    environment = ComputeEnvironment(
        cuda_device_count=0,
        supported_compute_types=frozenset(),
    )

    with patch(
        "yomikoe.engines.backend.detect_environment",
        return_value=environment,
    ):
        assert resolve_backend() is ComputeBackend.CPU
