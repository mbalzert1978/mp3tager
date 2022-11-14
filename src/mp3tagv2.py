from datetime import datetime
import logging
import os
from pathlib import Path
import shutil
import string
import sys
import uuid
from mediafile import MediaFile
from ShazamAPI import Shazam

logging.basicConfig(
    filename=datetime.now().strftime("mp3tag_%H_%M_%d_%m_%Y.log"),
    encoding="utf-8",
    level=logging.INFO,
)

log = logging.getLogger(__name__)

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
NO_DIR = "Target directory does not exist, creating directory."
NO_MEDIA = "No media file, skipping, skipping file: %s"
NONE = "No tags, copied file: %s to folder: %s \t result: %s"
CREATE = "creating file: %s"


def mp3tag(root: Path, target: Path) -> None:
    for folder, _, files in os.walk(root):
        for file_name in files:
            source = Path(folder) / file_name
            ext = _extract_suffix(source)
            if source.suffix not in AUDIO_FILE_EXTENSIONS:
                log.info(NO_MEDIA, root)
                continue
            try:
                tag = MediaFile(source)
            except Exception:
                result = copy_to_unknown(source, target, ext)
                log.info(NONE, source, target, result)
            if not target.is_dir():
                log.info(NO_DIR)
                target.mkdir()
            if not all((tag.album, tag.title, tag.artist)):
                result = copy_to_unknown(source, target, ext)
                log.info(NONE, source, target, result)
            artist_directory = log_sanatize_mkdir(
                target, tag.artist if tag.artist else "unbekannt"
            )
            album_directory = log_sanatize_mkdir(
                artist_directory, tag.album if tag.album else "unbekannt"
            )
            file = _create_path_sanatize(album_directory, (tag.title,))
            file = file.with_suffix(ext)
            log.info(CREATE, file)
            _ = shutil.copy(source, file)


def log_sanatize_mkdir(target, tag) -> Path:
    folder = _create_path_sanatize(target, (tag,))
    if not folder.exists():
        log.info("creating folder: %s", folder)
        folder.mkdir()
    return folder


def copy_to_unknown(file: Path, target: Path, ext):
    return shutil.copy(
        src=file,
        dst=(target / "unbekannt" / str(uuid.uuid4())).with_suffix(ext),
    )


def shazam_it(root, tag):
    mp3_file_content_to_recognize = root.read_bytes()
    recognize_generator = Shazam(
        lang="de", timezone="Europe/Berlin", region="DE"
    ).recognize_song(mp3_file_content_to_recognize)
    _, resp = next(recognize_generator)
    if resp.get("matches"):
        tag.title = resp.get("track", {}).get("title")
        tag.artist = resp.get("track", {}).get("subtitle")
        tag.genre = resp.get("track", {}).get("genres", {}).get("primary")


def _extract_suffix(item: Path) -> str:
    return item.suffix


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


if __name__ == "__main__":
    try:
        *_, source, destination = sys.argv
    except ValueError:
        print("Source and destination directorys are needed.")
        sys.exit()
    mp3tag(root=Path(source), target=Path(destination))
