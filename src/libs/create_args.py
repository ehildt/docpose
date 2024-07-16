import argparse
from pathlib import Path
from .constants import DESCRIPTION, DEFAULT_CONFIG_FILE


def create_args():
    parser = argparse.ArgumentParser(
        description=DESCRIPTION, formatter_class=argparse.RawTextHelpFormatter
    )
    parser.add_argument(
        "-c",
        "--config",
        type=Path,
        default=DEFAULT_CONFIG_FILE,
        help="Path to the configuration [YAML|YML] file",
    )
    parser.add_argument(
        "-i", "--init", action="store_true", help="Initialize a docpose example config"
    )
    parser.add_argument(
        "-v", "--version", 
        action="store_true", 
        help="Show the docpose version number"
    )

    return parser.parse_args()
