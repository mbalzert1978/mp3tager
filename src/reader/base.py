from pathlib import Path
from typing import Protocol


class Reader(Protocol):
    def read(self, file: Path) -> dict | dict[str, str]:
        ...
