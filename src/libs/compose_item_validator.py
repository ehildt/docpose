from typing import Any

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


def to_boolean(value: Any) -> bool:
    if isinstance(value, bool):
        return value
    if isinstance(value, str):
        value_lower = value.lower()
        if value_lower == "true":
            return True
        elif value_lower == "false":
            return False
    raise ValueError("Cannot cast to boolean")


def compose_item_validator(template: str, env, value, conditions):
    if unresolvableEnv(value):
        print(f"[WARN] {template} => environment => {env}: {value}; could not be resolved (was this intentional?)")
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
            if to_boolean(value) == expected_value:
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
