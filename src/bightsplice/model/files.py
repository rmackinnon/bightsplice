from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path


@dataclass(frozen=True, slots=True)
class SourceFile:
    """A file as it exists in one input pack."""

    relative_path: Path
    absolute_path: Path
    source_pack: str
    digest: str
    is_python: bool


@dataclass(slots=True)
class FilePack:
    """Inventory of one source pack."""

    name: str
    root: Path
    files: dict[Path, SourceFile] = field(default_factory=dict)


@dataclass(slots=True)
class ProjectFile:
    """A destination path and all source candidates for that path."""

    relative_path: Path
    sources: list[SourceFile] = field(default_factory=list)

    @property
    def collision(self) -> bool:
        return len(self.sources) > 1

    @property
    def identical(self) -> bool:
        return bool(self.sources) and len({item.digest for item in self.sources}) == 1
