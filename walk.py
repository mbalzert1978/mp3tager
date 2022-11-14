import os
import shutil
import sys
from pathlib import Path

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


def get_media_files(source):
    # Walk the source folder and build a dict of filenames and their hashes
    media_files = {}
    for folder, _, files in os.walk(source):
        for fn in files:
            file: Path = Path(folder) / fn
            if file.suffix in AUDIO_FILE_EXTENSIONS:
                media_files[file] = fn
    return media_files


def main(root: str, target: str):
    media_files = get_media_files(root)
    for k, _ in media_files.items():
        result = MediaFile(k)
        # prüfen ob result album artist und titel hat
        if not any((result.album, result.title, result.artist)):
            mp3_file_content_to_recognize = k.read_bytes()
            recognize_generator = Shazam(
                lang="de", timezone="Europe/Berlin", region="DE"
            ).recognize_song(mp3_file_content_to_recognize)
        tag_info = result.as_dict()
        target_file: Path = (
            Path(target).resolve()
            / tag_info.get("artist")
            / tag_info.get("album")
            / tag_info.get("title")
        )
        result = shutil.copy(k, target_file)
        target_file = target_file.with_suffix(k.suffix)
        target_file.touch()
        result = MediaFile(target_file)
        result.save(**tag_info)

        print()


if __name__ == "__main__":
    _, root, target = sys.argv
    main(root, target)
