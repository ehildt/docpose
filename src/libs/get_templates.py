from .config_classes import Compose


def get_templates(compose: Compose):
    templates = []
    for entry in compose:
        if isinstance(entry, str):
            templates.append(entry)
        else:
            templates.append(entry['template'])
    return templates