"""Custom error types used across the repository."""


class ConfigurationError(ValueError):
    """Raised when repository configuration cannot be resolved."""


class AuthError(RuntimeError):
    """Raised when authentication cannot complete successfully."""


class PowerBIAPIError(RuntimeError):
    """Raised when the Power BI REST API returns an actionable failure."""


class MCPError(RuntimeError):
    """Raised when a local MCP operation fails."""


class SemanticModelValidationError(RuntimeError):
    """Raised when semantic model validation cannot continue."""
