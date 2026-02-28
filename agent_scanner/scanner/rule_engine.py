import re
from pathlib import Path


SECRET_PATTERN = re.compile(
    r"(api_key|apikey|secret|password|token)\s*=\s*['\"][^'\"]+['\"]",
    re.IGNORECASE,
)

EVAL_PATTERN = re.compile(r"\beval\s*\(")


def scan_file(file_path: Path) -> list[dict]:
    findings = []

    with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
        lines = f.readlines()

    for i, line in enumerate(lines, start=1):

        # Hardcoded secret detection
        if SECRET_PATTERN.search(line):
            findings.append({
                "type": "Hardcoded Secret",
                "severity": "HIGH",
                "file": str(file_path),
                "line": i,
                "code": line.strip(),
            })

        # Unsafe eval detection
        if EVAL_PATTERN.search(line):
            findings.append({
                "type": "Unsafe eval() usage",
                "severity": "HIGH",
                "file": str(file_path),
                "line": i,
                "code": line.strip(),
            })

    return findings
