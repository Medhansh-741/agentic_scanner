import ast
from pathlib import Path


class VulnerabilityVisitor(ast.NodeVisitor):
    def __init__(self, file_path: Path):
        self.file_path = file_path
        self.findings = []

    def visit_Call(self, node):
        # Detect eval()
        if isinstance(node.func, ast.Name) and node.func.id == "eval":
            self.findings.append({
                "type": "Unsafe eval() usage (AST)",
                "severity": "HIGH",
                "file": str(self.file_path),
                "line": node.lineno,
                "code": "eval(...)",
            })

        # Detect exec()
        if isinstance(node.func, ast.Name) and node.func.id == "exec":
            self.findings.append({
                "type": "Unsafe exec() usage (AST)",
                "severity": "HIGH",
                "file": str(self.file_path),
                "line": node.lineno,
                "code": "exec(...)",
            })

        # Detect pickle.loads()
        if isinstance(node.func, ast.Attribute):
            if node.func.attr == "loads":
                if isinstance(node.func.value, ast.Name) and node.func.value.id == "pickle":
                    self.findings.append({
                        "type": "Insecure deserialization (pickle.loads)",
                        "severity": "HIGH",
                        "file": str(self.file_path),
                        "line": node.lineno,
                        "code": "pickle.loads(...)",
                    })

        self.generic_visit(node)


def scan_file_ast(file_path: Path) -> list[dict]:
    findings = []

    try:
        with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
            source = f.read()

        tree = ast.parse(source)
        visitor = VulnerabilityVisitor(file_path)
        visitor.visit(tree)
        findings.extend(visitor.findings)

    except Exception:
        pass  # Ignore parse errors

    return findings
