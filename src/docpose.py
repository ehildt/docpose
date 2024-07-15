from libs.create_args import create_args
from libs.read_config_yml import read_config_yml
from libs.process_templates import process_templates
from libs.render_templates import render_templates
from libs.write_to_path import write_to_file
from libs.constants import DEFAULT_CONFIG_FILE, SAMPLE_CONFIG


def main():
    args = create_args()
    if args.init:
        write_to_file(DEFAULT_CONFIG_FILE, SAMPLE_CONFIG)
    else:
        config = read_config_yml(args.config)
        rendered_templates = render_templates(config)
        process_templates(config, rendered_templates)


if __name__ == "__main__":
    main()