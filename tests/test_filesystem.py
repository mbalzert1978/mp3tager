from pathlib import Path
import shutil

import tempfile
from src.repo.filesystem import read_paths
from src.repo.media_file import MediaFileFake


def test_read_path():
    pass


def test_file_found_and_tags_created():
    try:
        expected_path = Path(tempfile.mkdtemp())
        expected_tag = {
            "album": "test_album",
            "title": "test_title",
            "artist": "test_artist",
        }
        result: dict[Path, str] = read_paths(expected_path, MediaFileFake())
        result, tag = next(iter(result.items()))
        assert result.exists()
        assert tag.get("title") == expected_tag.get("title")
        assert tag.get("album") == expected_tag.get("album")
        assert tag.get("genre") == expected_tag.get("genre")
    finally:
        shutil.rmtree(expected_path)


def test_no_file_found_and_tags_created():
    try:
        root = tempfile.mkdtemp()
        content = "I am a very useful file"
        (Path(root) / "my-file.mp3").write_text(content)
        result: dict[Path, str] = read_paths(root)
        expected_path, tags = next(iter(result.items()))
        assert expected_path.exists()
        assert not tags.get("title")
        assert not tags.get("album")
        assert not tags.get("genre")
    finally:
        shutil.rmtree(root)
