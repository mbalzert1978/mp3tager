from __future__ import annotations

from typing import Any

from pydantic import BaseModel, Field

from ..utilities.sequnce import fetch_one
from ..utilities.string import sanatize
from .tag_enum import Tags


class Status(BaseModel):
    version: str | None
    msg: str | None
    code: int | None


class Lang(BaseModel):
    name: str | None
    code: str | None


class Artist(BaseModel):
    name: str | None
    langs: list[Lang] = None


class Album(BaseModel):
    name: str | None


class Genre(BaseModel):
    name: str | None


class MusicItem(BaseModel):
    external_metadata: dict[str, Any] | None
    label: str | None
    db_begin_time_offset_ms: int | None
    db_end_time_offset_ms: int | None
    sample_begin_time_offset_ms: int | None
    sample_end_time_offset_ms: int | None
    play_offset_ms: int | None
    result_from: int | None
    duration_ms: int | None
    artists: list[Artist] | None
    external_ids: dict[str, Any] | None
    acrid: str | None
    title: str | None
    album: Album | None
    score: int | None
    release_date: str | None
    genres: list[Genre] = None


class Result(BaseModel):
    music: list[MusicItem] | None
    timestamp_utc: str | None


class ACRCloudModel(BaseModel):
    result_type: int | None
    status: Status
    result: Result | None = Field(alias="metadata")
    cost_time: float | None

    @property
    def musik_item(self) -> MusicItem | None:
        if not self.result:
            return None
        return fetch_one(self.result.music)

    def get_tags(self) -> dict[str, str]:
        if not self.result:
            return {
                "artist": Tags.ARTIST.value,
                "album": Tags.ALBUM.value,
                "title": Tags.TITLE.value,
            }
        return {
            "artist": sanatize(fetch_one(self.musik_item.artists).name),
            "album": sanatize(self.musik_item.album.name),
            "title": sanatize(self.musik_item.title),
        }

    def get_artist(self) -> str:
        if not self.result:
            return Tags.ARTIST.value
        return sanatize(fetch_one(self.musik_item.artists).name)

    def get_album(self) -> str:
        if not self.result:
            return Tags.ALBUM.value
        return sanatize(self.musik_item.album.name)

    def get_title(self) -> str:
        if not self.result:
            return Tags.TITLE.value
        return sanatize(self.musik_item.title)
