from __future__ import annotations

from dataclasses import dataclass, field
from enum import StrEnum
from pathlib import Path


class SymbolKind(StrEnum):
    CLASS = "class"
    FUNCTION = "function"
    ASYNC_FUNCTION = "async-function"
    ASSIGNMENT = "assignment"
    IMPORT = "import"


@dataclass(frozen=True, slots=True)
class Symbol:
    name: str
    kind: SymbolKind
    source_file: Path
    line: int
    structural_hash: str


@dataclass(frozen=True, slots=True)
class ImportReference:
    module: str | None
    names: tuple[str, ...]
    level: int
    line: int


@dataclass(slots=True)
class PythonModule:
    relative_path: Path
    module_name: str
    imports: list[ImportReference] = field(default_factory=list)
    symbols: dict[str, list[Symbol]] = field(default_factory=dict)
