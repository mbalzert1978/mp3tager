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


def mp3_tag(root: Path, target: Path) -> None:
    """Search for .mp3 files in the `source` and saves them in the
    `destination`.

    The files are saved if possible as follows artist / album / title.mp3
    any missing information will be compensated with uuid's.
    """
    for item in root.iterdir():
        if item.is_dir():
            mp3_tag(item, target)
        if item.is_file():
            _get_mp3_info_and_copy_with_new_filename(item, target)


def _get_mp3_info_and_copy_with_new_filename(root: Path, target: Path) -> None:
    audio: eyed3.AudioFile = _get_audio_object(root)
    ext = _extract_suffix(root)
    if not audio:
        log.info("No audio file, skipping.")
        return
    if not audio.tag:
        log.error("No mp3 tag info, skipping.")
        return
    if not target.is_dir():
        log.info("Target folder does not exist, creating folder.")
        target.mkdir()
    artist_dir = _create_path_sanatize(
        target, (audio.tag.artist, audio.tag.album, audio.tag.title)
    )
    if not artist_dir.exists():
        log.info("creating folder: %s", artist_dir)
        artist_dir.mkdir()
    album_dir = _create_path_sanatize(
        artist_dir, (audio.tag.album, audio.tag.artist, audio.tag.title)
    )
    if not album_dir.exists():
        log.info("creating folder: %s", album_dir)
        album_dir.mkdir()
    file = _create_path_sanatize(
        album_dir, (audio.tag.title, audio.tag.artist, audio.tag.album)
    )
    file = file.with_suffix(ext)
    log.info("creating file: %s", file)
    _ = shutil.copy(root, file)


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
            )
        )
    ).strip()


def _create_path_sanatize(root: Path, tags: tuple[str | None, ...]) -> Path:
    for tag in tags:
        if not tag:
            continue
        return root / _sanatize(tag)
    log.error("No valid tag info, generating uuid string.")
    uuid_str = str(uuid.uuid4())
    return root / _sanatize(uuid_str)


def _extract_suffix(item: Path) -> str:
    return item.suffix


def _get_audio_object(item) -> eyed3.AudioFile | None:
    return eyed3.load(item)


if __name__ == "__main__":
    try:
        *_, source, destination = sys.argv
    except ValueError:
        print("Source and destination directorys are needed.")
        sys.exit()
    mp3_tag(root=Path(source), target=Path(destination))
