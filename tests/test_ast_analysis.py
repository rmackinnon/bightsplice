from pathlib import Path

from bightsplice.model.python import SymbolKind
from bightsplice.python.ast_analysis import ASTAnalyzer


def test_ast_analyzer_inventories_imports_and_symbols(tmp_path: Path) -> None:
    package = tmp_path / "pkg"
    package.mkdir()
    module_path = package / "example.py"
    module_path.write_text(
        "\n".join(
            [
                "from .tools import Widget",
                "VALUE = 3",
                "",
                "class Example:",
                "    pass",
                "",
                "def build():",
                "    return Example()",
                "",
            ]
        ),
        encoding="utf-8",
    )

    module = ASTAnalyzer().analyze(module_path, tmp_path)

    assert module.module_name == "pkg.example"
    assert module.imports[0].module == "tools"
    assert module.imports[0].level == 1
    assert module.imports[0].names == ("Widget",)
    assert module.symbols["Example"][0].kind == SymbolKind.CLASS
    assert module.symbols["build"][0].kind == SymbolKind.FUNCTION
    assert module.symbols["VALUE"][0].kind == SymbolKind.ASSIGNMENT
