from pathlib import Path
from typing import Protocol

from ..models.base import ModelBase


class Reader(Protocol):
    def read(self, file_path: Path) -> ModelBase:
        ...
