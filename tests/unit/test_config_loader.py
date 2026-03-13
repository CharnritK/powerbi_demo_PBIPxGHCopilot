from __future__ import annotations

from pathlib import Path
import textwrap

import pytest

from src.config.loader import load_settings, require_dataset_id, require_group_id, validate_auth_mode


FIXTURE = Path(__file__).resolve().parents[1] / "fixtures" / "sample_config.yaml"
MISSING_ENV = Path(__file__).resolve().parents[1] / "fixtures" / ".missing.env"


def test_load_settings_from_yaml(monkeypatch: pytest.MonkeyPatch) -> None:
    for key in ("TENANT_ID", "CLIENT_ID", "CLIENT_SECRET", "WORKSPACE_ID", "DATASET_ID", "AUTH_MODE"):
        monkeypatch.delenv(key, raising=False)

    settings = load_settings(env_path=MISSING_ENV, settings_path=FIXTURE)

    assert settings.tenant_id == "tenant-from-yaml"
    assert settings.client_id == "client-from-yaml"
    assert settings.workspace_id == "workspace-from-yaml"
    assert settings.dataset_id == "dataset-from-yaml"
    assert settings.request_timeout_seconds == 45


def test_environment_overrides_yaml(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv("WORKSPACE_ID", "workspace-from-env")
    monkeypatch.setenv("AUTH_MODE", "service_principal")

    settings = load_settings(env_path=MISSING_ENV, settings_path=FIXTURE)

    assert settings.workspace_id == "workspace-from-env"
    assert settings.auth_mode == "service_principal"


def test_load_settings_uses_config_dot_env_as_fallback(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    for key in ("TENANT_ID", "CLIENT_ID", "CLIENT_SECRET", "WORKSPACE_ID", "DATASET_ID", "AUTH_MODE"):
        monkeypatch.delenv(key, raising=False)

    repo_root = tmp_path / "repo"
    config_dir = repo_root / "config"
    env_dir = config_dir / "environments"
    config_dir.mkdir(parents=True)
    env_dir.mkdir()

    (config_dir / ".env").write_text(
        textwrap.dedent(
            """
            TENANT_ID=tenant-from-config-env
            CLIENT_ID=client-from-config-env
            WORKSPACE_ID=workspace-from-config-env
            DATASET_ID=dataset-from-config-env
            AUTH_MODE=delegated
            """
        ).strip()
        + "\n",
        encoding="utf-8",
    )
    (config_dir / "settings.yaml").write_text("{}\n", encoding="utf-8")
    (env_dir / "dev.yaml").write_text("{}\n", encoding="utf-8")

    monkeypatch.setattr("src.config.loader.get_repo_root", lambda: repo_root)

    settings = load_settings()

    assert settings.tenant_id == "tenant-from-config-env"
    assert settings.client_id == "client-from-config-env"
    assert settings.workspace_id == "workspace-from-config-env"
    assert settings.dataset_id == "dataset-from-config-env"


def test_validate_auth_mode_supports_legacy_alias() -> None:
    assert validate_auth_mode("delegated_user") == "delegated"


def test_require_identifiers_raise_when_missing(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.delenv("WORKSPACE_ID", raising=False)
    monkeypatch.delenv("DATASET_ID", raising=False)
    settings = load_settings(env_path=MISSING_ENV, settings_path=FIXTURE)
    settings = settings.__class__(
        environment=settings.environment,
        auth_mode=settings.auth_mode,
        log_level=settings.log_level,
        auth=settings.auth,
        powerbi=settings.powerbi.__class__(
            workspace_id=None,
            dataset_id=None,
            dax_query=settings.dax_query,
            impersonated_user_name=settings.impersonated_user_name,
            request_timeout_seconds=settings.request_timeout_seconds,
            delegated_scopes=tuple(settings.delegated_scopes),
            service_principal_scope=settings.service_principal_scope,
        ),
        paths=settings.paths,
    )
    with pytest.raises(Exception):
        require_group_id(None, settings)
    with pytest.raises(Exception):
        require_dataset_id(None, settings)
