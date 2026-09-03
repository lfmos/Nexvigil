from __future__ import annotations

import json
import os
from datetime import datetime, timezone
from pathlib import Path
from typing import Literal

from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException, Request, status
from pydantic import BaseModel, Field


APP_ROOT = Path(__file__).resolve().parents[1]
LOG_DIR = APP_ROOT / "logs"
EVENT_FILE = LOG_DIR / "security_events.jsonl"
ENV_FILE = APP_ROOT / ".env"

LOG_DIR.mkdir(parents=True, exist_ok=True)

# Carrega variáveis locais do arquivo .env.
load_dotenv(ENV_FILE)


app = FastAPI(
    title="NexVigil Lab API",
    version="0.1.1",
    description="Synthetic security telemetry generator for the NexVigil lab.",
)


def get_demo_users() -> dict[str, str]:
    """
    Carrega credenciais sintéticas do laboratório através
    de variáveis de ambiente.

    Nenhuma senha deve permanecer hardcoded no código-fonte.
    """

    analyst_password = os.getenv("NEXVIGIL_ANALYST_PASSWORD")
    developer_password = os.getenv("NEXVIGIL_DEVELOPER_PASSWORD")

    if not analyst_password or not developer_password:
        raise RuntimeError(
            "NexVigil demo credentials are not configured. "
            "Create a local .env file based on .env.example."
        )

    return {
        "analyst@nexvigil.local": analyst_password,
        "developer@nexvigil.local": developer_password,
    }


class LoginRequest(BaseModel):
    username: str = Field(min_length=3, max_length=120)
    password: str = Field(min_length=1, max_length=200)


class LoginResponse(BaseModel):
    status: Literal["success"]


def write_event(event: dict) -> None:
    """
    Grava um evento de segurança sanitizado no arquivo JSONL.

    Senhas, tokens e outras credenciais nunca devem ser
    incluídos na telemetria.
    """

    with EVENT_FILE.open("a", encoding="utf-8") as handle:
        handle.write(json.dumps(event, ensure_ascii=False) + "\n")


@app.get("/health")
def health() -> dict:
    return {
        "status": "ok",
        "service": "nexvigil-lab-api",
        "version": "0.1.1",
    }


@app.post("/auth/login", response_model=LoginResponse)
def login(payload: LoginRequest, request: Request) -> LoginResponse:
    client_ip = request.client.host if request.client else "unknown"

    demo_users = get_demo_users()

    valid = demo_users.get(payload.username) == payload.password

    event = {
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "event_type": "authentication",
        "action": "login",
        "result": "success" if valid else "failed",
        "username": payload.username,
        "source_ip": client_ip,
        "service": "nexvigil-lab-api",
    }

    # A senha nunca é incluída no evento.
    write_event(event)

    if not valid:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid credentials",
        )

    return LoginResponse(status="success")