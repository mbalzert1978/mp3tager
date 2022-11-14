import os
from pathlib import Path

from .media_file import MediaFileRepo

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


def read_paths(root, filesystem: MediaFileRepo = MediaFileRepo()):
    media_files = {}
    for folder, _, files in os.walk(root):
        for file_name in files:
            file_path: Path = Path(folder) / file_name
            if file_path.suffix in AUDIO_FILE_EXTENSIONS:
                media_files[file_path] = filesystem.load(file_path)
    return media_files


def determine_actions(source_hashes, dest_hashes, source_folder, dest_folder):
    for sha, filename in source_hashes.items():
        if sha not in dest_hashes:
            sourcepath = Path(source_folder) / filename
            destpath = Path(dest_folder) / filename
            yield "COPY", sourcepath, destpath

        elif dest_hashes[sha] != filename:
            olddestpath = Path(dest_folder) / dest_hashes[sha]
            newdestpath = Path(dest_folder) / filename
            yield "MOVE", olddestpath, newdestpath

    for sha, filename in dest_hashes.items():
        if sha not in source_hashes:
            yield "DELETE", dest_folder / filename
