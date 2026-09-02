from pathlib import Path

from bightsplice.merge.planner import MergePlanner, PlannedOperation
from bightsplice.project import ProjectTree
from bightsplice.scan.pack import PackScanner


def test_plan_detects_unique_identical_python_and_binary_collisions(
    tmp_path: Path,
) -> None:
    pack_a = tmp_path / "pack-a"
    pack_b = tmp_path / "pack-b"
    pack_a.mkdir()
    pack_b.mkdir()

    (pack_a / "unique.py").write_text("A = 1\n", encoding="utf-8")
    (pack_a / "same.txt").write_text("same\n", encoding="utf-8")
    (pack_b / "same.txt").write_text("same\n", encoding="utf-8")

    (pack_a / "module.py").write_text("A = 1\n", encoding="utf-8")
    (pack_b / "module.py").write_text("B = 2\n", encoding="utf-8")

    (pack_a / "data.bin").write_bytes(b"a")
    (pack_b / "data.bin").write_bytes(b"b")

    scanner = PackScanner()
    tree = ProjectTree()
    tree.add_pack(scanner.scan(pack_a))
    tree.add_pack(scanner.scan(pack_b))

    plan = MergePlanner().build(tree)
    operations = {
        item.relative_path: item.operation
        for item in plan.files
    }

    assert operations[Path("unique.py")] == PlannedOperation.COPY
    assert operations[Path("same.txt")] == PlannedOperation.DEDUPLICATE
    assert operations[Path("module.py")] == PlannedOperation.MERGE_PYTHON
    assert operations[Path("data.bin")] == PlannedOperation.COLLISION
