from __future__ import annotations

import hashlib
from pathlib import Path

from bightsplice.model.files import FilePack, SourceFile


class PackScanner:
    """Create deterministic inventories for source packs."""

    DEFAULT_IGNORES = {
        ".git",
        ".hg",
        ".svn",
        ".mypy_cache",
        ".pytest_cache",
        ".ruff_cache",
        "__pycache__",
    }

    def __init__(self, ignores: set[str] | None = None) -> None:
        self.ignores = set(ignores or self.DEFAULT_IGNORES)

    def scan(self, root: Path) -> FilePack:
        root = root.expanduser().resolve()

        if not root.is_dir():
            raise NotADirectoryError(root)

        pack = FilePack(name=root.name, root=root)

        for path in sorted(root.rglob("*")):
            if not path.is_file():
                continue

            relative = path.relative_to(root)

            if any(part in self.ignores for part in relative.parts):
                continue

            pack.files[relative] = SourceFile(
                relative_path=relative,
                absolute_path=path,
                source_pack=pack.name,
                digest=self._digest(path),
                is_python=path.suffix == ".py",
            )

        return pack

    @staticmethod
    def _digest(path: Path) -> str:
        hasher = hashlib.sha256()

        with path.open("rb") as handle:
            for chunk in iter(lambda: handle.read(1024 * 1024), b""):
                hasher.update(chunk)

        return hasher.hexdigest()
