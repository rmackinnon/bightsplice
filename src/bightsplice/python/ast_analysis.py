from __future__ import annotations

import ast
import hashlib
from pathlib import Path

from bightsplice.model.python import (
    ImportReference,
    PythonModule,
    Symbol,
    SymbolKind,
)


class ASTAnalyzer:
    """Fast semantic inventory built on Python's standard AST."""

    def analyze(self, path: Path, project_root: Path) -> PythonModule:
        source = path.read_text(encoding="utf-8")
        tree = ast.parse(source, filename=str(path))

        module = PythonModule(
            relative_path=path.relative_to(project_root),
            module_name=self.module_name(path, project_root),
        )

        for node in tree.body:
            self._record_import(module, node)
            self._record_symbol(module, node, path)

        return module

    @staticmethod
    def module_name(path: Path, project_root: Path) -> str:
        relative = path.relative_to(project_root).with_suffix("")
        parts = list(relative.parts)

        if parts and parts[-1] == "__init__":
            parts.pop()

        return ".".join(parts)

    def structural_hash(self, node: ast.AST) -> str:
        representation = ast.dump(
            node,
            annotate_fields=True,
            include_attributes=False,
        )
        return hashlib.sha256(representation.encode("utf-8")).hexdigest()

    def _record_import(self, module: PythonModule, node: ast.AST) -> None:
        if isinstance(node, ast.Import):
            module.imports.append(
                ImportReference(
                    module=None,
                    names=tuple(alias.name for alias in node.names),
                    level=0,
                    line=node.lineno,
                )
            )
        elif isinstance(node, ast.ImportFrom):
            module.imports.append(
                ImportReference(
                    module=node.module,
                    names=tuple(alias.name for alias in node.names),
                    level=node.level,
                    line=node.lineno,
                )
            )

    def _record_symbol(
        self,
        module: PythonModule,
        node: ast.AST,
        source_file: Path,
    ) -> None:
        symbol: Symbol | None = None

        if isinstance(node, ast.ClassDef):
            symbol = self._symbol(node.name, SymbolKind.CLASS, node, source_file)
        elif isinstance(node, ast.FunctionDef):
            symbol = self._symbol(
                node.name,
                SymbolKind.FUNCTION,
                node,
                source_file,
            )
        elif isinstance(node, ast.AsyncFunctionDef):
            symbol = self._symbol(
                node.name,
                SymbolKind.ASYNC_FUNCTION,
                node,
                source_file,
            )
        elif isinstance(node, (ast.Assign, ast.AnnAssign)):
            for name in self._assignment_names(node):
                current = self._symbol(
                    name,
                    SymbolKind.ASSIGNMENT,
                    node,
                    source_file,
                )
                module.symbols.setdefault(name, []).append(current)
            return

        if symbol != None:
            module.symbols.setdefault(symbol.name, []).append(symbol)

    def _symbol(
        self,
        name: str,
        kind: SymbolKind,
        node: ast.AST,
        source_file: Path,
    ) -> Symbol:
        return Symbol(
            name=name,
            kind=kind,
            source_file=source_file,
            line=getattr(node, "lineno", 0),
            structural_hash=self.structural_hash(node),
        )

    @staticmethod
    def _assignment_names(node: ast.Assign | ast.AnnAssign) -> tuple[str, ...]:
        targets: list[ast.expr]

        if isinstance(node, ast.Assign):
            targets = list(node.targets)
        else:
            targets = [node.target]

        names: list[str] = []

        for target in targets:
            if isinstance(target, ast.Name):
                names.append(target.id)
            elif isinstance(target, (ast.Tuple, ast.List)):
                names.extend(
                    item.id
                    for item in target.elts
                    if isinstance(item, ast.Name)
                )

        return tuple(names)
