"""Legacy core.wake_word shim — re-exports from aura.wake_word."""

from aura.wake_word import WakeWordError, WakeWordListener

__all__ = ["WakeWordError", "WakeWordListener"]
