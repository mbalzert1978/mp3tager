import shutil
import tempfile
from pathlib import Path

from src.filesystem import MediaTagFileSystem


def test_get_media_files() -> None:
    media = MediaTagFileSystem()
    try:
        source = tempfile.mkdtemp()
        expected = (
            (Path(source) / "my-file.mp3"),
            w(Path(source) / "my-file.ogg"),
            (Path(source) / "my-file.flac"),
            (Path(source) / "my-file"),
            (Path(source) / "my-file.exe"),
        )
        _ = [x.touch() for x in expected]
        files = tuple(media.get(Path(source)))
        assert all(file in expected for file in files)
        assert len(files) == 3
    finally:
        shutil.rmtree(source)
