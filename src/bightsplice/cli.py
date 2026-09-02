from __future__ import annotations

import argparse
from pathlib import Path

from bightsplice.config import MergeConfig
from bightsplice.merge.planner import MergePlanner
from bightsplice.project import ProjectTree
from bightsplice.scan.pack import PackScanner


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="bightsplice",
        description=(
            "Reassemble split Python project packs and reconcile collisions."
        ),
    )
    parser.add_argument(
        "sources",
        nargs="+",
        type=Path,
        help="Source pack directories.",
    )
    parser.add_argument(
        "-d",
        "--destination",
        type=Path,
        required=True,
        help="Destination project directory.",
    )
    parser.add_argument(
        "--apply",
        action="store_true",
        help="Apply the merge. Dry-run is the default.",
    )
    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)

    config = MergeConfig(
        sources=tuple(args.sources),
        destination=args.destination,
        dry_run=not args.apply,
    )

    scanner = PackScanner()
    tree = ProjectTree()

    for source_root in config.sources:
        tree.add_pack(scanner.scan(source_root))

    plan = MergePlanner().build(tree)

    print(f"bightsplice: {len(config.sources)} source packs")
    print(f"destination: {config.destination}")
    print(f"mode: {'dry-run' if config.dry_run else 'apply'}")

    for item in plan.files:
        print(
            f"[{item.operation.value.upper()}] "
            f"{item.relative_path} ({item.source_count} source(s))"
        )

    if plan.conflicts:
        print(f"{len(plan.conflicts)} unresolved non-Python collision(s)")
        return 2

    if not config.dry_run:
        print(
            "Apply mode is not implemented in this initial scaffold; "
            "no files were written."
        )
        return 3

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
