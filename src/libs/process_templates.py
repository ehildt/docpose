from .write_to_path import write_to_file


def process_templates(config, rendered_templates):
    default_output = []

    for o in config.source.outputs[1:]:
        outputs = []

        for conf in config.compose:
            if isinstance(conf, str):
                rendered = rendered_templates[conf]
                if rendered not in default_output:
                    default_output.append(rendered)
                continue

            if "output" in conf and o in conf["output"]:
                outputs.append(rendered_templates[conf["template"]])
                continue

            if "template" in conf and "output" not in conf:
                rendered = rendered_templates[conf["template"]]
                if rendered not in default_output:
                    default_output.append(rendered)

        write_to_file(o, "\n\n".join(outputs))

    write_to_file(config.source.outputs[0], "\n\n".join(default_output))
