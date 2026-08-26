"""Post-processing utilities for transcription results."""

from .identity import IdentityTranscriptionProcessor
from .interface import TranscriptionProcessor

__all__ = ["TranscriptionProcessor", "IdentityTranscriptionProcessor"]
