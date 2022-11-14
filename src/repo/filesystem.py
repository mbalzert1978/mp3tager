import os
import shutil
from pathlib import Path
from typing import Generator, Protocol


class File(Protocol):
    def read(self, root: Path) -> Generator[Path, None, None]:
        ...

    def copy(self, root: Path, dest: Path) -> None:
        ...


class FileSystem:
    def read(self, root: Path) -> Generator[Path, None, None]:
        for folder, _, files in os.walk(root):
            for file_name in files:
                yield Path(folder) / file_name

    def copy(self, root: Path, dest: Path) -> None:
        shutil.copy(root, dest)
