import os
from pathlib import Path

import requests
from dotenv import load_dotenv

load_dotenv()
print()


class AudDReader:
    URI = "https://api.audd.io/"

    def read(self, file: Path) -> dict | dict[str, str]:
        data = {
            "api_token": os.getenv("API_KEY"),
            "return": "apple_music,spotify",
        }
        with open(file, "rb") as f:
            area = f.read(300000)
            files = {"file": area}
            with requests.session() as session:
                result = session.post(self.URI, data=data, files=files)
                return_value: dict | None = result.json()
                if return_value.get("status") is not "success":
                    return {}
                if return_value.get("result") is None:
                    return {}
                return return_value.get("result")
