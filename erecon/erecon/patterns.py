from __future__ import annotations

from typing import List


COMMON_PATTERNS = [
    "{first}.{last}",
    "{first}{last}",
    "{f}{last}",
    "{first}{l}",
    "{f}{l}",
    "{last}{first}",
    "{first}_{last}",
    "{last}.{first}",
]


def generate_email_patterns(first_name: str, last_name: str, domain: str) -> List[str]:
    first = first_name.strip().lower()
    last = last_name.strip().lower()
    f = first[:1]
    l = last[:1]
    emails = [
        pattern.format(first=first, last=last, f=f, l=l) + f"@{domain}"
        for pattern in COMMON_PATTERNS
    ]
    # De-duplicate while preserving order
    deduped: List[str] = []
    seen: set[str] = set()
    for e in emails:
        if e not in seen:
            deduped.append(e)
            seen.add(e)
    return deduped