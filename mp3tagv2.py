import sys
from pathlib import Path

from src.filesystem.base import FileSystem
from src.filesystem.mp3_tag_filesystem import MediaTagFileSystem
from src.reader.base import Reader
from src.reader.reader import AudDReader, MultiReader, TagReader
from src.utilities.string import sanatize


def mp3tag(
    source_folder: Path,
    destination_folder: Path,
    file_system: FileSystem = MediaTagFileSystem(),
    reader: Reader = MultiReader((TagReader(), AudDReader())),
) -> None:
    files = file_system.get(source_folder)
    for file in files:
        ext = file.suffix
        tags = reader.read(file)
        artist = sanatize(tags.get("artist"))
        album = sanatize(tags.get("album"))
        title = sanatize(tags.get("title"))
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
    mp3tag(source_folder=Path(source), destination_folder=Path(target_folder))
