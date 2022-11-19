import asyncio
import os
from pathlib import Path

import acrcloud
import requests
from dotenv import load_dotenv
from mediafile import MediaFile
from shazamio import Shazam

from ..models.acr_model import ACRCloudModel
from ..models.aud_model import AudDModel
from ..models.base import ModelBase
from ..models.tag_enum import Tags
from ..models.tag_model import Result, TagModel
from .base import Reader


class TagReader(Reader):
    def read(self, file_path: Path) -> ModelBase:
        result = Result(**MediaFile(file_path).as_dict())
        return TagModel(result=result)


class AudDReader(Reader):
    """Uses audd.io api with 500kb data from the file
    to recognize music in media files.
    """

    URI = "https://api.audd.io/"
    BYTES_TO_READ = 500_000

    def read(self, file_path: Path) -> ModelBase:
        """
        Call api and create tags from received data.

        Args:
            file: media file

        Returns:
            ModelBase
        """

        data = self._prepare_data()
        with file_path.open("rb") as file:
            files = {"file": file.read(self.BYTES_TO_READ)}
            return self._call_api(data, files)

    def _call_api(
        self, data: dict[str, str], files: dict[str, bytes]
    ) -> ModelBase:
        with requests.session() as session:
            response = session.post(self.URI, data=data, files=files)
            response.encoding = "utf-8"
            return AudDModel(**response.json())

    def _prepare_data(self) -> dict[str, str]:
        return {
            "api_token": os.getenv("API_KEY"),
            "return": "apple_music,spotify",
        }


class ACRCloudReader(Reader):
    """Uses acrcloud.com api with 1mb data from the file
    to recognize music in media files.
    """

    def read(self, file_path: Path) -> ModelBase:
        """
        Call api and create tags from received data.

        Args:
            file: media file

        Returns:
            ModelBase
        """
        provider = acrcloud.ACRcloud(self._prepare_credentials())
        return ACRCloudModel(**provider.recognize_audio(file_path))

    def _prepare_credentials(self) -> str:
        load_dotenv()
        return {
            "key": os.getenv("ACCESS_KEY"),
            "secret": os.getenv("SECRET_KEY"),
            "host": os.getenv("ACR_HOST"),
        }


class ShazamIOReader(Reader):
    async def read(self, file_path: Path) -> ModelBase:
        shaz = Shazam()
        out = await shaz.recognize_song(file_path)
        print(out)
        print()
