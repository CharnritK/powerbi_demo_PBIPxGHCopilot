"""Authentication entrypoints used by scripts and notebooks."""

from src.auth.delegated_user import acquire_delegated_access_token, get_delegated_user_token
from src.auth.service_principal import (
    acquire_service_principal_access_token,
    get_service_principal_token,
)
from src.config.loader import validate_auth_mode
from src.config.models import RuntimeSettings


def get_access_token(
    settings: RuntimeSettings,
    auth_mode: str,
    use_device_code: bool | None = None,
    login_hint: str | None = None,
) -> str:
    normalized = validate_auth_mode(auth_mode)
    if normalized == "delegated":
        return acquire_delegated_access_token(
            settings=settings,
            use_device_code=use_device_code,
            login_hint=login_hint,
        )
    return acquire_service_principal_access_token(settings)


__all__ = [
    "acquire_delegated_access_token",
    "acquire_service_principal_access_token",
    "get_access_token",
    "get_delegated_user_token",
    "get_service_principal_token",
]
