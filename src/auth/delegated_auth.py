from src.auth.delegated_user import acquire_delegated_access_token
from src.common.errors import AuthError as DelegatedAuthError

__all__ = ["DelegatedAuthError", "acquire_delegated_access_token"]
