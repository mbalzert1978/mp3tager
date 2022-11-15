import sys
import uuid
from pathlib import Path

from src.filesystem.base import FileSystem
from src.filesystem.mp3_tag_filesystem import MediaTagFileSystem
from src.reader.base import Reader
from src.reader.tag_reader import TagReader

from .src.utilities.string import sanatize


def ref_mp3tag(
    source_folder: Path,
    destination_folder: Path,
    file_system: FileSystem = MediaTagFileSystem(),
    reader: Reader = TagReader(),
) -> None:
    files = file_system.get(source_folder)
    for file in files:
        ext = file.suffix
        tags = reader.read(file)
        artist = sanatize(tags.get("artist", "unkown_artist"))
        album = sanatize(tags.get("album", "unknown_album"))
        title = sanatize(tags.get("title", str(uuid.uuid4())))
        path = file_system.mkpath(destination_folder, (artist, album, title))
        file_system.mkdir(path)
        path = path.with_suffix(ext)
        file_system.copy(file, path)


if __name__ == "__main__":
    try:
        *_, source, target_folder = sys.argv
    except ValueError:
        print("Source and destination directorys are needed.")
        sys.exit()
    ref_mp3tag(
        source_folder=Path(source), destination_folder=Path(target_folder)
    )
