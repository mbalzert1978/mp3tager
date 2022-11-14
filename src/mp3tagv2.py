from collections import namedtuple
import os
from pathlib import Path
import shutil
import string
import sys
from typing import Generator
import uuid
from mediafile import MediaFile
from ShazamAPI import Shazam


AUDIO_FILE_EXTENSIONS = [
    ".asf",
    ".wma",
    ".wmv",
    ".wm",
    ".mpg",
    ".mpeg",
    ".m1v",
    ".mp2",
    ".mp3",
    ".mpa",
    ".mpe",
    ".wav",
    ".m4a",
    ".flac",
    ".ogg",
]


class FileSystem:
    def read(self, root: Path) -> Generator[Path, None, None]:
        for folder, _, files in os.walk(root):
            for file_name in files:
                yield Path(folder) / file_name

    def copy(self, root: Path, dest: Path) -> None:
        shutil.copy(root, dest)


empty_tags = namedtuple("empty_tags", ["artist", "album", "title"])


def ref_mp3tag(
    source_folder: Path, target: Path, file_system: FileSystem = FileSystem()
) -> None:
    files = file_system.read(source_folder)
    for file in files:
        ext = file.suffix
        if ext not in AUDIO_FILE_EXTENSIONS:
            continue
        try:
            tags = MediaFile(file).as_dict()
        except Exception:
            tags = {
                "artist": "",
                "album": "",
                "title": "",
            }
        destination = create_folder_from_tag(target, ext, tags)
        file_system.copy(file, destination)


def create_folder_from_tag(target: Path, ext: str, tags: dict) -> Path:
    artist = _sanatize(tags.get("artist") or "unkown_artist")
    album = _sanatize(tags.get("album") or "unknown_album")
    title = _sanatize(tags.get("title") or str(uuid.uuid4()))
    dest: Path = Path(target) / artist / album / title
    try:
        dest.parent.mkdir(parents=True, exist_ok=False)
    except FileExistsError:
        pass
    dest = dest.with_suffix(ext)
    return dest


def shazam_it(root, tag) -> None:
    mp3_file_content_to_recognize = root.read_bytes()
    recognize_generator = Shazam(
        lang="de", timezone="Europe/Berlin", region="DE"
    ).recognize_song(mp3_file_content_to_recognize)
    _, resp = next(recognize_generator)
    if resp.get("matches"):
        tag.title = resp.get("track", {}).get("title")
        tag.artist = resp.get("track", {}).get("subtitle")
        tag.genre = resp.get("track", {}).get("genres", {}).get("primary")


def _sanatize(value: str) -> str:
    return "".join(
        letter
        for letter in value
        if letter
        in (
            letter
            for letter in (
                string.ascii_lowercase
                + string.ascii_uppercase
                + string.digits
                + " "
                + "-"
                + "_"
            )
        )
    ).strip()


if __name__ == "__main__":
    try:
        *_, source, target_folder = sys.argv
    except ValueError:
        print("Source and destination directorys are needed.")
        sys.exit()
    ref_mp3tag(source_folder=Path(source), target=Path(target_folder))
