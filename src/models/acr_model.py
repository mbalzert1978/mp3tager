from __future__ import annotations

from typing import Any, Dict, List, Optional
from uuid import uuid4

from pydantic import BaseModel, Field

from ..utilities.sequnce import fetch_one
from ..utilities.string import sanatize


class Status(BaseModel):
    version: str
    msg: str
    code: int


class Lang(BaseModel):
    name: str
    code: str


class Artist(BaseModel):
    name: str
    langs: Optional[List[Lang]] = None


class Album(BaseModel):
    name: str


class Genre(BaseModel):
    name: str


class MusicItem(BaseModel):
    external_metadata: Dict[str, Any]
    label: str
    db_begin_time_offset_ms: int
    db_end_time_offset_ms: int
    sample_begin_time_offset_ms: int
    sample_end_time_offset_ms: int
    play_offset_ms: int
    result_from: int
    duration_ms: int
    artists: List[Artist]
    external_ids: Dict[str, Any]
    acrid: str
    title: str
    album: Album
    score: int
    release_date: str
    genres: Optional[List[Genre]] = None


class Result(BaseModel):
    music: List[MusicItem]
    timestamp_utc: str


class ACRCloudModel(BaseModel):
    result_type: int | None
    status: Status
    result: Result | None = Field(alias="metadata")
    cost_time: float | None

    def get_tags(self) -> dict[str, str]:
        if not self.result:
            return {
                "artist": "unknown_artist",
                "album": "unknown_album",
                "title": sanatize(str(uuid4())),
            }
        music_item: MusicItem = fetch_one(self.result.music)
        return {
            "artist": sanatize(fetch_one(music_item.artists).name),
            "album": sanatize(music_item.album.name),
            "title": sanatize(music_item.title),
        }
