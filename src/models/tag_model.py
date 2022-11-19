from __future__ import annotations

from typing import Any, List
from uuid import uuid4

from pydantic import BaseModel, validator

from ..utilities.string import sanatize


class Result(BaseModel):
    class Config:
        validate_assignment = True

    title: str | None
    artist: str | None
    album: str | None
    artists: List | None = None
    genres: List | None = None
    genre: Any | None = None
    lyricist: Any | None = None
    composer: Any | None = None
    composer_sort: Any | None = None
    arranger: Any | None = None
    grouping: Any | None = None
    track: Any | None = None
    tracktotal: Any | None = None
    disc: Any | None = None
    disctotal: Any | None = None
    url: Any | None = None
    lyrics: Any | None = None
    comments: Any | None = None
    copyright: Any | None = None
    bpm: Any | None = None
    comp: Any | None = None
    albumartist: Any | None = None
    albumartists: List | None = None
    albumtypes: List | None = None
    albumtype: Any | None = None
    label: Any | None = None
    artist_sort: Any | None = None
    albumartist_sort: Any | None = None
    asin: Any | None = None
    catalognums: List | None = None
    catalognum: Any | None = None
    barcode: Any | None = None
    isrc: Any | None = None
    disctitle: Any | None = None
    encoder: Any | None = None
    script: Any | None = None
    languages: List | None = None
    language: Any | None = None
    country: Any | None = None
    albumstatus: Any | None = None
    media: Any | None = None
    albumdisambig: Any | None = None
    date: Any | None = None
    year: Any | None = None
    month: Any | None = None
    day: Any | None = None
    original_date: Any | None = None
    original_year: Any | None = None
    original_month: Any | None = None
    original_day: Any | None = None
    artist_credit: Any | None = None
    albumartist_credit: Any | None = None
    art: Any | None = None
    images: List | None = None
    mb_trackid: Any | None = None
    mb_releasetrackid: Any | None = None
    mb_workid: Any | None = None
    mb_albumid: Any | None = None
    mb_artistids: List | None = None
    mb_artistid: Any | None = None
    mb_albumartistids: List | None = None
    mb_albumartistid: Any | None = None
    mb_releasegroupid: Any | None = None
    acoustid_fingerprint: Any | None = None
    acoustid_id: Any | None = None
    rg_track_gain: float | None = None
    rg_album_gain: Any | None = None
    rg_track_peak: float | None = None
    rg_album_peak: Any | None = None
    r128_track_gain: Any | None = None
    r128_album_gain: Any | None = None
    initial_key: Any | None = None

    @validator("artist")
    def set_artist(cls, value):
        return value or "unknown_artist"

    @validator("album")
    def set_album(cls, value):
        return value or "unknown_album"

    @validator("title")
    def set_title(cls, value):
        return value or str(uuid4())


class TagModel(BaseModel):
    result: Result | None

    def get_tags(self) -> dict[str, str]:
        return {
            "artist": sanatize(self.result.artist),
            "album": sanatize(self.result.album),
            "title": sanatize(self.result.title),
        }
