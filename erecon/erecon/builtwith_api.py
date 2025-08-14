from __future__ import annotations

from typing import Any, Dict, Optional

import requests

from .utils import logger


def fetch_builtwith(
    domain: str,
    api_key: Optional[str],
    api_url: str = "https://api.builtwith.com/v21/api.json",
    timeout: int = 20,
) -> Dict[str, Any]:
    if not api_key:
        raise ValueError("BUILTWITH_API_KEY is not configured")

    params = {
        "KEY": api_key,
        "LOOKUP": domain,
    }
    logger.info(f"BuiltWith lookup {domain} via {api_url}")
    resp = requests.get(api_url, params=params, timeout=timeout)
    resp.raise_for_status()
    data = resp.json()
    return data