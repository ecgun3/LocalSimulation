from __future__ import annotations

import argparse
import json
import sys
from typing import Any, Dict

from .config import load_config
from .aggregate import recon_domain, recon_email
from .patterns import generate_email_patterns


def _print_json(data: Dict[str, Any]) -> None:
    print(json.dumps(data, indent=2, sort_keys=False, ensure_ascii=False))


def _print_human(data: Dict[str, Any]) -> None:
    # Keep simple and readable
    if "domain" in data:
        dom = data["domain"]
        print(f"Domain: {dom}")
        if data.get("mx_records"):
            print("MX Records:")
            for rec in data["mx_records"]:
                print(f"  - {rec['preference']}: {rec['exchange']}")
        if data.get("mx_providers"):
            print("Providers:")
            for p in data["mx_providers"]:
                print(f"  - {p}")
        if data.get("mx_error"):
            print(f"MX Error: {data['mx_error']}")
        if data.get("builtwith_error"):
            print(f"BuiltWith Error: {data['builtwith_error']}")
        if data.get("builtwith_skipped"):
            print("BuiltWith: skipped (no API key)")
        if data.get("email_patterns"):
            print("Email patterns (guesses):")
            for e in data["email_patterns"]:
                print(f"  - {e}")
    else:
        email = data.get("email")
        if email:
            print(f"Email: {email}")
        di = data.get("domain_info")
        if di:
            print("")
            _print_human(di)
        hh = data.get("holehe")
        if hh:
            if not hh.get("available"):
                print("Holehe: not available")
            else:
                if hh.get("json") is not None:
                    print("Holehe (JSON present)")
                else:
                    # Print a few lines of raw output for human context
                    raw = (hh.get("stdout") or "").splitlines()
                    if raw:
                        print("Holehe (raw):")
                        for line in raw[:10]:
                            print(f"  {line}")
        if data.get("genesys_error"):
            print(f"Genesys Error: {data['genesys_error']}")
        if data.get("genesys_skipped"):
            print("Genesys: skipped (not configured)")
        if data.get("email_patterns"):
            print("Email patterns (guesses):")
            for e in data["email_patterns"]:
                print(f"  - {e}")


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="ERecon - Email Reconnaissance CLI")
    parser.add_argument("--domain", help="Domain to recon")
    parser.add_argument("--email", help="Email to recon")
    parser.add_argument("--first", help="First name for pattern guesses")
    parser.add_argument("--last", help="Last name for pattern guesses")
    parser.add_argument("--json", action="store_true", help="Output JSON")

    args = parser.parse_args(argv)

    cfg = load_config()

    if not args.domain and not args.email:
        parser.error("Please specify --domain or --email")

    if args.email:
        result = recon_email(args.email, cfg)
        if args.first and args.last:
            try:
                dom = args.email.split("@", 1)[1]
                result["email_patterns"] = generate_email_patterns(args.first, args.last, dom)
            except Exception:
                pass
    else:
        result = recon_domain(args.domain, cfg)  # type: ignore[arg-type]
        if args.first and args.last and args.domain:
            result["email_patterns"] = generate_email_patterns(args.first, args.last, args.domain)

    if args.json:
        _print_json(result)
    else:
        _print_human(result)

    return 0


if __name__ == "__main__":
    raise SystemExit(main())