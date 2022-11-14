from typing import Any, Protocol


class MediaBase(Protocol):
    def load(self, filename: str) -> dict[str, Any] | None:
        ...

    def save(self, media_tags: dict[str, Any]) -> None:
        ...
