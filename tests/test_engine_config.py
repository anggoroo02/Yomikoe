from dataclasses import FrozenInstanceError

import pytest

from yomikoe.engines.backend import ComputeBackend
from yomikoe.engines.config import TranscriptionConfig


def test_transcription_config_uses_defaults() -> None:
    config = TranscriptionConfig()

    assert config.model == "small"
    assert config.language == "ja"
    assert config.backend is ComputeBackend.AUTO
    assert config.compute_type == "default"


def test_transcription_config_accepts_custom_values() -> None:
    config = TranscriptionConfig(
        model="medium",
        language="en",
        backend=ComputeBackend.CUDA,
        compute_type="float16",
    )

    assert config.model == "medium"
    assert config.language == "en"
    assert config.backend is ComputeBackend.CUDA
    assert config.compute_type == "float16"


def test_transcription_config_is_immutable() -> None:
    config = TranscriptionConfig()

    with pytest.raises(FrozenInstanceError):
        config.language = "en"


@pytest.mark.parametrize("model", ["", " ", "\t", "\n"])
def test_config_rejects_empty_model(model: str) -> None:
    with pytest.raises(ValueError, match="model must not be empty or whitespace"):
        TranscriptionConfig(model=model)


@pytest.mark.parametrize("model", [None, 123, object()])
def test_config_rejects_non_string_model(model: object) -> None:
    with pytest.raises(TypeError, match="model must be a string"):
        TranscriptionConfig(model=model)  # type: ignore[arg-type]


@pytest.mark.parametrize("language", ["", " ", "\t", "\n"])
def test_config_rejects_empty_language(language: str) -> None:
    with pytest.raises(ValueError, match="language must not be empty or whitespace"):
        TranscriptionConfig(language=language)


@pytest.mark.parametrize("language", [None, 123, object()])
def test_config_rejects_non_string_language(language: object) -> None:
    with pytest.raises(TypeError, match="language must be a string"):
        TranscriptionConfig(language=language)  # type: ignore[arg-type]


@pytest.mark.parametrize("backend", ["auto", "cpu", "cuda", None, 123])
def test_config_rejects_invalid_backend(backend: object) -> None:
    with pytest.raises(TypeError, match="backend must be a ComputeBackend"):
        TranscriptionConfig(backend=backend)  # type: ignore[arg-type]


@pytest.mark.parametrize("compute_type", ["", " ", "\t", "\n"])
def test_config_rejects_empty_compute_type(compute_type: str) -> None:
    with pytest.raises(
        ValueError,
        match="compute_type must not be empty or whitespace",
    ):
        TranscriptionConfig(compute_type=compute_type)


@pytest.mark.parametrize("compute_type", [None, 123, object()])
def test_config_rejects_non_string_compute_type(compute_type: object) -> None:
    with pytest.raises(TypeError, match="compute_type must be a string"):
        TranscriptionConfig(compute_type=compute_type)  # type: ignore[arg-type]
