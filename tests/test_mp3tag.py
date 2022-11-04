import logging
import tempfile
from pathlib import Path

import pytest

import mp3tag
from mp3tag import _create_path_sanatize, _extract_suffix, _sanatize, mp3_tag

from .path_stub import PathStub


@pytest.mark.parametrize("val,exp", [("!test:", "test"), (":$te_st/", "test")])
def test_sanatize(val, exp) -> None:
    assert _sanatize(val) == exp


@pytest.mark.parametrize(
    "val,exp",
    [
        (Path("t.txt"), ".txt"),
        (Path("t.jpg"), ".jpg"),
        (Path("t"), ""),
    ],
)
def test_extract_suffix(val, exp):
    assert _extract_suffix(val) == exp


def test_create_path_sanatize(caplog):
    assert (
        _create_path_sanatize(Path("test"), (None, None, "", "on!e"))
        == Path("test") / "one"
    )
    with caplog.at_level(logging.INFO):
        _ = _create_path_sanatize(Path("test"), (None,))
    assert "No valid tag info, generating uuid string." in caplog.text


def test_mp3_tag(monkeypatch) -> None:
    monkeypatch.setattr(
        mp3tag,
        "_get_mp3_info_and_copy_with_new_filename",
        lambda x, y: (x, y),
    )
    stub, temp = PathStub(), tempfile.mkdtemp()
    mp3_tag(stub, temp)  # type:ignore
    assert stub.iterdir_called
    assert stub.is_dir_called
    assert stub.is_file_called
