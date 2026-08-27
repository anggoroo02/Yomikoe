class EngineError(Exception):
    """Base exception for transcription engines."""


class EngineConfigurationError(EngineError):
    """Raised when an engine cannot be configured or initialized."""


class EngineTranscriptionError(EngineError):
    """Raised when transcription fails."""
