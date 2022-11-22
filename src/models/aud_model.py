from __future__ import annotations

from typing import Any

from pydantic import BaseModel

from ..utilities.string import sanatize
from .tag_enum import Tags


class Preview(BaseModel):
    url: str | None


class Artwork(BaseModel):
    width: int | None
    height: int | None
    url: str | None
    bgColor: str | None
    textColor1: str | None
    textColor2: str | None
    textColor3: str | None
    textColor4: str | None


class PlayParams(BaseModel):
    id: str | None
    kind: str | None


class AppleMusic(BaseModel):
    previews: list[Preview] | None
    artwork: Artwork | None
    artistName: str | None
    url: str | None
    discNumber: int | None
    genreNames: list[str] | None
    durationInMillis: int | None
    releaseDate: str | None
    name: str | None
    isrc: str | None
    albumName: str | None
    playParams: PlayParams | None
    trackNumber: int | None
    composerName: str | None


class ExternalUrls(BaseModel):
    spotify: str | None


class Artist(BaseModel):
    name: str | None
    id: str | None
    uri: str | None
    href: str | None
    external_urls: ExternalUrls | None


class Image(BaseModel):
    height: int | None
    width: int | None
    url: str | None


class ExternalUrls1(BaseModel):
    spotify: str | None


class Album(BaseModel):
    name: str | None
    artists: list[Artist] | None
    album_group: str | None
    album_type: str | None
    id: str | None
    uri: str | None
    available_markets: list[str] | None
    href: str | None
    images: list[Image] | None
    external_urls: ExternalUrls1 | None
    release_date: str | None
    release_date_precision: str | None


class ExternalIds(BaseModel):
    isrc: str | None


class ExternalUrls2(BaseModel):
    spotify: str | None


class Artist1(BaseModel):
    name: str | None
    id: str | None
    uri: str | None
    href: str | None
    external_urls: ExternalUrls2 | None


class ExternalUrls3(BaseModel):
    spotify: str | None


class Spotify(BaseModel):
    album: Album | None
    external_ids: ExternalIds | None
    popularity: int | None
    is_playable: Any | None
    linked_from: Any | None
    artists: list[Artist1] | None
    available_markets: list[str] | None
    disc_number: int | None
    duration_ms: int | None
    explicit: bool | None
    external_urls: ExternalUrls3 | None
    href: str | None
    id: str | None
    name: str | None
    preview_url: str | None
    track_number: int | None
    uri: str | None


class Result(BaseModel):
    artist: str | None
    title: str | None
    album: str | None
    release_date: str | None
    label: str | None
    timecode: str | None
    song_link: str | None
    apple_music: AppleMusic | None
    spotify: Spotify | None


class AudDModel(BaseModel):
    status: str
    result: Result | None

    def get_tags(self) -> dict[str, str]:
        return (
            {
                "artist": sanatize(self.result.artist),
                "album": sanatize(self.result.album),
                "title": sanatize(self.result.title),
            }
            if self.result
            else {
                "artist": Tags.ARTIST.value,
                "album": Tags.ALBUM.value,
                "title": Tags.TITLE.value,
            }
        )

    def get_artist(self) -> str:
        return (
            sanatize(self.result.artist) if self.result else Tags.ARTIST.value
        )

    def get_album(self) -> str:
        return sanatize(self.result.album) if self.result else Tags.ALBUM.value

    def get_title(self) -> str:
        return sanatize(self.result.title) if self.result else Tags.TITLE.value
