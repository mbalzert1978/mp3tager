import src.mp3tagv2 as mp3tag
from src.media.media_file import MediaFile


def test_recognize_song_returns_MediaFile() -> None:
    result = mp3tag.reqcognize_song("test")
    assert isinstance(result, MediaFile)
