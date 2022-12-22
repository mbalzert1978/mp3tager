from dataclasses import dataclass


@dataclass(unsafe_hash=True)
class MediaFile:
    name: str
    path: str
    tags:
