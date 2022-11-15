from pathlib import Path
from typing import Generator, Protocol


class FileSystem(Protocol):
    """Manipulate the filesystem."""

    def get(self, root: Path) -> Generator[Path, None, None]:
        ...

    def copy(self, root: Path, dest: Path) -> None:
        ...

    def mkdir(self, dest: Path) -> None:
        ...

    def mkpath(self, root: Path, folders: tuple[str, ...]) -> Path:
        ...
