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
    classes = [node for node in tree.body if isinstance(node, ast.ClassDef)]
    if not classes:
        violations.append(f"{path.relative_to(ROOT)}: arquivo sem classe Controller")
    for module in imports(tree):
        if module.startswith(("models", "repositories", "extensions")) or module.startswith("sqlalchemy"):
            violations.append(f"{path.relative_to(ROOT)}: import proibido {module}")
    if re.search(r"\btext\s*\(|\bCALL\s+sp_", source, re.I):
        violations.append(f"{path.relative_to(ROOT)}: contém SQL/CALL")
    for classe in classes:
        if not classe.name.endswith("Controller"):
            violations.append(f"{path.relative_to(ROOT)}:{classe.lineno}: classe não termina em Controller")
        for metodo in (n for n in classe.body if isinstance(n, (ast.FunctionDef, ast.AsyncFunctionDef))):
            decoradores = [
                ast.unparse(decorador.func if isinstance(decorador, ast.Call) else decorador)
                for decorador in metodo.decorator_list
            ]
            if "staticmethod" not in decoradores:
                violations.append(f"{path.relative_to(ROOT)}:{metodo.lineno}: {metodo.name} não é estático")

for path in python_files(BACKEND / "services"):
    if "externos" in path.parts:
        continue
    tree = ast.parse(path.read_text(encoding="utf-8-sig"))
    source = path.read_text(encoding="utf-8-sig")
    for module in imports(tree):
        if module == "flask" or module.startswith("flask.") or module == "sqlalchemy" or module.startswith("sqlalchemy."):
            violations.append(f"{path.relative_to(ROOT)}: import de camada externa {module}")
    if re.search(r"\bCALL\s+sp_", source, re.I):
        violations.append(f"{path.relative_to(ROOT)}: contém CALL")
    for node in ast.walk(tree):
        if isinstance(node, ast.Raise) and isinstance(node.exc, ast.Call):
            alvo = node.exc.func
            if isinstance(alvo, ast.Name) and alvo.id in {"ValueError", "PermissionError"}:
                violations.append(f"{path.relative_to(ROOT)}:{node.lineno}: lança {alvo.id}")
        if isinstance(node, ast.ClassDef) and node.name.endswith("Service"):
            public = [n.name for n in node.body if isinstance(n, (ast.FunctionDef, ast.AsyncFunctionDef)) and not n.name.startswith("_")]
            extras = [name for name in public if name not in {"__init__", "executar"}]
            if extras:
                violations.append(f"{path.relative_to(ROOT)}:{node.lineno}: {node.name} tem métodos além de executar: {', '.join(extras)}")

for path in python_files(BACKEND / "repositories"):
    source = path.read_text(encoding="utf-8-sig")
    tree = ast.parse(path.read_text(encoding="utf-8-sig"))
    if re.search(r"\.query\b|\.outerjoin\s*\(|\.join\s*\(", source):
        violations.append(f"{path.relative_to(ROOT)}: consulta ORM proibida (.query/join/outerjoin)")
    for node in ast.walk(tree):
        if isinstance(node, ast.ClassDef):
            for method in (n for n in node.body if isinstance(n, (ast.FunctionDef, ast.AsyncFunctionDef))):
                if method.name in {"criar", "atualizar", "deletar", "listar_todos", "buscar_por_id"}:
                    violations.append(f"{path.relative_to(ROOT)}:{method.lineno}: repository contém CRUD {method.name}")
                if not method.name.startswith("_") and not re.search(r"\bCALL\s+sp_", ast.get_source_segment(source, method), re.I):
                    violations.append(f"{path.relative_to(ROOT)}:{method.lineno}: {method.name} sem CALL sp_...")

if (BACKEND / "api_controller.py").exists():
    violations.append("backend/api_controller.py: módulo legado ainda existe")

for path in python_files(BACKEND):
    if "repositories" in path.parts or "tests" in path.parts:
        continue
    if re.search(r"\bCALL\s+sp_", path.read_text(encoding="utf-8-sig"), re.I):
        violations.append(f"{path.relative_to(ROOT)}: CALL fora de repositories/")

arquivo_procedures = BACKEND / "database" / "procedures.sql"
procedures_sql = set(re.findall(
    r"CREATE\s+PROCEDURE\s+(sp_\w+)",
    arquivo_procedures.read_text(encoding="utf-8-sig"),
    re.I,
))
procedures_repositories = set()
for path in python_files(BACKEND / "repositories"):
    procedures_repositories.update(re.findall(
        r"\bCALL\s+(sp_\w+)", path.read_text(encoding="utf-8-sig"), re.I
    ))
if procedures_sql - procedures_repositories:
    violations.append(
        "procedures.sql: sem chamada em Repository: "
        + ", ".join(sorted(procedures_sql - procedures_repositories))
    )
if procedures_repositories - procedures_sql:
    violations.append(
        "repositories/: procedures não definidas no SQL: "
        + ", ".join(sorted(procedures_repositories - procedures_sql))
    )

if violations:
    print("VIOLAÇÕES DE ARQUITETURA:")
    print("\n".join(f"- {item}" for item in sorted(set(violations))))
    sys.exit(1)
print("Arquitetura válida.")
