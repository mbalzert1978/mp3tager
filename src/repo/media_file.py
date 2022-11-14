from pathlib import Path
from typing import Any, Protocol

from mediafile import MediaFile


class FileRepo(Protocol):
    def load(self, file: Path) -> dict[str, Any] | None:
        ...

    def save(self, filename: str, tags: dict[str, Any]) -> None:
        ...


class MediaFileFake:
    def load(self, file: Path) -> dict[str, Any] | None:
        return {
            "album": "test_album",
            "title": "test_title",
            "artist": "test_artist",
        }

    def save(self, filename: str, tags: dict[str, Any]) -> None:
        ...


class MediaFileRepo:
    def load(self, file: Path) -> dict[str, Any] | None:
        try:
            result = MediaFile(file)
            return result.as_dict()
        except Exception:
            return {
                "album": "",
                "title": "",
                "artist": "",
            }

    def save(self, filename: str, tags: dict[str, Any]) -> None:
        self.media_file.save(**tags)

    def _get_result(self) -> None:
        id3v23 = False
        while 1:
            self.media_file = MediaFile(self.file, id3v23=id3v23)
            if not any(
                (
                    self.media_file.album,
                    self.media_file.title,
                    self.media_file.artist,
                )
            ):
                if not id3v23:
                    id3v23 = True
                    continue
                break
