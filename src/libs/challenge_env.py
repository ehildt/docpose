import os
from typing import Tuple

def get_env_from_os(value: str):
    if isinstance(value, str) and value.startswith("$"):
        res = value.split("$", 1)
        value = os.getenv(res.pop(), value)
    return value

def get_env_var_from_line(line: str) -> Tuple[str, str]:
    key, value = line.split("=", 1)
    return (key, get_env_from_os(value))