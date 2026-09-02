from __future__ import annotations

from dataclasses import dataclass, field
from enum import StrEnum
from pathlib import Path

from bightsplice.model.files import ProjectFile
from bightsplice.project import ProjectTree


class PlannedOperation(StrEnum):
    COPY = "copy"
    DEDUPLICATE = "deduplicate"
    MERGE_PYTHON = "merge-python"
    COLLISION = "collision"


@dataclass(frozen=True, slots=True)
class PlannedFile:
    relative_path: Path
    operation: PlannedOperation
    source_count: int


@dataclass(slots=True)
class MergePlan:
    files: list[PlannedFile] = field(default_factory=list)

    @property
    def conflicts(self) -> list[PlannedFile]:
        return [
            item
            for item in self.files
            if item.operation == PlannedOperation.COLLISION
        ]


class MergePlanner:
    """Classify unified project paths before any writes occur."""

    def build(self, tree: ProjectTree) -> MergePlan:
        plan = MergePlan()

        for path in sorted(tree.files):
            project_file = tree.files[path]
            plan.files.append(self._plan_file(project_file))

        return plan

    @staticmethod
    def _plan_file(project_file: ProjectFile) -> PlannedFile:
        if not project_file.collision:
            operation = PlannedOperation.COPY
        elif project_file.identical:
            operation = PlannedOperation.DEDUPLICATE
        elif project_file.relative_path.suffix == ".py":
            operation = PlannedOperation.MERGE_PYTHON
        else:
            operation = PlannedOperation.COLLISION

        return PlannedFile(
            relative_path=project_file.relative_path,
            operation=operation,
            source_count=len(project_file.sources),
        )
