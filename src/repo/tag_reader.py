from pathlib import Path
from typing import Any, Protocol

from mediafile import MediaFile


class Reader(Protocol):
    def get(self, file: Path) -> dict[str, Any] | dict[str, str]:
        ...


class TagReader:
    def get(self, file: Path) -> dict[str, Any] | dict[str, str]:
        try:
            return MediaFile(file).as_dict()
        except Exception:
            return {
                "artist": "",
                "album": "",
                "title": "",
            }
