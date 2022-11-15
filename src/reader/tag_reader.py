from pathlib import Path

from mediafile import MediaFile


class TagReader:
    def read(self, file: Path) -> dict | dict[str, str]:
        try:
            return MediaFile(file).as_dict()
        except Exception:
            return {}
