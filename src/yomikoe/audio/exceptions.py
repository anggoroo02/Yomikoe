class AudioError(Exception):
    """Base exception for audio errors."""


class UnsupportedAudioFormatError(AudioError):
    """Raised when audio format is not supported."""


class AudioLoadError(AudioError):
    """Raised when audio cannot be loaded."""