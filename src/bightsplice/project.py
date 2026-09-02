from __future__ import annotations

from pathlib import Path

from bightsplice.model.files import FilePack, ProjectFile


class ProjectTree:
    """Unified view of all paths contributed by the input packs."""

    def __init__(self) -> None:
        self.files: dict[Path, ProjectFile] = {}

    def add_pack(self, pack: FilePack) -> None:
        for path, source in pack.files.items():
            project_file = self.files.setdefault(
                path,
                ProjectFile(relative_path=path),
            )
            project_file.sources.append(source)

    def collisions(self) -> list[ProjectFile]:
        return [
            project_file
            for project_file in self.files.values()
            if project_file.collision
        ]
