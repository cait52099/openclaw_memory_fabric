"""Base adapter interface for OCMF.

This module defines the universal contract that all tool adapters must implement.
"""
from abc import ABC, abstractmethod
from typing import Any, Dict, List, Optional, Protocol, runtime_checkable


# =============================================================================
# Adapter Contract - Protocol Definition
# =============================================================================

@runtime_checkable
class AdapterProtocol(Protocol):
    """Universal Adapter Contract.

    All tool adapters MUST implement this protocol.
    This ensures interoperability between different AI tools.
    """

    def get_name(self) -> str:
        """Get adapter name.

        Returns:
            Unique tool name (e.g., 'claude-code', 'openclaw', 'codex-cli')
        """
        ...

    def get_scope_from_context(self, context: Dict[str, Any]) -> Dict[str, Any]:
        """Extract scope from tool context.

        Args:
            context: Tool-specific context dict

        Returns:
            Scope dict with keys: user, workspace, project, session, tool
        """
        ...

    def before_response(self, query: str, context: Dict[str, Any]) -> str:
        """Recall hook - called before generating response.

        Args:
            query: User query/input
            context: {user, workspace, project, session, tool, ...}

        Returns:
            injection_text: Text to inject into LLM context
        """
        ...

    def after_response(
        self,
        query: str,
        response: str,
        context: Dict[str, Any],
    ) -> str:
        """Remember hook - called after generating response.

        Args:
            query: User query/input
            response: AI response
            context: {user, workspace, project, session, tool, ...}

        Returns:
            event_id: Remembered event ID, or empty string on failure
        """
        ...


    def before_task(self, task: str, context: Dict[str, Any]) -> str:
        """Optional: Task recall hook.

        Called before executing a task.
        """
        ...

    def after_task(
        self,
        task: str,
        result: str,
        success: bool,
        context: Dict[str, Any],
    ) -> str:
        """Optional: Task remember hook.

        Called after task execution.
        """
        ...

    def get_injection_policy(self) -> "InjectionPolicy":
        """Optional: Get tool-specific injection policy.

        Returns:
            InjectionPolicy instance, or None for default
        """
        ...


    def get_supported_scopes(self) -> List[str]:
        """Optional: List of scope levels this adapter supports.

        Returns:
            List of supported scope keys
        """
        ...


    def get_default_scope(self) -> Dict[str, Optional[str]]:
        """Optional: Get default scope values.

        Returns:
            Default scope dict
        """
        ...


    def validate_context(self, context: Dict[str, Any]) -> bool:
        """Optional: Validate context has required fields.

        Args:
            context: Context dict to validate

        Returns:
            True if valid, False otherwise
        """
        ...


    def get_error_strategy(self) -> str:
        """Optional: Get error handling strategy.

        Returns:
            'fail-open' or 'fail-close'
        """
        ...


    def get_version(self) -> str:
        """Optional: Get adapter version.

        Returns:
            Semantic version string
        """
        ...


    def health_check(self) -> Dict[str, Any]:
        """Optional: Check adapter health.

        Returns:
            Health status dict
        """
        ...


    def shutdown(self) -> None:
        """Optional: Clean up resources."""
        ...


    def get_capabilities(self) -> Dict[str, bool]:
        """Optional: Get adapter capabilities.

        Returns:
            Dict of capability_name -> supported
        """
        ...


    def get_required_context_fields(self) -> List[str]:
        """Optional: List of required context fields.

        Returns:
            List of required field names
        """
        ...


    def get_optional_context_fields(self) -> List[str]:
        """Optional: List of optional context fields.

        Returns:
            List of optional field names
        """
        ...


    def get_context_field_defaults(self) -> Dict[str, Any]:
        """Optional: Get default values for context fields.

        Returns:
            Dict of field_name -> default_value
        """
        ...


    def serialize_injection(self, injection_text: str) -> str:
        """Optional: Serialize injection text for transport.

        Args:
            injection_text: Raw injection text

        Returns:
            Serialized text
        """
        ...

    def deserialize_injection(self, serialized: str) -> str:
        """Optional: Deserialize injection text.

        Args:
            serialized: Serialized text

        Returns:
            Raw injection text
        """
        ...


    def truncate_injection(self, injection_text: str, max_length: int) -> str:
        """Optional: Truncate injection text to max length.

        Args:
            injection_text: Text to truncate
            max_length: Maximum length

        Returns:
            Truncated text
        """
        ...


    def get_max_injection_length(self) -> int:
        """Optional: Get maximum injection length for this adapter.

        Returns:
            Max length in characters
        """
        ...


    def should_remember(self, query: str, response: str, context: Dict[str, Any]) -> bool:
        """Optional: Determine if interaction should be remembered.

        Args:
            query: User query
            response: AI response
            context: Context dict

        Returns:
            True if should remember
        """
        ...

    def should_recall(self, query: str, context: Dict[str, Any]) -> bool:
        """Optional: Determine if recall should be performed.

        Args:
            query: User query
            context: Context dict

        Returns:
            True if should recall
        """
        ...


    def enrich_context(self, context: Dict[str, Any]) -> Dict[str, Any]:
        """Optional: Enrich context with additional fields.

        Args:
            context: Original context

        Returns:
            Enriched context
        """
        ...

    def filter_injection(self, injection_text: str, context: Dict[str, Any]) -> str:
        """Optional: Filter injection text based on context.

        Args:
            injection_text: Text to filter
            context: Context dict

        Returns:
            Filtered text
        """
        ...


    def rank_injections(self, injections: List[str], context: Dict[str, Any]) -> List[str]:
        """Optional: Rank multiple injections by relevance.

        Args:
            injections: List of injection texts
            context: Context dict

        Returns:
            Ranked list (highest relevance first)
        """
        ...


    def get_injection_metadata(self) -> Dict[str, Any]:
        """Optional: Get metadata about injection behavior.

        Returns:
            Metadata dict
        """
        ...


    def validate_scope(self, scope: Dict[str, Any]) -> bool:
        """Optional: Validate scope dict.

        Args:
            scope: Scope dict to validate

        Returns:
            True if valid
        """
        ...


    def normalize_scope(self, scope: Dict[str, Any]) -> Dict[str, Optional[str]]:
        """Optional: Normalize scope to standard format.

        Args:
            scope: Raw scope dict

        Returns:
            Normalized scope
        """
        ...

    def expand_scope(self, scope: Dict[str, Any]) -> List[Dict[str, Optional[str]]]:
        """Optional: Expand scope to include fallback levels.

        Args:
            scope: Base scope

        Returns:
            List of scopes to try (most specific first)
        """
        ...

    def get_scope_priority(self) -> List[str]:
        """Optional: Get scope level priority order.

        Returns:
            List of scope keys in priority order
        """
        ...


    def should_use_fallback(self, recall_result: Any, context: Dict[str, Any]) -> bool:
        """Optional: Determine if fallback should be used.

        Args:
            recall_result: Result from recall
            context: Context dict

        Returns:
            True if should fallback
        """
        ...

    def get_fallback_levels(self) -> List[str]:
        """Optional: Get fallback scope levels.

        Returns:
            List of scope keys to try in order
        """
        ...


    def merge_injections(self, injections: List[str]) -> str:
        """Optional: Merge multiple injections into one.

        Args:
            injections: List of injection texts

        Returns:
            Merged text
        """
        ...


    def get_cache_ttl(self) -> int:
        """Optional: Get TTL for cached recall results.

        Returns:
            TTL in seconds
        """
        ...

    def should_use_cache(self, query: str, context: Dict[str, Any]) -> bool:
        """Optional: Determine if cache should be used.

        Args:
            query: User query
            context: Context dict

        Returns:
            True if should use cache
        """
        ...

    def invalidate_cache(self, scope: Dict[str, Any]) -> None:
        """Optional: Invalidate cache for scope.

        Args:
            scope: Scope to invalidate
        """
        ...


    def get_stats(self) -> Dict[str, Any]:
        """Optional: Get adapter statistics.

        Returns:
            Stats dict
        """
        ...

    def reset_stats(self) -> None:
        """Optional: Reset statistics."""
        ...


    def get_config(self) -> Dict[str, Any]:
        """Optional: Get adapter configuration.

        Returns:
            Config dict
        """
        ...

    def update_config(self, config: Dict[str, Any]) -> None:
        """Optional: Update adapter configuration.

        Args:
            config: New config
        """
        ...


    def validate_config(self, config: Dict[str, Any]) -> bool:
        """Optional: Validate configuration.

        Args:
            config: Config to validate

        Returns:
            True if valid
        """
        ...


    def get_schema_version(self) -> str:
        """Optional: Get contract schema version.

        Returns:
            Schema version string
        """
        ...

    def is_compatible(self, other_version: str) -> bool:
        """Optional: Check if compatible with other version.

        Args:
            other_version: Version to check

        Returns:
            True if compatible
        """
        ...


    def get_migration_path(self, from_version: str) -> Optional[List[str]]:
        """Optional: Get migration path from version.

        Args:
            from_version: Starting version

        Returns:
            List of migration steps, or None
        """
        ...


    def rollback(self, version: str) -> bool:
        """Optional: Rollback to previous version.

        Args:
            version: Version to rollback to

        Returns:
            True if successful
        """
        ...

    def get_deprecation_warnings(self) -> List[str]:
        """Optional: Get list of deprecation warnings.

        Returns:
            List of warning messages
        """
        ...

    def is_deprecated(self, method: str) -> bool:
        """Optional: Check if method is deprecated.

        Args:
            method: Method name

        Returns:
            True if deprecated
        """
        ...

    def get_alternative_method(self, deprecated: str) -> Optional[str]:
        """Optional: Get alternative for deprecated method.

        Args:
            deprecated: Deprecated method name

        Returns:
            Alternative method name
        """
        ...


    def supports_feature(self, feature: str) -> bool:
        """Optional: Check if feature is supported.

        Args:
            feature: Feature name

        Returns:
            True if supported
        """
        ...

    def get_supported_features(self) -> List[str]:
        """Optional: Get list of supported features.

        Returns:
            List of feature names
        """
        ...

    def enable_feature(self, feature: str) -> None:
        """Optional: Enable a feature.

        Args:
            feature: Feature name
        """
        ...

    def disable_feature(self, feature: str) -> None:
        """Optional: Disable a feature.

        Args:
            feature: Feature name
        """
        ...

    def get_feature_config(self, feature: str) -> Optional[Dict[str, Any]]:
        """Optional: Get configuration for feature.

        Args:
            feature: Feature name

        Returns:
            Config dict, or None
        """
        ...

    def set_feature_config(self, feature: str, config: Dict[str, Any]) -> None:
        """Optional: Set configuration for feature.

        Args:
            feature: Feature name
            config: Configuration
        """
        ...


# =============================================================================
# Context Contract - Required Fields
# =============================================================================

# Minimum required context fields
CONTEXT_REQUIRED_FIELDS = ["user"]

# All possible context fields
CONTEXT_ALL_FIELDS = [
    "user",
    "workspace",
    "project",
    "session",
    "tool",
    "timestamp",
    "metadata",
]

# Scope fields (excluding tool for isolation)
SCOPE_FIELDS = [
    "user",
    "workspace",
    "project",
    "session",
]


# =============================================================================
# Output Contract
# =============================================================================

class OutputContract:
    """Standard output formats for adapter methods."""

    @staticmethod
    def before_response_output() -> Dict[str, Any]:
        """Standard output for before_response.

        Returns:
            Dict with required keys
        """
        return {
            "injection_text": str,  # Text to inject
            "memory_count": int,     # Number of memories found
            "fallback_used": bool,   # Whether fallback was used
            "truncated": bool,       # Whether content was truncated
        }

    @staticmethod
    def after_response_output() -> Dict[str, Any]:
        """Standard output for after_response.

        Returns:
            Dict with required keys
        """
        return {
            "event_id": str,        # Remembered event ID
            "success": bool,        # Whether remember succeeded
            "error": str,           # Error message if failed
        }


# =============================================================================
# Error Handling
# =============================================================================

class AdapterError(Exception):
    """Base exception for adapter errors."""

    def __init__(self, message: str, code: str = "ADAPTER_ERROR"):
        self.message = message
        self.code = code
        super().__init__(self.message)


class ContextValidationError(AdapterError):
    """Raised when context validation fails."""

    def __init__(self, message: str):
        super().__init__(message, "CONTEXT_VALIDATION_ERROR")


class ScopeError(AdapterError):
    """Raised when scope is invalid."""

    def __init__(self, message: str):
        super().__init__(message, "SCOPE_ERROR")


class RecallError(AdapterError):
    """Raised when recall fails."""

    def __init__(self, message: str):
        super().__init__(message, "RECALL_ERROR")


class RememberError(AdapterError):
    """Raised when remember fails."""

    def __init__(self, message: str):
        super().__init__(message, "REMEMBER_ERROR")


class ConfigurationError(AdapterError):
    """Raised when configuration is invalid."""

    def __init__(self, message: str):
        super().__init__(message, "CONFIG_ERROR")


# =============================================================================
# Best-Effort Error Handling Strategy
# =============================================================================

class ErrorStrategy:
    """Error handling strategies for adapters.

    OCMF adapters follow a 'fail-open' (best-effort) strategy:
    - If recall fails, return empty injection (don't block response)
    - If remember fails, log error but continue
    - If scope is invalid, use defaults
    """

    @staticmethod
    def handle_recall_error(error: Exception, default: str = "") -> str:
        """Handle recall errors with fail-open strategy.

        Args:
            error: Exception that occurred
            default: Default return value

        Returns:
            Default value (empty string)
        """
        # Log error in production
        # import logging
        # logging.warning(f"Recall error: {error}")
        return default

    @staticmethod
    def handle_remember_error(error: Exception, default: str = "") -> str:
        """Handle remember errors with fail-open strategy.

        Args:
            error: Exception that occurred
            default: Default return value

        Returns:
            Default value (empty string)
        """
        # Log error in production
        # import logging
        # logging.warning(f"Remember error: {error}")
        return default

    @staticmethod
    def handle_context_error(error: Exception, default: Optional[Dict] = None) -> Dict:
        """Handle context errors with fail-open strategy.

        Args:
            error: Exception that occurred
            default: Default return value

        Returns:
            Default value (empty dict)
        """
        if default is None:
            default = {}
        return default


# =============================================================================
# Base Adapter (backward compatibility)
# =============================================================================

class Adapter(ABC):
    """Base class for tool adapters (backward compatibility).

    New adapters should implement AdapterProtocol directly.
    """

    def __init__(self, config: Optional[Dict[str, Any]] = None):
        """Initialize adapter with config."""
        self.config = config or {}

    @abstractmethod
    def get_name(self) -> str:
        """Get adapter name."""
        pass

    @abstractmethod
    def get_scope_from_context(self, context: Dict[str, Any]) -> Dict[str, Any]:
        """Extract scope from tool context.

        Returns dict with user/workspace/project/session/tool.
        """
        pass

    @abstractmethod
    def before_response(self, query: str, context: Dict[str, Any]) -> str:
        """Hook called before generating response.

        Returns text to inject into context.
        """
        pass

    @abstractmethod
    def after_response(
        self,
        query: str,
        response: str,
        context: Dict[str, Any],
    ) -> str:
        """Hook called after generating response.

        Returns event_id or empty string.
        """
        pass


# =============================================================================
# Injection Policy
# =============================================================================

class InjectionPolicy:
    """Policy for injecting context into LLM prompts.

    This policy prevents prompt bloat by:
    1. Using gist mode by default (prefer_gist=True)
    2. Enforcing max_length limits
    3. Limiting number of memories
    4. Supporting layered injection (system -> user -> tool)
    """

    # Default limits to prevent prompt bloat
    DEFAULT_MAX_LENGTH = 2000
    DEFAULT_MAX_MEMORIES = 5

    # Layer limits (LLM context decreases as layer goes higher)
    LAYER_LIMITS = {
        "system": 500,   # System prompt
        "user": 1500,    # User message prefix
        "tool": 2000,    # Tool context
    }

    def __init__(
        self,
        max_length: int = DEFAULT_MAX_LENGTH,
        max_memories: int = DEFAULT_MAX_MEMORIES,
        prefer_gist: bool = True,
        layer: str = "user",
    ):
        """Initialize injection policy.

        Args:
            max_length: Maximum length of injected text
            max_memories: Maximum number of memories to include
            prefer_gist: If True, use gist instead of full details
            layer: Injection layer (system/user/tool)
        """
        self.max_length = min(max_length, self.LAYER_LIMITS.get(layer, max_length))
        self.max_memories = max_memories
        self.prefer_gist = prefer_gist
        self.layer = layer

    def apply(self, recall_result) -> str:
        """Apply policy to recall result."""
        if self.prefer_gist:
            return recall_result.to_gist_text(self.max_memories)
        else:
            return recall_result.to_injection_text(self.max_length)

    def truncate(self, text: str, max_length: Optional[int] = None) -> str:
        """Truncate text to max length with ellipsis."""
        limit = max_length or self.max_length
        if len(text) > limit:
            return text[:limit] + "\n... (truncated)"
        return text

    @classmethod
    def for_layer(cls, layer: str) -> "InjectionPolicy":
        """Create policy optimized for specific layer."""
        limits = cls.LAYER_LIMITS.get(layer, cls.DEFAULT_MAX_LENGTH)
        return cls(
            max_length=limits,
            max_memories=cls.DEFAULT_MAX_MEMORIES,
            prefer_gist=True,  # Always prefer gist to prevent bloat
            layer=layer,
        )


# =============================================================================
# Adapter Metadata
# =============================================================================

ADAPTER_METADATA = {
    "contract_version": "1.0.0",
    "protocol": "AdapterProtocol",
    "context_required": CONTEXT_REQUIRED_FIELDS,
    "context_all": CONTEXT_ALL_FIELDS,
    "scope_fields": SCOPE_FIELDS,
    "error_strategy": "fail-open",
}
