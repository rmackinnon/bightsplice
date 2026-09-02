from __future__ import annotations

import libcst as cst


class CSTEditor:
    """Source-preserving Python editing boundary."""

    def parse(self, source: str) -> cst.Module:
        return cst.parse_module(source)

    def render(self, module: cst.Module) -> str:
        return module.code

    def validate_round_trip(self, source: str) -> bool:
        """Confirm LibCST can parse and render a module without edits."""
        return self.render(self.parse(source)) == source
