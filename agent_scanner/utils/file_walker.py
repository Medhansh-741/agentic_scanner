from pathlib import Path


EXCLUDED_DIRS = {
    ".git",
    "venv",
    "__pycache__",
    ".mypy_cache",
    ".pytest_cache",
    "agent_scanner",
}

def get_python_files(repo_path: Path) -> list[Path]:
    python_files = []

    for path in repo_path.rglob("*.py"):
        if any(part in EXCLUDED_DIRS for part in path.parts):
            continue
        python_files.append(path)

    return python_files
