"""Validated, secret-free settings for the local prototype and protected remote demos."""

import os
from dataclasses import dataclass, field
from typing import Mapping

from dotenv import load_dotenv

load_dotenv()


@dataclass(frozen=True)
class Settings:
    mode: str = "local-mock"
    log_level: str = "INFO"
    exposure: str = "local"
    api_token: str | None = field(default=None, repr=False)
    rate_limit_per_minute: int = 60

    @classmethod
    def from_env(cls, environ: Mapping[str, str] | None = None) -> "Settings":
        source = os.environ if environ is None else environ
        mode = source.get("VOICEAGENT_MODE", "local-mock").strip().lower()
        if mode != "local-mock":
            raise ValueError(
                "Only VOICEAGENT_MODE=local-mock is supported; live integrations are not implemented."
            )

        log_level = source.get("LOG_LEVEL", "INFO").strip().upper()
        if log_level not in {"DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"}:
            raise ValueError("LOG_LEVEL must be a standard Python logging level.")

        exposure = source.get("VOICEAGENT_EXPOSURE", "local").strip().lower()
        if exposure not in {"local", "remote"}:
            raise ValueError("VOICEAGENT_EXPOSURE must be either 'local' or 'remote'.")

        raw_rate_limit = source.get("VOICEAGENT_RATE_LIMIT_PER_MINUTE", "60").strip()
        try:
            rate_limit_per_minute = int(raw_rate_limit)
        except ValueError as exc:
            raise ValueError("VOICEAGENT_RATE_LIMIT_PER_MINUTE must be an integer from 1 to 10000.") from exc
        if not 1 <= rate_limit_per_minute <= 10_000:
            raise ValueError("VOICEAGENT_RATE_LIMIT_PER_MINUTE must be an integer from 1 to 10000.")

        api_token = source.get("VOICEAGENT_API_TOKEN", "").strip() or None
        if exposure == "remote":
            if api_token is None or len(api_token) < 32:
                raise ValueError(
                    "Remote exposure requires VOICEAGENT_API_TOKEN with at least 32 characters."
                )
            if api_token.lower() in {"change-me", "changeme", "replace-me-with-a-secret"} or api_token.lower().startswith("replace-me"):
                raise ValueError("VOICEAGENT_API_TOKEN must not be a placeholder.")

        return cls(
            mode=mode,
            log_level=log_level,
            exposure=exposure,
            api_token=api_token,
            rate_limit_per_minute=rate_limit_per_minute,
        )


settings = Settings.from_env()
