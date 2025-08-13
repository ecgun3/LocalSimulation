from __future__ import annotations

from typing import Any, Dict, Optional

from .config import Config


def recon_domain(domain: str, cfg: Config) -> Dict[str, Any]:
    result: Dict[str, Any] = {"domain": domain}

    # MX
    try:
        from .dns_mx import get_mx_records, detect_provider, serialize_mx  # local import

        mx_records = get_mx_records(domain)
        result["mx_records"] = serialize_mx(mx_records)
        result["mx_providers"] = detect_provider(mx_records)
    except Exception as exc:  # noqa: BLE001
        result["mx_error"] = str(exc)

    # BuiltWith
    if cfg.builtwith_api_key:
        try:
            from .builtwith_api import fetch_builtwith  # local import

            bw = fetch_builtwith(
                domain,
                api_key=cfg.builtwith_api_key,
                api_url=cfg.builtwith_api_url,
                timeout=cfg.requests_timeout,
            )
            result["builtwith"] = bw
        except Exception as exc:  # noqa: BLE001
            result["builtwith_error"] = str(exc)
    else:
        result["builtwith_skipped"] = True

    return result


def recon_email(email: str, cfg: Config) -> Dict[str, Any]:
    result: Dict[str, Any] = {"email": email}

    # Derive domain and run domain recon
    try:
        domain = email.split("@", 1)[1]
    except Exception:
        domain = None
    if domain:
        result["domain_info"] = recon_domain(domain, cfg)

    # Holehe
    try:
        from .holehe_integration import run_holehe  # local import

        hh = run_holehe(email, holehe_cmd=cfg.holehe_cmd, timeout=cfg.requests_timeout * 3)
        result["holehe"] = hh
    except Exception as exc:  # noqa: BLE001
        result["holehe_error"] = str(exc)

    return result