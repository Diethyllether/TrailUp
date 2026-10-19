"""Verificações estáticas dos limites de camada exigidos pelo projeto."""
from pathlib import Path
import ast
import re
import sys

ROOT = Path(__file__).resolve().parents[1]
BACKEND = ROOT / "backend"
violations = []


def python_files(folder):
    return [p for p in folder.rglob("*.py") if "__pycache__" not in p.parts]


def imports(tree):
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            for name in node.names:
                yield name.name
        elif isinstance(node, ast.ImportFrom):
            yield node.module or ""


for path in python_files(BACKEND / "controllers"):
    if path.name == "__init__.py":
        continue
    tree = ast.parse(path.read_text(encoding="utf-8-sig"))
    source = path.read_text(encoding="utf-8-sig")
    if not any(isinstance(node, ast.ClassDef) for node in tree.body):
        violations.append(f"{path.relative_to(ROOT)}: arquivo sem classe Controller")
    for module in imports(tree):
        if module.startswith(("models", "repositories", "extensions")) or module.startswith("sqlalchemy"):
            violations.append(f"{path.relative_to(ROOT)}: import proibido {module}")
    if re.search(r"\btext\s*\(|\bCALL\s+sp_", source, re.I):
        violations.append(f"{path.relative_to(ROOT)}: contém SQL/CALL")

for path in python_files(BACKEND / "services"):
    if "externos" in path.parts:
        continue
    tree = ast.parse(path.read_text(encoding="utf-8-sig"))
    source = path.read_text(encoding="utf-8-sig")
    for module in imports(tree):
        if module == "flask" or module.startswith("flask.") or module == "sqlalchemy.sql":
            violations.append(f"{path.relative_to(ROOT)}: import de camada externa {module}")
    if re.search(r"\bCALL\s+sp_", source, re.I):
        violations.append(f"{path.relative_to(ROOT)}: contém CALL")
    for node in ast.walk(tree):
        if isinstance(node, ast.ClassDef) and node.name.endswith("Service"):
            public = [n.name for n in node.body if isinstance(n, (ast.FunctionDef, ast.AsyncFunctionDef)) and not n.name.startswith("_")]
            extras = [name for name in public if name not in {"__init__", "executar"}]
            if extras:
                violations.append(f"{path.relative_to(ROOT)}:{node.lineno}: {node.name} tem métodos além de executar: {', '.join(extras)}")

for path in python_files(BACKEND / "repositories"):
    tree = ast.parse(path.read_text(encoding="utf-8-sig"))
    for node in ast.walk(tree):
        if isinstance(node, ast.ClassDef):
            for method in (n for n in node.body if isinstance(n, (ast.FunctionDef, ast.AsyncFunctionDef))):
                if method.name in {"criar", "atualizar", "deletar", "listar_todos", "buscar_por_id"}:
                    violations.append(f"{path.relative_to(ROOT)}:{method.lineno}: repository contém CRUD {method.name}")

for path in python_files(BACKEND):
    if "repositories" in path.parts:
        continue
    if re.search(r"\bCALL\s+sp_", path.read_text(encoding="utf-8-sig"), re.I):
        violations.append(f"{path.relative_to(ROOT)}: CALL fora de repositories/")

if violations:
    print("VIOLAÇÕES DE ARQUITETURA:")
    print("\n".join(f"- {item}" for item in sorted(set(violations))))
    sys.exit(1)
print("Arquitetura válida.")
