from dataclasses import dataclass


@dataclass
class MediaFile:
    artist: str
    song: str
    title: str
    album: str
