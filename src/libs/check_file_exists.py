from pathlib import Path
from typing import List
from .custom_exceptions import NotAFileError
from .constants import DEFAULT_LOCAL_ENV_FILE


def check_files_exists(files: List[str]):
    for f in files:
        filePath = Path(f)

        if filePath.name in DEFAULT_LOCAL_ENV_FILE:
            continue

        if not filePath.exists():
            FileNotFoundError(f"{filePath.absolute()}")

        if not filePath.is_file():
            NotAFileError(f"{filePath.absolute()}")
