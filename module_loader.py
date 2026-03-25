"""Lazy loading and discovery of analytical modules."""

from typing import Optional

from models import AnalyticalModule


class ModuleRegistry:
    """Registry for discovering and loading analytical modules."""

    def __init__(self):
        """Initialize module registry."""
        self._modules: dict[str, AnalyticalModule] = {}
        self._loaded_modules: dict[str, any] = {}
        self._register_default_modules()

    def _register_default_modules(self) -> None:
        """Register built-in analytical modules."""
        self._modules["market_analysis"] = AnalyticalModule(
            name="market_analysis",
            description="Analyze market trends, growth drivers, and opportunity sizing",
            keywords=["market", "industry", "trend", "TAM", "segment"],
            compact_tokens=800,
            full_tokens=2100,
            ttl_seconds=604800,  # 7 days
        )

        self._modules["competitor_review"] = AnalyticalModule(
            name="competitor_review",
            description="Competitive analysis, positioning, and strategy assessment",
            keywords=["competitor", "competitive", "positioning", "vs"],
            compact_tokens=750,
            full_tokens=1950,
            ttl_seconds=604800,  # 7 days
        )

        self._modules["risk_assessment"] = AnalyticalModule(
            name="risk_assessment",
            description="Risk identification, quantification, and mitigation strategies",
            keywords=["risk", "threat", "compliance", "mitigation"],
            compact_tokens=900,
            full_tokens=2300,
            ttl_seconds=2592000,  # 30 days
        )

        self._modules["technical_audit"] = AnalyticalModule(
            name="technical_audit",
            description="Technical architecture, scalability, and implementation review",
            keywords=["architecture", "technical", "design", "infrastructure"],
            compact_tokens=850,
            full_tokens=2200,
            ttl_seconds=604800,  # 7 days
        )

    def register_module(self, module_metadata: AnalyticalModule) -> None:
        """
        Register a new analytical module.

        Args:
            module_metadata: AnalyticalModule metadata
        """
        self._modules[module_metadata.name] = module_metadata

    def load_module(self, module_name: str) -> Optional[any]:
        """
        Lazy-load an analytical module on demand.

        Args:
            module_name: Name of module to load

        Returns:
            Loaded module instance, or None if not found
        """
        if module_name not in self._modules:
            return None

        # Return cached module if already loaded
        if module_name in self._loaded_modules:
            return self._loaded_modules[module_name]

        # Dynamically import module
        try:
            module_path = f"modules.{module_name}"
            __import__(module_path)
            import sys
            module = sys.modules[module_path]
            self._loaded_modules[module_name] = module
            return module
        except ImportError:
            return None

    def get_module_metadata(self, module_name: str) -> Optional[AnalyticalModule]:
        """
        Get metadata for a module without loading it.

        Args:
            module_name: Name of module

        Returns:
            AnalyticalModule metadata or None
        """
        return self._modules.get(module_name)

    def get_compact_summary(self, module_name: str) -> dict:
        """
        Get compact pattern card for a module (without full framework).

        Returns 60% smaller summary with key decision points.

        Args:
            module_name: Name of module

        Returns:
            Dictionary with compact analysis summary
        """
        metadata = self._modules.get(module_name)
        if not metadata:
            return {}

        return {
            "module": module_name,
            "description": metadata.description,
            "compact_tokens": metadata.compact_tokens,
            "full_tokens": metadata.full_tokens,
            "token_savings": metadata.token_savings(),
            "savings_percentage": f"{metadata.savings_percentage():.1f}%",
            "ttl_seconds": metadata.ttl_seconds,
            "framework_type": "compact",
        }

    def get_full_framework(self, module_name: str) -> dict:
        """
        Get full framework for a module.

        Args:
            module_name: Name of module

        Returns:
            Dictionary with full analysis framework
        """
        metadata = self._modules.get(module_name)
        if not metadata:
            return {}

        return {
            "module": module_name,
            "description": metadata.description,
            "keywords": metadata.keywords,
            "compact_tokens": metadata.compact_tokens,
            "full_tokens": metadata.full_tokens,
            "ttl_seconds": metadata.ttl_seconds,
            "framework_type": "full",
        }

    def list_modules(self) -> list[str]:
        """
        Get list of all registered modules.

        Returns:
            List of module names
        """
        return list(self._modules.keys())

    def get_all_metadata(self) -> dict[str, AnalyticalModule]:
        """
        Get metadata for all registered modules.

        Returns:
            Dictionary mapping module names to metadata
        """
        return self._modules.copy()

    def unload_module(self, module_name: str) -> None:
        """
        Unload a loaded module (free memory).

        Args:
            module_name: Name of module to unload
        """
        if module_name in self._loaded_modules:
            del self._loaded_modules[module_name]

    def unload_all_modules(self) -> None:
        """Unload all loaded modules."""
        self._loaded_modules.clear()
