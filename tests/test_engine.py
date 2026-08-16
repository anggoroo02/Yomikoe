from collections.abc import Callable
from pathlib import Path
from unittest.mock import Mock, patch

import pytest

from yomikoe.audio import LoadedAudio
from yomikoe.engines import FasterWhisperEngine, TranscriptionProgress
from yomikoe.engines.backend import ComputeBackend


def test_faster_whisper_engine_initializes_model(
    tmp_path: Path,
) -> None:
    with patch("yomikoe.engines.faster_whisper.resolve_backend") as resolve_backend:
        resolve_backend.return_value = ComputeBackend.CPU

        with patch("yomikoe.engines.faster_whisper.WhisperModel") as whisper_model:
            FasterWhisperEngine(
                model_name="tiny",
                backend=ComputeBackend.CPU,
                compute_type="int8",
            )

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

    with patch(
        "yomikoe.engines.faster_whisper.resolve_backend",
        return_value=ComputeBackend.CPU,
    ):
        with patch(
            "yomikoe.engines.faster_whisper.WhisperModel",
            return_value=model,
        ):
            engine = FasterWhisperEngine(backend=ComputeBackend.CPU)

    audio = loaded_audio_factory()

    result = engine.transcribe(audio)

    model.transcribe.assert_called_once_with(str(audio["path"]))

    assert result.language == "ja"
    assert len(result.segments) == 2

    assert result.segments[0].start == 0.0
    assert result.segments[0].end == 1.5
    assert result.segments[0].text == "こんにちは"

    assert result.segments[1].start == 2.0
    assert result.segments[1].end == 3.5
    assert result.segments[1].text == "世界"


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

    progress_callback = Mock()

    with patch(
        "yomikoe.engines.faster_whisper.resolve_backend",
        return_value=ComputeBackend.CPU,
    ):
        with patch(
            "yomikoe.engines.faster_whisper.WhisperModel",
            return_value=model,
        ):
            engine = FasterWhisperEngine(backend=ComputeBackend.CPU)

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

    with patch(
        "yomikoe.engines.faster_whisper.resolve_backend",
        return_value=ComputeBackend.CUDA,
    ):
        with patch(
            "yomikoe.engines.faster_whisper.WhisperModel",
            side_effect=[first_model, second_model],
        ) as whisper_model:
            engine = FasterWhisperEngine(backend=ComputeBackend.AUTO)

            result = engine.transcribe(loaded_audio_factory())

    assert engine.backend is ComputeBackend.CPU
    assert result.language == "ja"
    assert result.segments[0].text == "こんにちは"

    assert whisper_model.call_count == 2
    assert whisper_model.call_args_list[0].kwargs == {
        "device": "cuda",
        "compute_type": "default",
    }
    assert whisper_model.call_args_list[1].kwargs == {
        "device": "cpu",
        "compute_type": "default",
    }


def test_faster_whisper_engine_does_not_fallback_for_explicit_backend(
    loaded_audio_factory: Callable[[float | None], LoadedAudio],
) -> None:
    model = Mock()
    model.transcribe.side_effect = RuntimeError("CUDA unavailable")

    with patch(
        "yomikoe.engines.faster_whisper.resolve_backend",
        return_value=ComputeBackend.CUDA,
    ):
        with patch(
            "yomikoe.engines.faster_whisper.WhisperModel",
            return_value=model,
        ):
            engine = FasterWhisperEngine(backend=ComputeBackend.CUDA)

            with pytest.raises(RuntimeError, match="CUDA unavailable"):
                engine.transcribe(loaded_audio_factory())


def test_faster_whisper_engine_does_not_fallback_when_auto_resolves_to_cpu(
    loaded_audio_factory: Callable[[float | None], LoadedAudio],
) -> None:
    model = Mock()
    model.transcribe.side_effect = RuntimeError("CPU transcription failed")

    with patch(
        "yomikoe.engines.faster_whisper.resolve_backend",
        return_value=ComputeBackend.CPU,
    ):
        with patch(
            "yomikoe.engines.faster_whisper.WhisperModel",
            return_value=model,
        ):
            engine = FasterWhisperEngine(backend=ComputeBackend.AUTO)

            with pytest.raises(
                RuntimeError,
                match="CPU transcription failed",
            ):
                engine.transcribe(loaded_audio_factory())

    assert engine.backend is ComputeBackend.CPU
    model.transcribe.assert_called_once()
