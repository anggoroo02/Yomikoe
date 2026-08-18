from collections.abc import Callable
from pathlib import Path
from unittest.mock import Mock, patch

import pytest

from yomikoe.audio import LoadedAudio
from yomikoe.engines import FasterWhisperEngine, TranscriptionProgress
from yomikoe.engines.backend import ComputeBackend
from yomikoe.engines.config import TranscriptionConfig


def test_faster_whisper_engine_initializes_model(
    tmp_path: Path,
) -> None:
    config = TranscriptionConfig(
        model="tiny",
        backend=ComputeBackend.CPU,
        compute_type="int8",
        language="en",
    )

    with patch("yomikoe.engines.faster_whisper.resolve_backend") as resolve_backend:
        resolve_backend.return_value = ComputeBackend.CPU

        with patch("yomikoe.engines.faster_whisper.WhisperModel") as whisper_model:
            FasterWhisperEngine(config=config)

            resolve_backend.assert_called_once_with(ComputeBackend.CPU)
            whisper_model.assert_called_once_with(
                "tiny",
                device="cpu",
                compute_type="int8",
            )


def test_faster_whisper_engine_maps_transcription_result(
    loaded_audio_factory: Callable[[float | None], LoadedAudio],
) -> None:
    segments = [
        Mock(start=0.0, end=1.5, text="  こんにちは  "),
        Mock(start=2.0, end=3.5, text=" 世界 "),
    ]
    info = Mock(language="ja")

    model = Mock()
    model.transcribe.return_value = (segments, info)

    config = TranscriptionConfig(
        backend=ComputeBackend.CPU,
    )

    with patch(
        "yomikoe.engines.faster_whisper.resolve_backend",
        return_value=ComputeBackend.CPU,
    ):
        with patch(
            "yomikoe.engines.faster_whisper.WhisperModel",
            return_value=model,
        ):
            engine = FasterWhisperEngine(config=config)

    audio = loaded_audio_factory()

    result = engine.transcribe(audio)

    model.transcribe.assert_called_once_with(
        str(audio["path"]),
        language="ja",
    )

    assert result.language == "ja"
    assert len(result.segments) == 2

    assert result.segments[0].start == 0.0
    assert result.segments[0].end == 1.5
    assert result.segments[0].text == "こんにちは"

    assert result.segments[1].start == 2.0
    assert result.segments[1].end == 3.5
    assert result.segments[1].text == "世界"


def test_faster_whisper_engine_uses_explicit_language(
    loaded_audio_factory: Callable[[float | None], LoadedAudio],
) -> None:
    segments = [
        Mock(start=0.0, end=1.5, text=" Hello "),
    ]
    info = Mock(language="en")

    model = Mock()
    model.transcribe.return_value = (segments, info)

    config = TranscriptionConfig(
        backend=ComputeBackend.CPU,
        language="en",
    )

    with patch(
        "yomikoe.engines.faster_whisper.resolve_backend",
        return_value=ComputeBackend.CPU,
    ):
        with patch(
            "yomikoe.engines.faster_whisper.WhisperModel",
            return_value=model,
        ):
            engine = FasterWhisperEngine(config=config)

    audio = loaded_audio_factory()

    result = engine.transcribe(audio)

    model.transcribe.assert_called_once_with(
        str(audio["path"]),
        language="en",
    )

    assert result.language == "en"


def test_faster_whisper_engine_reports_progress(
    loaded_audio_factory: Callable[[float | None], LoadedAudio],
) -> None:
    segments = [
        Mock(start=0.0, end=1.5, text="こんにちは"),
        Mock(start=2.0, end=4.0, text="世界"),
    ]
    info = Mock(language="ja")

    model = Mock()
    model.transcribe.return_value = (segments, info)

    config = TranscriptionConfig(
        backend=ComputeBackend.CPU,
    )

    progress_callback = Mock()

    with patch(
        "yomikoe.engines.faster_whisper.resolve_backend",
        return_value=ComputeBackend.CPU,
    ):
        with patch(
            "yomikoe.engines.faster_whisper.WhisperModel",
            return_value=model,
        ):
            engine = FasterWhisperEngine(config=config)

    engine.transcribe(
        loaded_audio_factory(10.0),
        progress_callback=progress_callback,
    )

    assert progress_callback.call_count == 2

    progress_callback.assert_any_call(
        TranscriptionProgress(
            current_seconds=1.5,
            total_seconds=10.0,
        )
    )
    progress_callback.assert_any_call(
        TranscriptionProgress(
            current_seconds=4.0,
            total_seconds=10.0,
        )
    )


def test_faster_whisper_engine_falls_back_to_cpu_on_auto_backend_error(
    loaded_audio_factory: Callable[[float | None], LoadedAudio],
) -> None:
    segments = [
        Mock(start=0.0, end=1.0, text="こんにちは"),
    ]
    info = Mock(language="ja")

    first_model = Mock()
    first_model.transcribe.side_effect = RuntimeError("CUDA unavailable")

    second_model = Mock()
    second_model.transcribe.return_value = (segments, info)

    config = TranscriptionConfig(
        model="medium",
        language="ja",
        backend=ComputeBackend.AUTO,
        compute_type="float16",
    )

    with patch(
        "yomikoe.engines.faster_whisper.resolve_backend",
        return_value=ComputeBackend.CUDA,
    ):
        with patch(
            "yomikoe.engines.faster_whisper.WhisperModel",
            side_effect=[first_model, second_model],
        ) as whisper_model:
            engine = FasterWhisperEngine(config=config)

            result = engine.transcribe(loaded_audio_factory())

    assert engine.backend is ComputeBackend.CPU
    assert result.language == "ja"
    assert result.segments[0].text == "こんにちは"

    assert whisper_model.call_count == 2
    assert whisper_model.call_args_list[0].args == ("medium",)
    assert whisper_model.call_args_list[0].kwargs == {
        "device": "cuda",
        "compute_type": "float16",
    }
    assert whisper_model.call_args_list[1].args == ("medium",)
    assert whisper_model.call_args_list[1].kwargs == {
        "device": "cpu",
        "compute_type": "float16",
    }

    first_model.transcribe.assert_called_once_with(
        str(loaded_audio_factory()["path"]),
        language="ja",
    )


def test_faster_whisper_engine_does_not_fallback_for_explicit_backend(
    loaded_audio_factory: Callable[[float | None], LoadedAudio],
) -> None:
    model = Mock()
    model.transcribe.side_effect = RuntimeError("CUDA unavailable")

    config = TranscriptionConfig(
        backend=ComputeBackend.CUDA,
    )

    with patch(
        "yomikoe.engines.faster_whisper.resolve_backend",
        return_value=ComputeBackend.CUDA,
    ):
        with patch(
            "yomikoe.engines.faster_whisper.WhisperModel",
            return_value=model,
        ):
            engine = FasterWhisperEngine(config=config)

            with pytest.raises(RuntimeError, match="CUDA unavailable"):
                engine.transcribe(loaded_audio_factory())

    assert engine.backend is ComputeBackend.CUDA


def test_faster_whisper_engine_does_not_fallback_when_auto_resolves_to_cpu(
    loaded_audio_factory: Callable[[float | None], LoadedAudio],
) -> None:
    model = Mock()
    model.transcribe.side_effect = RuntimeError("CPU transcription failed")

    config = TranscriptionConfig(
        backend=ComputeBackend.AUTO,
    )

    with patch(
        "yomikoe.engines.faster_whisper.resolve_backend",
        return_value=ComputeBackend.CPU,
    ):
        with patch(
            "yomikoe.engines.faster_whisper.WhisperModel",
            return_value=model,
        ):
            engine = FasterWhisperEngine(config=config)

            with pytest.raises(
                RuntimeError,
                match="CPU transcription failed",
            ):
                engine.transcribe(loaded_audio_factory())

    assert engine.backend is ComputeBackend.CPU
    model.transcribe.assert_called_once()
