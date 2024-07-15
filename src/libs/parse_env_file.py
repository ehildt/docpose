from .challenge_env import get_env_var_from_line


def parse_env_file(env_path: str):
    env_vars = {}
    try:
        with open(env_path) as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith("#"):
                    key, value = get_env_var_from_line(line)
                    env_vars[key] = value
        return env_vars
    except Exception as e:
        raise e
