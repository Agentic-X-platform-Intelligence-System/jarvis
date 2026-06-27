"""Legacy root entry shim — delegates to apps.voice.main."""

from apps.voice.main import main

if __name__ == "__main__":
    raise SystemExit(main())
