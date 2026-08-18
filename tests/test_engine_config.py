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
