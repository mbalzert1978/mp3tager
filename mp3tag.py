"""Modul for organizing mp3 files."""
import logging
import shutil
import string
import sys
import uuid
from pathlib import Path

import eyed3

logging.basicConfig(
    filename="mp3tagger.log",
    encoding="utf-8",
    level=logging.INFO,
)

log = logging.getLogger(__name__)


def mp3_tag(source: Path, destination: Path) -> None:
    """Search for .mp3 files in the `source` and saves them in the
    `destination`.

    The files are saved if possible as follows artist / album / title.mp3
    any missing information will be compensated with uuid's.
    """
    for item in source.iterdir():
        if item.is_dir():
            mp3_tag(item, destination)
        if item.is_file():
            __get_mp3_info_and_copy_with_new_filename(item, destination)


def __get_mp3_info_and_copy_with_new_filename(
    source: Path, destination: Path
) -> None:
    audio: eyed3.AudioFile = __get_audio_object(source)
    ext = __extract_suffix(source)
    if not audio:
        log.info("No audio File.")
        return
    if not audio.tag:
        log.error("No audio tag on mp3 file.")
        return
    artist_dir: Path = __create_path_from_artist(destination, audio)
    if not artist_dir.exists():
        log.info("creating folder: %s", artist_dir)
        artist_dir.mkdir()
    album_dir: Path = __create_path_from_album(artist_dir, audio)
    if not album_dir.exists():
        log.info("creating folder: %s", album_dir)
        album_dir.mkdir()
    file: Path = __create_path_from_title(album_dir, audio)
    file = file.with_suffix(ext)
    log.info("creating file: %s", file)
    _ = shutil.copy(source, file)


def __sanatize(input: str) -> str:
    return "".join(
        letter
        for letter in input
        if letter
        in (
            letter
            for letter in (
                string.ascii_lowercase
                + string.ascii_uppercase
                + string.digits
                + " "
                + "-"
            )
        )
    ).strip()


def __create_path_from_artist(root: Path, audio: eyed3.AudioFile) -> Path:
    if audio.tag.artist:
        value = audio.tag.artist
    elif audio.tag.album:
        log.error("No artist => taking album")
        value = audio.tag.album
    elif audio.tag.title:
        log.error("No album => taking title")
        value = audio.tag.title
    else:
        log.error("Nothing to get generate uuid.")
        value = str(uuid.uuid4())
    return root / __sanatize(value)


def __create_path_from_album(root: Path, audio: eyed3.AudioFile) -> Path:
    if audio.tag.album:
        value = audio.tag.album
    elif audio.tag.artist:
        log.error("No album => taking artist")
        value = audio.tag.artist
    elif audio.tag.title:
        log.error("No artist => taking title")
        value = audio.tag.title
    else:
        log.error("Nothing to get generate uuid.")
        value = str(uuid.uuid4())
    return root / __sanatize(value)


def __create_path_from_title(root: Path, audio: eyed3.AudioFile) -> Path:
    if audio.tag.title:
        value = audio.tag.title
    elif audio.tag.artist:
        log.error("No title => taking artist")
        value = audio.tag.artist
    elif audio.tag.album:
        log.error("No artist => taking album")
        value = audio.tag.album
    else:
        log.error("Nothing to get generate uuid.")
        value = str(uuid.uuid4())
    return root / __sanatize(value)


def __extract_suffix(item: Path) -> str:
    return item.suffix


def __get_audio_object(item) -> eyed3.AudioFile | None:
    return eyed3.load(item)


if __name__ == "__main__":
    try:
        _, source, destination = sys.argv
    except ValueError:
        print("Source and destination directorys are needed.")
        sys.exit()
    mp3_tag(source=Path(source), destination=Path(destination))
