from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True, slots=True)
class MergeConfig:
    """Runtime configuration for a bightsplice merge."""

    sources: tuple[Path, ...]
    destination: Path
    dry_run: bool = True
    collision_policy: str = "merge"
    import_fix_policy: str = "safe"

    def __post_init__(self) -> None:
        if len(self.sources) < 2:
            raise ValueError("bightsplice requires at least two source packs")

        if self.collision_policy not in {"merge", "first", "last", "error"}:
            raise ValueError(
                f"unsupported collision policy: {self.collision_policy}"
            )

        if self.import_fix_policy not in {"safe", "report", "off"}:
            raise ValueError(
                f"unsupported import-fix policy: {self.import_fix_policy}"
            )
