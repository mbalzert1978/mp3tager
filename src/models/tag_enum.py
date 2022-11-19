from enum import Enum
from uuid import uuid4


class Tags(str, Enum):
    ARTIST = "unknown_artist"
    ALBUM = "unknown_album"
    TITLE = str(uuid4())
