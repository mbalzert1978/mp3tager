import os
import shutil
from pathlib import Path


class MediaTagFileSystem:
    AUDIO_FILE_EXTENSIONS = (
        ".alac",
        ".m4a",
        ".aac",
        ".ape",
        ".mp3",
        ".mp4",
        ".wav",
        ".flac",
        ".ogg",
        ".opus",
        ".wv",
        ".mpc",
        ".asf",
        ".aiff",
        ".dsf",
    )

    def get(self, root: Path) -> list[Path]:
        path_objects = []
        for folder, _, files in os.walk(root):
            path_objects.extend(
                Path(folder) / file_name
                for file_name in files
                if file_name.endswith(self.AUDIO_FILE_EXTENSIONS)
            )
        return path_objects

    def copy(self, root: Path, dest: Path) -> None:
        shutil.copy(root, dest)

    def mkdir(self, dest: Path) -> None:
        dest.parent.mkdir(parents=True, exist_ok=True)

    def mkpath(self, target: Path, folders: tuple[str, ...]) -> Path:
        return target.joinpath(*folders)
