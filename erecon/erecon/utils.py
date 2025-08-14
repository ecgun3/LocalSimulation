from __future__ import annotations

import json
import logging
import time
from typing import Any, Dict, Optional

import requests


def requests_retry_session(
    retries: int = 3,
    backoff_factor: float = 0.5,
    status_forcelist: tuple[int, ...] = (429, 500, 502, 503, 504),
) -> requests.Session:
    session = requests.Session()

    # Simple manual retry loop in our wrappers below; keep session plain here.
    # This avoids needing urllib3 Retry dependency setup.
    return session


def http_post_json(
    url: str,
    json_body: Dict[str, Any],
    headers: Optional[Dict[str, str]] = None,
    timeout: int = 20,
    retries: int = 3,
    backoff_factor: float = 0.5,
) -> requests.Response:
    session = requests_retry_session()
    last_exc: Optional[Exception] = None
    for attempt in range(retries):
        try:
            resp = session.post(url, json=json_body, headers=headers, timeout=timeout)
            if resp.status_code in (429, 500, 502, 503, 504):
                raise requests.HTTPError(
                    f"Retryable status {resp.status_code} for POST {url}"
                )
            return resp
        except Exception as exc:  # noqa: BLE001
            last_exc = exc
            sleep_s = backoff_factor * (2**attempt)
            time.sleep(sleep_s)
    assert last_exc is not None
    raise last_exc


def http_post_form(
    url: str,
    form: Dict[str, Any],
    headers: Optional[Dict[str, str]] = None,
    timeout: int = 20,
    retries: int = 3,
    backoff_factor: float = 0.5,
) -> requests.Response:
    session = requests_retry_session()
    last_exc: Optional[Exception] = None
    for attempt in range(retries):
        try:
            resp = session.post(url, data=form, headers=headers, timeout=timeout)
            if resp.status_code in (429, 500, 502, 503, 504):
                raise requests.HTTPError(
                    f"Retryable status {resp.status_code} for POST {url}"
                )
            return resp
        except Exception as exc:  # noqa: BLE001
            last_exc = exc
            sleep_s = backoff_factor * (2**attempt)
            time.sleep(sleep_s)
    assert last_exc is not None
    raise last_exc


def try_parse_json(text: str) -> Optional[Dict[str, Any]]:
    try:
        return json.loads(text)
    except Exception:  # noqa: BLE001
        return None


def redact_secret(value: Optional[str]) -> str:
    if not value:
        return ""
    if len(value) <= 6:
        return "***"
    return value[:3] + "***" + value[-3:]


logging.basicConfig(level=logging.INFO, format="[%(levelname)s] %(message)s")
logger = logging.getLogger("erecon")