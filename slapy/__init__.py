from pathlib import Path

import toml


def get_version() -> str:
    root = Path(__file__).parents[1]

    f = (root / 'pyproject.toml').open()

    return toml.load(f)['tool']['poetry']['version']


__version__ = get_version()
