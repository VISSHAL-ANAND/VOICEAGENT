import pytest

from app.config import Settings


def test_settings_default_to_local_mock_mode_and_local_exposure() -> None:
    settings = Settings.from_env({})

    assert settings.mode == "local-mock"
    assert settings.log_level == "INFO"
    assert settings.exposure == "local"
    assert settings.api_token is None


def test_settings_normalize_log_level() -> None:
    settings = Settings.from_env({"LOG_LEVEL": "warning"})

    assert settings.log_level == "WARNING"


def test_live_mode_is_rejected_until_integrations_exist() -> None:
    with pytest.raises(ValueError, match="Only VOICEAGENT_MODE=local-mock"):
        Settings.from_env({"VOICEAGENT_MODE": "production"})


def test_invalid_log_level_is_rejected() -> None:
    with pytest.raises(ValueError, match="LOG_LEVEL"):
        Settings.from_env({"LOG_LEVEL": "LOUD"})


def test_invalid_exposure_is_rejected() -> None:
    with pytest.raises(ValueError, match="VOICEAGENT_EXPOSURE"):
        Settings.from_env({"VOICEAGENT_EXPOSURE": "public"})


def test_remote_exposure_requires_long_token() -> None:
    with pytest.raises(ValueError, match="at least 32 characters"):
        Settings.from_env({"VOICEAGENT_EXPOSURE": "remote", "VOICEAGENT_API_TOKEN": "too-short"})


def test_remote_exposure_rejects_placeholder_token() -> None:
    with pytest.raises(ValueError, match="must not be a placeholder"):
        Settings.from_env({
            "VOICEAGENT_EXPOSURE": "remote",
            "VOICEAGENT_API_TOKEN": "replace-me-with-a-secret",
        })


def test_remote_exposure_accepts_configured_token_without_returning_it_in_repr() -> None:
    token = "t" * 40
    settings = Settings.from_env({
        "VOICEAGENT_EXPOSURE": "remote",
        "VOICEAGENT_API_TOKEN": token,
    })

    assert settings.exposure == "remote"
    assert settings.api_token == token
    assert token not in repr(settings)
