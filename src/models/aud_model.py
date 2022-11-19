from __future__ import annotations

from typing import Any, List
from uuid import uuid4

from pydantic import BaseModel

from ..utilities.string import sanatize


class Preview(BaseModel):
    url: str


class Artwork(BaseModel):
    width: int
    height: int
    url: str
    bgColor: str
    textColor1: str
    textColor2: str
    textColor3: str
    textColor4: str


class PlayParams(BaseModel):
    id: str
    kind: str


class AppleMusic(BaseModel):
    previews: List[Preview]
    artwork: Artwork
    artistName: str
    url: str
    discNumber: int
    genreNames: List[str]
    durationInMillis: int
    releaseDate: str
    name: str
    isrc: str
    albumName: str
    playParams: PlayParams
    trackNumber: int
    composerName: str


class ExternalUrls(BaseModel):
    spotify: str


class Artist(BaseModel):
    name: str
    id: str
    uri: str
    href: str
    external_urls: ExternalUrls


class Image(BaseModel):
    height: int
    width: int
    url: str


class ExternalUrls1(BaseModel):
    spotify: str


class Album(BaseModel):
    name: str
    artists: List[Artist]
    album_group: str
    album_type: str
    id: str
    uri: str
    available_markets: List[str]
    href: str
    images: List[Image]
    external_urls: ExternalUrls1
    release_date: str
    release_date_precision: str


class ExternalIds(BaseModel):
    isrc: str


class ExternalUrls2(BaseModel):
    spotify: str


class Artist1(BaseModel):
    name: str
    id: str
    uri: str
    href: str
    external_urls: ExternalUrls2


class ExternalUrls3(BaseModel):
    spotify: str


class Spotify(BaseModel):
    album: Album
    external_ids: ExternalIds
    popularity: int
    is_playable: Any
    linked_from: Any
    artists: List[Artist1]
    available_markets: List[str]
    disc_number: int
    duration_ms: int
    explicit: bool
    external_urls: ExternalUrls3
    href: str
    id: str
    name: str
    preview_url: str
    track_number: int
    uri: str


class Result(BaseModel):
    artist: str
    title: str
    album: str
    release_date: str
    label: str
    timecode: str
    song_link: str
    apple_music: AppleMusic | None
    spotify: Spotify | None


class AudDModel(BaseModel):
    status: str
    result: Result | None

    def get_tags(self) -> dict[str, str]:
        if not self.result:
            return {
                "artist": "unknown_artist",
                "album": "unknown_album",
                "title": sanatize(str(uuid4())),
            }
        return {
            "artist": sanatize(self.result.artist),
            "album": sanatize(self.result.album),
            "title": sanatize(self.result.title),
        }
