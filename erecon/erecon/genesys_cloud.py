from __future__ import annotations

import base64
import time
from dataclasses import dataclass
from typing import Any, Dict, List, Optional

from .utils import http_post_form, http_post_json, logger


@dataclass
class OAuthToken:
    access_token: str
    token_type: str
    expires_in: int
    acquired_at: float

    def is_expired(self) -> bool:
        # Consider token expired if within 60s of expiry
        return (time.time() - self.acquired_at) > max(0, self.expires_in - 60)


class GenesysClient:
    def __init__(
        self,
        login_url: str,
        api_url: str,
        client_id: str,
        client_secret: str,
        timeout: int = 20,
    ) -> None:
        self.login_url = login_url.rstrip("/")
        self.api_url = api_url.rstrip("/")
        self.client_id = client_id
        self.client_secret = client_secret
        self.timeout = timeout
        self._token: Optional[OAuthToken] = None

    def _basic_auth_header(self) -> str:
        creds = f"{self.client_id}:{self.client_secret}".encode()
        return base64.b64encode(creds).decode()

    def _ensure_token(self) -> str:
        if self._token is None or self._token.is_expired():
            token_url = f"{self.login_url}/oauth/token"
            headers = {
                "Authorization": f"Basic {self._basic_auth_header()}",
                "Content-Type": "application/x-www-form-urlencoded",
            }
            form = {"grant_type": "client_credentials"}
            logger.info("Requesting Genesys OAuth token")
            resp = http_post_form(token_url, form=form, headers=headers, timeout=self.timeout)
            resp.raise_for_status()
            data = resp.json()
            self._token = OAuthToken(
                access_token=data["access_token"],
                token_type=data.get("token_type", "Bearer"),
                expires_in=int(data.get("expires_in", 3600)),
                acquired_at=time.time(),
            )
        assert self._token is not None
        return self._token.access_token

    def search_users_by_email(self, email: str, page_size: int = 25) -> Dict[str, Any]:
        token = self._ensure_token()
        url = f"{self.api_url}/api/v2/users/search"
        headers = {"Authorization": f"Bearer {token}", "Content-Type": "application/json"}
        body: Dict[str, Any] = {
            "pageSize": page_size,
            "query": [
                {"type": "TERM", "fields": ["email"], "value": email},
            ],
        }
        resp = http_post_json(url, json_body=body, headers=headers, timeout=self.timeout)
        resp.raise_for_status()
        return resp.json()