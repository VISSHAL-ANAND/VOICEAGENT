"""Validated, secret-free settings for the local prototype."""

import os
from dataclasses import dataclass
from typing import Mapping


@dataclass(frozen=True)
class Settings:
    mode: str = "local-mock"
    log_level: str = "INFO"

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

        return cls(mode=mode, log_level=log_level)


settings = Settings.from_env()
