from typing import Dict
from copy import deepcopy
from .constants import (
    TO_BE_LOE,
    TO_BE_GOE,
    TO_CONTAIN,
    TO_EQUAL,
)

from .prepare_env_variables import prepare_env_variables
from .dict_to_dataclass import dict_to_dataclass
from .challenge_env import get_env_from_os
from .config_classes import Compose, Config
from .compose_item_validator import compose_item_validator


def get_envs_to_template(config: Config) -> Dict:
    source_envs = prepare_env_variables(config.source.env_files)
    compose_envs = {}
    for entry in config.compose:
        if isinstance(entry, str):
            compose_envs[entry] = source_envs
            continue

        item = dict_to_dataclass(Compose, entry)

        com_envs = deepcopy(source_envs)
        com_envs.update(prepare_env_variables(item.env_files))

        for env in item.environment:
            for j in env:
                if (
                    isinstance(j, str)
                    and j not in TO_EQUAL
                    and j not in TO_BE_GOE
                    and j not in TO_BE_LOE
                    and j not in TO_CONTAIN
                ):
                    val = get_env_from_os(env[j])
                    if compose_item_validator(item.template, j, val, env):
                        com_envs[j] = val

        compose_envs[item.template] = com_envs
    return compose_envs
