from pathlib import Path
from .config_classes import Config
from .constants import DEFAULT_CONFIG_FILE
from .check_file_exists import check_files_exists
from .custom_exceptions import (
    FolderNotFoundError,
    NotAFolderError,
    ConditionNotMetError,
)


def validate_template_dir(config: Config):
    template_dir = Path(config.source.template_dir or DEFAULT_CONFIG_FILE)

    if not template_dir.exists():
        raise FolderNotFoundError(f"{template_dir.absolute()}")

    if not template_dir.is_dir():
        raise NotAFolderError(f"{template_dir.absolute()}")


def validate_source_conditionals(config: Config):
    if not config.source.env_files and not config.source.environment:
        raise ConditionNotMetError(
            "At least one of source.[env_files | environment] must be provided."
        )


def validate_config_source(config: Config):
    validate_template_dir(config)
    check_files_exists(config.source.env_files)
    validate_source_conditionals(config)


__all__ = ["validate_config_source"]
