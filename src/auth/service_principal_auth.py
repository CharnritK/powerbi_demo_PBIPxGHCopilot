from src.auth.service_principal import acquire_service_principal_access_token
from src.common.errors import AuthError as ServicePrincipalAuthError

__all__ = ["ServicePrincipalAuthError", "acquire_service_principal_access_token"]
