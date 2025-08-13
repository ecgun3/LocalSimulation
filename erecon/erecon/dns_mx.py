from __future__ import annotations

from dataclasses import dataclass
from typing import List, Dict, Any

import dns.resolver


@dataclass
class MxRecord:
    preference: int
    exchange: str


COMMON_PROVIDERS = {
    "google": [".google.com.", ".googlemail.com."],
    "microsoft": [".outlook.com.", ".protection.outlook.com."],
    "proofpoint": [".pphosted.com."],
    "mimecast": [".mimecast.com."],
    "barracuda": [".ess.barracudanetworks.com.", ".barracudanetworks.com."],
    "sendgrid": [".sendgrid.net."],
    "mailgun": [".mailgun.org."],
    "zoho": [".zoho.com.", ".zohomail.com."],
    "fastmail": [".messagingengine.com."],
    "yandex": [".yandex.net."],
    "icloud": [".icloud.com."],
    "rackspace": [".emailsrvr.com."],
    "cisco": [".protection.outlook.com.", ".secureserver.net."],
    "godaddy": [".secureserver.net."],
}


def get_mx_records(domain: str) -> List[MxRecord]:
    answers = dns.resolver.resolve(domain, "MX")
    records: List[MxRecord] = []
    for rdata in answers:  # type: ignore[attr-defined]
        records.append(
            MxRecord(preference=int(rdata.preference), exchange=str(rdata.exchange).lower())
        )
    records.sort(key=lambda r: r.preference)
    return records


def detect_provider(mx_records: List[MxRecord]) -> List[str]:
    providers: set[str] = set()
    for rec in mx_records:
        for provider, needles in COMMON_PROVIDERS.items():
            for needle in needles:
                if rec.exchange.endswith(needle):
                    providers.add(provider)
    return sorted(providers)


def serialize_mx(mx_records: List[MxRecord]) -> List[Dict[str, Any]]:
    return [
        {"preference": rec.preference, "exchange": rec.exchange}
        for rec in mx_records
    ]