from unittest.mock import patch

from yomikoe.engines.environment import detect_environment


def test_detect_environment_with_cuda() -> None:
    with (
        patch(
            "yomikoe.engines.environment.ctranslate2.get_cuda_device_count",
            return_value=1,
        ),
        patch(
            "yomikoe.engines.environment.ctranslate2.get_supported_compute_types",
            return_value=["float16", "float32"],
        ),
    ):
        environment = detect_environment()

    assert environment.cuda_device_count == 1
    assert environment.supported_compute_types == frozenset({"float16", "float32"})
    assert environment.has_cuda is True


def test_detect_environment_without_cuda() -> None:
    with patch(
        "yomikoe.engines.environment.ctranslate2.get_cuda_device_count",
        return_value=0,
    ):
        environment = detect_environment()

    assert environment.cuda_device_count == 0
    assert environment.supported_compute_types == frozenset()
    assert environment.has_cuda is False


def test_detect_environment_handles_detection_error() -> None:
    with patch(
        "yomikoe.engines.environment.ctranslate2.get_cuda_device_count",
        side_effect=RuntimeError("CUDA unavailable"),
    ):
        environment = detect_environment()

    assert environment.cuda_device_count == 0
    assert environment.supported_compute_types == frozenset()

    assert environment.has_cuda is False
