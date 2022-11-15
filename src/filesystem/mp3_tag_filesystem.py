import os
import shutil
from pathlib import Path
from typing import Generator


class MediaTagFileSystem:
    AUDIO_FILE_EXTENSIONS = (
        ".asf",
        ".wma",
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
    )

    def get(self, root: Path) -> Generator[Path, None, None]:
        for folder, _, files in os.walk(root):
            for file_name in files:
                if not file_name.endswith(self.AUDIO_FILE_EXTENSIONS):
                    continue
                yield Path(folder) / file_name

    def copy(self, root: Path, dest: Path) -> None:
        shutil.copy(root, dest)

    def mkdir(self, dest: Path) -> None:
        dest.parent.mkdir(parents=True, exist_ok=True)

    def mkpath(self, target: Path, folders: tuple[str, ...]) -> Path:
        for folder in folders:
            target /= folder
        return target
