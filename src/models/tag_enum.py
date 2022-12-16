from enum import Enum
from uuid import uuid4


class Tags(Enum):
    ARTIST = "unknown_artist"
    ALBUM = "unknown_album"
    TITLE = str(uuid4())

    def __str__(self) -> str:
        return self.value
