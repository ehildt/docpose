from typing import Any
from .store import warn

from libs.constants import (
    TO_BE_LOE,
    TO_BE_GOE,
    TO_CONTAIN,
    TO_EQUAL,
)


def unresolvableEnv(value: Any):
    if isinstance(value, str) and value.startswith("$"):
        return True


def is_boolean(value: Any) -> bool:
    if unresolvableEnv(value):
        return False
    if isinstance(value, bool):
        return True
    if isinstance(value, str) and value.lower() in ("true", "false"):
        return True
    return False


def to_boolean(value: Any, key: str, template: str, rule: str) -> bool:
    if isinstance(value, bool):
        return value

    if isinstance(value, str):
        value_stripped = value.strip().lower()
        if value_stripped in ['true', '"true"', "'true'"]:
            return True
        elif value_stripped in ['false', '"false"', "'false'", '']:
            warn(template, rule, {key: value}, 'falsy')
            return False
        # Attempt to convert the string to a number
        try:
            numeric_value = float(value_stripped)
            if numeric_value == 0:
                warn(template, rule, {key: value}, 'falsy')
                return False
            else:
                warn(template, rule, {key: value}, 'truthy')
                return True
        except ValueError:
            warn(template, rule, {key: value}, 'truthy')
            return True

    if isinstance(value, (int, float)):
        return value != 0

    raise ValueError(f"{template} => {key}; cannot be cast to boolean: {value}")


def compose_item_validator(template: str, env, value, conditions):
    if unresolvableEnv(value):
        warn(template, 'environment', {env: value}, 'truthy')
        return False

    if TO_CONTAIN in conditions:
        expected_value = conditions[TO_CONTAIN]
        if not isinstance(expected_value, str):
            raise ValueError(f"{env} - {TO_CONTAIN} must be of type string")
        elif isinstance(expected_value, str) and str(value) not in expected_value:
            raise ValueError(
                f"{env} - {value} does not contain substring {expected_value}"
            )

    if TO_EQUAL in conditions:
        expected_value = conditions[TO_EQUAL]
        boolean = is_boolean(value)
        if isinstance(expected_value, str):
            if str(value) != expected_value:
                raise ValueError(f"{env} - {value} does not equal {expected_value}")

        elif isinstance(expected_value, int) and not boolean:
            if int(value) != expected_value:
                raise ValueError(f"{env} - {value} does not equal {expected_value}")

        elif isinstance(expected_value, float) and not boolean:
            if float(value) != expected_value:
                raise ValueError(f"{env} - {value} does not equal {expected_value}")

        elif isinstance(expected_value, bool) and boolean:
            if to_boolean(value, env, template, 'environment') == expected_value:
                raise ValueError(f"{env} - {boolean} does not equal {expected_value}")

    if isinstance(value, str) and value.startswith("$"):
        return True

    if TO_BE_GOE in conditions:
        if float(value) < float(conditions[TO_BE_GOE]):
            raise ValueError(
                f"{env} - {value} is not greater than or equal to {conditions[TO_BE_GOE]}"
            )

    if TO_BE_LOE in conditions:
        if float(value) > float(conditions[TO_BE_LOE]):
            raise ValueError(
                f"{env} - {value} is not less than or equal to {conditions[TO_BE_LOE]}"
            )

    return True
