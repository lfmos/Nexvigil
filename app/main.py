from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Literal

from fastapi import FastAPI, Request
from pydantic import BaseModel, Field

APP_ROOT = Path(__file__).resolve().parents[1]
LOG_DIR = APP_ROOT / "logs"
EVENT_FILE = LOG_DIR / "security_events.jsonl"
LOG_DIR.mkdir(parents=True, exist_ok=True)

app = FastAPI(
    title="NexVigil Lab API",
    version="0.1.0",
    description="Synthetic security telemetry generator for the NexVigil lab.",
)

# Synthetic demo accounts only.
DEMO_USERS = {
    "analyst@nexvigil.local": "PurpleTeam!2026",
    "developer@nexvigil.local": "DevSecOps!2026",
}


class LoginRequest(BaseModel):
    username: str = Field(min_length=3, max_length=120)
    password: str = Field(min_length=1, max_length=200)


class LoginResponse(BaseModel):
    status: Literal["success", "failed"]


def write_event(event: dict) -> None:
    """Append a sanitized security event as one JSON line."""
    with EVENT_FILE.open("a", encoding="utf-8") as handle:
        handle.write(json.dumps(event, ensure_ascii=False) + "\n")


@app.get("/health")
def health() -> dict:
    return {"status": "ok", "service": "nexvigil-lab-api", "version": "0.1.0"}


@app.post("/auth/login", response_model=LoginResponse)
def login(payload: LoginRequest, request: Request) -> LoginResponse:
    client_ip = request.client.host if request.client else "unknown"
    valid = DEMO_USERS.get(payload.username) == payload.password

    # Password is intentionally NEVER logged.
    event = {
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "event_type": "authentication",
        "action": "login",
        "result": "success" if valid else "failed",
        "username": payload.username,
        "source_ip": client_ip,
        "service": "nexvigil-lab-api",
    }
    write_event(event)

    return LoginResponse(status="success" if valid else "failed")
