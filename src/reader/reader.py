import os
from collections import defaultdict
from pathlib import Path

import requests
from dotenv import load_dotenv
from mediafile import FileTypeError, MediaFile, UnreadableFileError

from .base import Reader


class TagReader(Reader):
    def read(self, file_path: Path) -> dict[str, str]:
        try:
            return MediaFile(file_path).as_dict()
        except (FileTypeError, UnreadableFileError):
            return {"artist": "", "album": "", "title": ""}


class AudDReader(Reader):
    """
    Read media files and return there tags.

    Returns:
        Calls audd.io api with 300kb data from the file
        to recognize music in audio files
    """

    URI = "https://api.audd.io/"

    def read(self, file_path: Path) -> dict[str, str]:
        """
        Call api and create tags from received data.

        Args:
            file: media file

        Returns:
            Dictionary with `"artists"`, `"album"` and `"title"`
        """

        data = self._prepare_data()
        with file_path.open("rb") as file:
            files = {"file": file.read(300000)}
            return self._call_api(data, files)

    def _call_api(
        self, data: dict[str, str], files: dict[str, bytes]
    ) -> dict[str, str]:
        with requests.session() as session:
            response = session.post(self.URI, data=data, files=files)
            api_data = response.json() if response else {}
        return api_data.get("result")

    def _prepare_data(self) -> dict[str, str]:
        return {
            "api_token": self._get_api_key(),
            "return": "apple_music,spotify",
        }

    def _get_api_key(self) -> str:
        load_dotenv()
        if not (api_key := os.getenv("API_KEY")):
            raise KeyError(
                "No api key found in environ. "
                f"Please provide a valid api key from {self.URI} via .env"
            )
        return api_key


class MultiReader(Reader):
    def __init__(self, readers: tuple[Reader, ...]) -> None:
        self.readers = readers

    def read(self, file_path: Path) -> dict | dict[str, str]:
        responses = []
        for reader in self.readers:
            response = reader.read(file_path=file_path)
            if not all(self._get_tags(response)):
                responses.append(response)
                continue
            return response
        return self.evaluate_responses(responses)

    def evaluate_responses(self, data: list[dict]) -> dict[str, str]:
        temp = {"artist": "", "album": "", "title": ""}
        for response in data:
            for key, value in response.items():
                if not value:
                    continue
                if value not in temp.values():
                    temp[key] = value
        return temp

    def _get_tags(self, response: dict) -> tuple[str | None, ...]:
        return (
            response.get("artist"),
            response.get("album"),
            response.get("title"),
        )
