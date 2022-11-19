from typing import Protocol


class ModelBase(Protocol):
    def get_tags(self) -> dict[str, str]:
        ...

    def get_artist(self) -> str:
        ...

    def get_album(self) -> str:
        ...

    def get_title(self) -> str:
        ...
