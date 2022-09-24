"""Git Utilities."""

from pathlib import Path
from typing import Optional

from ._util import run
from .exceptions import NoGitError


def get_repo_top(path: Optional[Path]):
    """Determine Git Clone Repository Top Directory."""
    path = path or Path.cwd()
    result = run(("git", "rev-parse", "--show-cdup"), capture_output=True, check=False)
    if result.stderr:
        raise NoGitError()
    cdup = result.stdout.decode("utf-8").strip()
    return (path / cdup).resolve()
