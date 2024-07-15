from pathlib import Path
from typing import List, Dict
from .constants import DEFAULT_LOCAL_ENV_FILE
from .parse_env_file import parse_env_file


def prepare_env_variables(env_files: List[str]) -> Dict[str, str]:
    envs = {}
    local_envs = {}
    for file in env_files:
        path = Path(file)
        if not path.exists():
            continue
        if path.name == DEFAULT_LOCAL_ENV_FILE:
            local_envs.update(parse_env_file(file))
        else:
            envs.update(parse_env_file(file))
    envs.update(local_envs)
    return envs
