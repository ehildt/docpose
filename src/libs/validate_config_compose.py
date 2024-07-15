from .config_classes import Config, Compose
from .dict_to_dataclass import dict_to_dataclass
from .custom_exceptions import TemplateRequiredError
from .check_file_exists import check_files_exists


def validate_config_compose(config: Config):
    for entry in config.compose:
        if isinstance(entry, str):
            continue

        item = dict_to_dataclass(Compose, entry)

        if not item.template:
            raise TemplateRequiredError("Field template is required")

        check_files_exists([f"{config.source.template_dir}/{item.template}"])
        check_files_exists(item.env_files)
