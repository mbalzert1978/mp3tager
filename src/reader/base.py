from pathlib import Path
from typing import Protocol


class Reader(Protocol):
    def read(self, file_path: Path) -> dict[str, str]:
        ...
