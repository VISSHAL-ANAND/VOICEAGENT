import pytest

from app.config import Settings


def test_settings_default_to_local_mock_mode() -> None:
    settings = Settings.from_env({})

    assert settings.mode == "local-mock"
    assert settings.log_level == "INFO"


def test_settings_normalize_log_level() -> None:
    settings = Settings.from_env({"LOG_LEVEL": "warning"})

    assert settings.log_level == "WARNING"


def test_live_mode_is_rejected_until_integrations_exist() -> None:
    with pytest.raises(ValueError, match="Only VOICEAGENT_MODE=local-mock"):
        Settings.from_env({"VOICEAGENT_MODE": "production"})


def test_invalid_log_level_is_rejected() -> None:
    with pytest.raises(ValueError, match="LOG_LEVEL"):
        Settings.from_env({"LOG_LEVEL": "LOUD"})
