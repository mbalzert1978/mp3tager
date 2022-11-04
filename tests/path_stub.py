from __future__ import annotations
from pathlib import Path
from typing import Generator


class PathStub:
    def __init__(self, id_ret_val: bool = True, if_ret_val: bool = False) -> None:
        self.folder = Path("test") / "sub" / "subsub"
        self.idir = id_ret_val
        self.ifile = if_ret_val
        self.count = 0

    def iterdir(self) -> Generator[PathStub, None, None]:
        self.iterdir_called = True
        if self.count < 2:
            self.idir = False
            self.ifile = True
        self.count += 1
        yield self

    def is_dir(self) -> bool:
        self.is_dir_called = True
        return self.idir

    def is_file(self) -> bool:
        self.is_file_called = True
        return self.ifile
