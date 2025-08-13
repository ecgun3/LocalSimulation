from __future__ import annotations

import json
import shlex
import shutil
import subprocess
from typing import Any, Dict, Optional

from .utils import logger, try_parse_json


def run_holehe(
    email: str,
    holehe_cmd: str = "holehe",
    timeout: int = 180,
) -> Dict[str, Any]:
    cmd_available = shutil.which(holehe_cmd.split()[0]) is not None
    if not cmd_available and holehe_cmd == "holehe":
        # Try module invocation as a fallback
        holehe_cmd = "python -m holehe"
        cmd_available = shutil.which("python") is not None

    if not cmd_available:
        logger.warning("Holehe not installed; skipping")
        return {"available": False, "returncode": None, "json": None, "stdout": "", "stderr": ""}

    # Attempt JSON output first (some versions support -j/--json)
    json_flags = ["-j"]
    full_cmd = f"{holehe_cmd} {shlex.quote(email)} {' '.join(json_flags)}"
    logger.info(f"Running Holehe: {full_cmd}")
    try:
        proc = subprocess.run(
            full_cmd,
            shell=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            timeout=timeout,
            check=False,
            text=True,
        )
        stdout = proc.stdout.strip()
        stderr = proc.stderr.strip()
        parsed = try_parse_json(stdout)
        if parsed is None:
            # Retry without JSON flag to capture raw output
            logger.info("Holehe JSON parse failed; retrying without -j flag")
            full_cmd = f"{holehe_cmd} {shlex.quote(email)}"
            proc = subprocess.run(
                full_cmd,
                shell=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                timeout=timeout,
                check=False,
                text=True,
            )
            stdout = proc.stdout.strip()
            stderr = proc.stderr.strip()
        else:
            stderr = stderr
        return {
            "available": True,
            "returncode": proc.returncode,
            "json": parsed,
            "stdout": stdout,
            "stderr": stderr,
        }
    except subprocess.TimeoutExpired as exc:
        return {
            "available": True,
            "returncode": None,
            "json": None,
            "stdout": "",
            "stderr": f"timeout: {exc}",
        }