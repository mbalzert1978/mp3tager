from __future__ import annotations

from typing import Any, Dict, List, Optional

from pydantic import BaseModel


class Tracks(BaseModel):
    href: str | None
    items: List[Dict[str, Any]] | None
    limit: int | None
    next: str | None
    offset: int | None
    previous: str | None
    total: int | None


class Artists(BaseModel):
    href: str | None
    items: List[Dict[str, Any]] | None
    limit: int | None
    next: str | None
    offset: int | None
    previous: str | None
    total: int | None


class Albums(BaseModel):
    href: str | None
    items: List[Dict[str, Any]] | None
    limit: int | None
    next: str | None
    offset: int | None
    previous: str | None
    total: int | None


class Playlists(BaseModel):
    href: str | None
    items: List[Dict[str, Any]] | None
    limit: int | None
    next: str | None
    offset: int | None
    previous: str | None
    total: int | None


class Shows(BaseModel):
    href: str | None
    items: List[Dict[str, Any]] | None
    limit: int | None
    next: str | None
    offset: int | None
    previous: str | None
    total: int | None


class Episodes(BaseModel):
    href: str | None
    items: List[Dict[str, Any]] | None
    limit: int | None
    next: str | None
    offset: int | None
    previous: str | None
    total: int | None


class Audiobooks(BaseModel):
    href: str | None
    items: List[Dict[str, Any]] | None
    limit: int | None
    next: str | None
    offset: int | None
    previous: str | None
    total: int | None


class SpotiModel(BaseModel):
    tracks: Optional[Tracks] = None
    artists: Optional[Artists] = None
    albums: Optional[Albums] = None
    playlists: Optional[Playlists] = None
    shows: Optional[Shows] = None
    episodes: Optional[Episodes] = None
    audiobooks: Optional[Audiobooks] = None
