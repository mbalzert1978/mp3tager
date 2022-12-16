import re
import sys
from pathlib import Path

from src.filesystem.base import FileSystem
from src.filesystem.media import MediaTagFileSystem
from src.models.tag_enum import Tags
from src.reader.base import Reader
from src.reader.reader import (
    ACRCloudReader,
    AudDReader,
    ShazamIOReader,
    TagReader,
)
from src.utilities.sequnce import fetch_one

UUID4 = re.compile(r"[\w\d]{8}-[\w\d]{4}-[\w\d]{4}-[\w\d]{4}-[\w\d]{12}")


def mp3tag(
    source_folder: Path,
    destination_folder: Path,
    file_system: FileSystem = MediaTagFileSystem(),
    reader: Reader = TagReader(),
) -> None:
    files = file_system.get(source_folder)
    for file in files:
        ext = file.suffix
        tags = reader.read(file).get_tags()
        path = file_system.mkpath(
            destination_folder,
            (tags.get("artist"), tags.get("album"), tags.get("title")),
        )
        file_system.mkdir(path)
        path = path.with_suffix(ext)
        file_system.copy(file, path)


def multi_mp3tag(
    source_folder: Path,
    destination_folder: Path,
    file_system: FileSystem = MediaTagFileSystem(),
    readers: tuple[Reader] = (TagReader(), ACRCloudReader()),
) -> None:
    files = file_system.get(source_folder)
    for file in files:
        ext = file.suffix
        tags = {}
        for reader in readers:
            artist = tags.get("artist")
            if not artist or artist == "unknown_artist":
                artist = reader.read(file_path=file).get_artist()
                tags["artist"] = artist
            album = tags.get("album")
            if not album or album == "unknown_album":
                album = reader.read(file_path=file).get_album()
                tags["album"] = album
            title = tags.get("title")
            if not title or UUID4.match(title):
                title = reader.read(file_path=file).get_title()
                tags["title"] = title
        path = file_system.mkpath(
            destination_folder,
            (tags.get("artist"), tags.get("album"), tags.get("title")),
        )
        file_system.mkdir(path)
        path = path.with_suffix(ext)
        file_system.copy(file, path)


class Mp3Tag:
    def __init__(self, source_folder: Path, destination_folder: Path) -> None:
        self.source = source_folder
        self.destination = destination_folder
        self.filesystem = MediaTagFileSystem()
        self.reader = TagReader()
        self.readers = (TagReader(), ACRCloudReader(), AudDReader())
        self.artist = ""
        self.album = ""
        self.title = ""

    def tag_media_files(self) -> None:
        files = self.filesystem.get(self.source)
        for file in files:
            ext = file.suffix
            for reader in self.readers:
                if not self.artist or self.artist == str(Tags.ARTIST):
                    self.artist = reader.read(file_path=file).get_artist()
                if not self.album or self.album == str(Tags.ALBUM):
                    self.album = reader.read(file_path=file).get_album()
                if not self.title or UUID4.match(self.title):
                    self.title = reader.read(file_path=file).get_title()
            path = self.filesystem.mkpath(
                self.destination, (self.artist, self.album, self.title)
            )
            self.filesystem.mkdir(path)
            path = path.with_suffix(ext)
            self.filesystem.copy(file, path)
            self.artist = ""
            self.album = ""
            self.title = ""

    def get_tags(
        self, file: Path, reader: Reader = TagReader()
    ) -> dict[str, str]:
        file = fetch_one(self.filesystem.get(file))
        return reader.read(file)


if __name__ == "__main__":
    try:
        *_, source, target_folder = sys.argv
    except ValueError:
        print("Source and destination directorys are needed.")
        sys.exit()
    tag = Mp3Tag(
        source_folder=Path(source), destination_folder=Path(target_folder)
    )
    tag.tag_media_files()
