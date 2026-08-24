from __future__ import annotations

import argparse
import ipaddress
import time
from urllib.parse import urlparse

import httpx


def ensure_local_target(base_url: str) -> None:
    """Refuse any non-loopback target.

    The simulator exists only to generate telemetry inside the NexVigil lab.
    """
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
            "For safety, the v0.1 simulator only accepts localhost or loopback IPs."
        ) from exc

    if not address.is_loopback:
        raise ValueError(
            "Blocked: NexVigil v0.1 attack simulation may only target loopback."
        )


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Generate synthetic failed-login telemetry for NexVigil."
    )
    parser.add_argument(
        "--base-url",
        default="http://127.0.0.1:8000",
        help="Lab API URL. Must resolve to localhost/loopback.",
    )
    parser.add_argument("--attempts", type=int, default=8)
    parser.add_argument("--delay", type=float, default=0.25)
    args = parser.parse_args()

    ensure_local_target(args.base_url)

    if args.attempts < 1 or args.attempts > 50:
        raise ValueError("Attempts must be between 1 and 50.")

    endpoint = f"{args.base_url.rstrip('/')}/auth/login"

    print("[NexVigil] Local Attack Simulation")
    print("[NexVigil] Scenario: repeated failed authentication")
    print(f"[NexVigil] Target: {endpoint}")

    with httpx.Client(timeout=5.0) as client:
        for number in range(1, args.attempts + 1):
            response = client.post(
                endpoint,
                json={
                    "username": "analyst@nexvigil.local",
                    "password": f"wrong-password-{number}",
                },
            )
            print(f"Attempt {number:02d}: HTTP {response.status_code}")
            time.sleep(args.delay)

    print("[NexVigil] Simulation completed.")


if __name__ == "__main__":
    main()
