from typing import Any
from jinja2 import Environment


def bool(value: Any):
    if not isinstance(value, str):
        return False

    value = value.lower()

    if value in "true":
        return True

    return False


def jinja2_extend_filters(env: Environment):
    env.filters["bool"] = bool
    return env
