from typing import Protocol


class ModelBase(Protocol):
    def get_tags(self) -> dict[str, str]:
        ...
