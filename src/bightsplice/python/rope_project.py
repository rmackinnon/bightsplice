from __future__ import annotations

from pathlib import Path

from rope.base.project import Project


class RopeProjectManager:
    """Lifecycle adapter around a Rope project."""

    def __init__(self, root: Path) -> None:
        self.root = root
        self._project: Project | None = None

    @property
    def project(self) -> Project:
        if self._project == None:
            raise RuntimeError("Rope project has not been opened")
        return self._project

    def open(self) -> Project:
        if self._project == None:
            self._project = Project(str(self.root))
        return self._project

    def close(self) -> None:
        if self._project != None:
            self._project.close()
            self._project = None

    def __enter__(self) -> "RopeProjectManager":
        self.open()
        return self

    def __exit__(self, exc_type, exc, traceback) -> None:
        self.close()
