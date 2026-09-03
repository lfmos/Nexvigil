from __future__ import annotations

import ipaddress
import os
import time
from pathlib import Path
from urllib.parse import urlparse

import httpx
from dotenv import load_dotenv


ROOT = Path(__file__).resolve().parents[1]
ENV_FILE = ROOT / ".env"

load_dotenv(ENV_FILE)


BASE_URL = "http://127.0.0.1:8000"
USERNAME = "analyst@nexvigil.local"

VALID_PASSWORD = os.getenv("NEXVIGIL_ANALYST_PASSWORD")

if not VALID_PASSWORD:
    raise RuntimeError(
        "NEXVIGIL_ANALYST_PASSWORD is not configured. "
        "Create a local .env file based on .env.example."
    )


def ensure_local_target(base_url: str) -> None:
    parsed = urlparse(base_url)

    hostname = parsed.hostname

    if hostname == "localhost":
        return

    if not hostname:
        raise ValueError("Invalid target URL.")

    try:
        address = ipaddress.ip_address(hostname)

    except ValueError as exc:
        raise ValueError(
            "NexVigil simulations only accept localhost or loopback IPs."
        ) from exc

    if not address.is_loopback:
        raise ValueError(
            "Blocked: attack simulation may only target loopback."
        )


def main() -> None:
    ensure_local_target(BASE_URL)

    endpoint = f"{BASE_URL}/auth/login"

    print("[NexVigil] Purple Team Scenario")
    print("[NexVigil] Scenario: Failed Logins -> Successful Login")
    print(f"[NexVigil] Target: {endpoint}")
    print()

    with httpx.Client(timeout=5.0) as client:
        for number in range(1, 6):
            response = client.post(
                endpoint,
                json={
                    "username": USERNAME,
                    "password": f"wrong-password-{number}",
                },
            )

            print(
                f"Failed attempt {number:02d}: "
                f"HTTP {response.status_code}"
            )

            time.sleep(0.3)

        print()

        response = client.post(
            endpoint,
            json={
                "username": USERNAME,
                "password": VALID_PASSWORD,
            },
        )

        print(
            "Final authentication: "
            f"HTTP {response.status_code}"
        )

    print()
    print("[NexVigil] Scenario completed.")


if __name__ == "__main__":
    main()