import os
from dataclasses import dataclass
from typing import Optional

try:
    from dotenv import load_dotenv  # type: ignore
    load_dotenv()
except Exception:
    pass


@dataclass
class Config:
    builtwith_api_key: Optional[str]
    builtwith_api_url: str

    genesys_login_url: Optional[str]
    genesys_api_url: Optional[str]
    genesys_client_id: Optional[str]
    genesys_client_secret: Optional[str]

    holehe_cmd: str
    requests_timeout: int


def load_config() -> Config:
    return Config(
        builtwith_api_key=os.getenv("BUILTWITH_API_KEY"),
        builtwith_api_url=os.getenv(
            "BUILTWITH_API_URL", "https://api.builtwith.com/v21/api.json"
        ),
        genesys_login_url=os.getenv("GENESYS_LOGIN_URL"),
        genesys_api_url=os.getenv("GENESYS_API_URL"),
        genesys_client_id=os.getenv("GENESYS_CLIENT_ID"),
        genesys_client_secret=os.getenv("GENESYS_CLIENT_SECRET"),
        holehe_cmd=os.getenv("HOLEHE_CMD", "holehe"),
        requests_timeout=int(os.getenv("REQUESTS_TIMEOUT", "20")),
    )