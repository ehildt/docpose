from jinja2 import Environment, FileSystemLoader, TemplateError
from .get_templates import get_templates
from .dict_to_dataclass import dict_to_dataclass
from .get_envs_to_template import get_envs_to_template
from .config_classes import Compose, Config


def render_template(template_dir, template_name, context):
    try:
        env = Environment(loader=FileSystemLoader(template_dir))
        template = env.get_template(template_name)
        return template.render(context)
    except TemplateError as e:
        raise ValueError(f"Template error in {template_name}: {e}")


def render_templates(config: Config):
    tpl_envs = get_envs_to_template(config)
    templates = get_templates(config.compose)
    rendered_templates = {}
    for item in config.compose:
        if isinstance(item, str):
            rendered_templates[item] = render_template(
                config.source.template_dir, item, tpl_envs[item]
            )
            continue

        item = dict_to_dataclass(Compose, item)

        for dep in item.depends_on:
            if dep not in templates:
                raise ValueError(
                    f"{item.template} depends on {dep} but {dep} is not composed"
                )

        if item.template:
            rendered_templates[item.template] = render_template(
                config.source.template_dir, item.template, tpl_envs[item.template]
            )

    return rendered_templates
