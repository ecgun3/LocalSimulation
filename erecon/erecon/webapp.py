from __future__ import annotations

import json
from typing import Any, Dict

from flask import Flask, render_template, request

from .config import load_config
from .aggregate import recon_domain, recon_email
from .patterns import generate_email_patterns


app = Flask(__name__, template_folder="templates")


@app.get("/")
def index() -> str:
    return render_template("index.html")


@app.post("/run")
def run_recon() -> str:
    cfg = load_config()

    domain = (request.form.get("domain") or "").strip()
    email = (request.form.get("email") or "").strip()
    first = (request.form.get("first") or "").strip()
    last = (request.form.get("last") or "").strip()

    if not domain and not email:
        return render_template("index.html", error="Lütfen domain ya da email girin.")

    result: Dict[str, Any]
    if email:
        result = recon_email(email, cfg)
        if first and last:
            try:
                dom = email.split("@", 1)[1]
                result["email_patterns"] = generate_email_patterns(first, last, dom)
            except Exception:
                pass
    else:
        result = recon_domain(domain, cfg)
        if first and last and domain:
            result["email_patterns"] = generate_email_patterns(first, last, domain)

    pretty_json = json.dumps(result, indent=2, ensure_ascii=False)
    return render_template("result.html", result=result, pretty_json=pretty_json)


def main() -> None:
    app.run(host="0.0.0.0", port=5000, debug=False)


if __name__ == "__main__":
    main()
