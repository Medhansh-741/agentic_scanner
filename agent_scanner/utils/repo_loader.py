import os
import tempfile
from pathlib import Path
from git import Repo
from urllib.parse import urlparse


def is_github_url(target: str) -> bool:
    try:
        parsed = urlparse(target)
        return parsed.scheme in ("http", "https") and "github.com" in parsed.netloc
    except Exception:
        return False


def load_repository(target: str) -> Path:
    """
    If local path -> validate and return Path
    If GitHub URL -> clone to temp directory and return Path
    """

    # Local path case
    if os.path.exists(target):
        return Path(target).resolve()

    # GitHub case
    if is_github_url(target):
        temp_dir = tempfile.mkdtemp()
        Repo.clone_from(target, temp_dir)
        return Path(temp_dir).resolve()

    raise ValueError("Invalid target. Provide a local path or GitHub repo URL.")
