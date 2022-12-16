import shutil
import tempfile
from pathlib import Path

from src.filesystem import MediaTagFileSystem


def test_get_all_media_files() -> None:
    media = MediaTagFileSystem()
    try:
        source = tempfile.mkdtemp()
        (Path(source) / "one_down").mkdir()
        expected = (
            (Path(source) / "my-file.mp3"),
            (Path(source) / "my-file.ogg"),
            (Path(source) / "my-file.flac"),
            (Path(source) / "my-file"),
            (Path(source) / "one_down" / "my-file.exe"),
        )
        _ = [x.touch() for x in expected]
        files = tuple(media.get(Path(source)))
        assert all(file in expected for file in files)
        assert len(files) == 3
    finally:
        shutil.rmtree(source)


def test_copy_files() -> None:
    media = MediaTagFileSystem()
    try:
        source = tempfile.mkdtemp()
        destination = tempfile.mkdtemp()
        expected: Path = Path(source) / "my-file.mp3"
        expected.touch()
        media.copy(Path(expected), Path(destination))
        assert expected in destination
    finally:
        shutil.rmtree(source)
        shutil.rmtree(destination)
