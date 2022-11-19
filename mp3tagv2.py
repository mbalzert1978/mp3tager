import sys
from pathlib import Path

from src.filesystem.base import FileSystem
from src.filesystem.media import MediaTagFileSystem
from src.reader.base import Reader
from src.reader.reader import (
    ACRCloudReader,
    AudDReader,
    MultiReader,
    TagReader,
)


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


if __name__ == "__main__":
    try:
        *_, source, target_folder = sys.argv
    except ValueError:
        print("Source and destination directorys are needed.")
        sys.exit()
    mp3tag(source_folder=Path(source), destination_folder=Path(target_folder))
