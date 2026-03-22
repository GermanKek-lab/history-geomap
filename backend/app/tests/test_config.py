import importlib


def _reload_config_module():
    import app.core.config as config

    return importlib.reload(config)


def test_settings_parse_comma_separated_cors_origins_from_env(monkeypatch) -> None:
    monkeypatch.setenv("CORS_ORIGINS", "http://localhost:5173,http://localhost:8080")

    config = _reload_config_module()
    settings = config.Settings(_env_file=None)

    assert settings.cors_origins == ["http://localhost:5173", "http://localhost:8080"]


def test_settings_parse_json_cors_origins_from_env(monkeypatch) -> None:
    monkeypatch.setenv("CORS_ORIGINS", '["http://localhost:5173", "http://localhost:8080"]')

    config = _reload_config_module()
    settings = config.Settings(_env_file=None)

    assert settings.cors_origins == ["http://localhost:5173", "http://localhost:8080"]
