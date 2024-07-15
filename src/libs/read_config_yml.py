from yaml import safe_load
from .config_classes import Config
from .dict_to_dataclass import dict_to_dataclass
from .validate_config_source import validate_config_source
from .validate_config_compose import validate_config_compose


def read_config_yml(file_descriptor: str):
    try:
        with open(file_descriptor, "r") as file:
            config = dict_to_dataclass(Config, safe_load(file))
            validate_config_source(config)
            validate_config_compose(config)
            return config
    except FileNotFoundError as error:
        raise error


__all__ = ["read_config_yml"]
